"use client"

import { useState, useRef, useEffect, useCallback } from "react"
import { MarkdownMessage } from "@/components/chat/MarkdownMessage"

// ─── Tipos ────────────────────────────────────────────────────────────────────

type AIMode = "chat" | "agent" | "multi-agent" | "agi"
type UploadStatus = "idle" | "uploading" | "success" | "error"

interface Message {
  role: "user" | "assistant"
  content: string
  mode?: AIMode
  isStreaming?: boolean
}

interface ChatSession {
  id: string
  title: string
  timestamp: Date
  mode: AIMode
}

// ─── Constantes ───────────────────────────────────────────────────────────────

const API_BASE = "http://localhost:8000"

const MODES: { id: AIMode; label: string; icon: string; endpoint: string; color: string }[] = [
  { id: "chat",        label: "Chat",        icon: "💬", endpoint: "/chat",        color: "chat"  },
  { id: "agent",       label: "Agent",       icon: "🤖", endpoint: "/agent",       color: "agent" },
  { id: "multi-agent", label: "Multi",       icon: "🕸️", endpoint: "/multi-agent", color: "multi" },
  { id: "agi",         label: "AGI",         icon: "🧠", endpoint: "/agi",         color: "agi"   },
]

const SUGGESTIONS = [
  "Explique o que é RAG e como funciona",
  "Crie um agente de pesquisa em Python",
  "Como funciona o pgvector?",
  "Descreva a arquitetura de multi-agentes",
]

// ─── Componente Principal ────────────────────────────────────────────────────

export default function Home() {
  const [messages, setMessages]         = useState<Message[]>([])
  const [input, setInput]               = useState("")
  const [loading, setLoading]           = useState(false)
  const [activeMode, setActiveMode]     = useState<AIMode>("chat")
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>("idle")
  const [uploadedFile, setUploadedFile] = useState<string>("")
  const [sessions, setSessions]         = useState<ChatSession[]>([])
  const [activeSession, setActiveSession] = useState<string | null>(null)

  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef    = useRef<HTMLTextAreaElement>(null)
  const fileInputRef   = useRef<HTMLInputElement>(null)

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  // Auto-resize textarea
  useEffect(() => {
    const ta = textareaRef.current
    if (!ta) return
    ta.style.height = "auto"
    ta.style.height = Math.min(ta.scrollHeight, 160) + "px"
  }, [input])

  // ─── Upload PDF ─────────────────────────────────────────────────────────────

  const handleUpload = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploadStatus("uploading")
    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await fetch(`${API_BASE}/uploadfile/`, {
        method: "POST",
        body: formData,
      })
      if (!res.ok) throw new Error("Upload failed")
      const data = await res.json()
      setUploadedFile(file.name)
      setUploadStatus("success")
      // Toast message in chat
      setMessages(prev => [...prev, {
        role: "assistant",
        content: `✅ **PDF carregado com sucesso!**\n\nArquivo: \`${file.name}\`\nStatus: processando embeddings e injetando no banco vetorial em background.\n\nAgora você pode fazer perguntas sobre o conteúdo do documento!`,
        mode: "chat",
      }])
    } catch {
      setUploadStatus("error")
      setTimeout(() => setUploadStatus("idle"), 3000)
    }
  }, [])

  // ─── Send Message ────────────────────────────────────────────────────────────

  const sendMessage = useCallback(async (override?: string) => {
    const text = (override ?? input).trim()
    if (!text || loading) return

    const currentMode = MODES.find(m => m.id === activeMode)!
    const userMsg: Message = { role: "user", content: text, mode: activeMode }

    setMessages(prev => [...prev, userMsg])
    setInput("")
    setLoading(true)

    // Create session on first message
    if (messages.length === 0) {
      const session: ChatSession = {
        id: Date.now().toString(),
        title: text.slice(0, 35) + (text.length > 35 ? "…" : ""),
        timestamp: new Date(),
        mode: activeMode,
      }
      setSessions(prev => [session, ...prev])
      setActiveSession(session.id)
    }

    // Placeholder assistant message for streaming
    const placeholderIdx = messages.length + 1
    setMessages(prev => [...prev, {
      role: "assistant",
      content: "",
      mode: activeMode,
      isStreaming: true,
    }])

    try {
      const res = await fetch(`${API_BASE}${currentMode.endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [
            ...messages.map(m => ({ role: m.role, content: m.content })),
            { role: "user", content: text },
          ],
        }),
      })

      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      if (!res.body) throw new Error("No response body")

      // ── Streaming Reader ──
      const reader  = res.body.getReader()
      const decoder = new TextDecoder()
      let accumulated = ""

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const raw = decoder.decode(value, { stream: true })

        // Handle both SSE format and plain text
        const lines = raw.split("\n")
        for (const line of lines) {
          let chunk = ""
          if (line.startsWith("data: ")) {
            try { chunk = JSON.parse(line.slice(6)) } catch { chunk = line.slice(6) }
          } else {
            chunk = line
          }
          accumulated += chunk
        }

        const snapshot = accumulated
        setMessages(prev => {
          const updated = [...prev]
          updated[updated.length - 1] = {
            role: "assistant",
            content: snapshot,
            mode: activeMode,
            isStreaming: true,
          }
          return updated
        })
      }

      // Finalize
      setMessages(prev => {
        const updated = [...prev]
        updated[updated.length - 1] = {
          role: "assistant",
          content: accumulated || "(sem resposta)",
          mode: activeMode,
          isStreaming: false,
        }
        return updated
      })

    } catch (err) {
      setMessages(prev => {
        const updated = [...prev]
        updated[updated.length - 1] = {
          role: "assistant",
          content: `❌ **Erro de conexão**\n\nNão foi possível conectar ao backend em \`${API_BASE}\`. Verifique se o uvicorn está rodando.\n\n\`\`\`\nuvicorn main:app --reload\n\`\`\``,
          mode: activeMode,
          isStreaming: false,
        }
        return updated
      })
    } finally {
      setLoading(false)
    }
  }, [input, loading, messages, activeMode])

  // ─── Keyboard Handler ────────────────────────────────────────────────────────

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  // ─── New Chat ─────────────────────────────────────────────────────────────────

  const newChat = () => {
    setMessages([])
    setInput("")
    setActiveSession(null)
    setUploadStatus("idle")
    setUploadedFile("")
  }

  // ─── Render ───────────────────────────────────────────────────────────────────

  const currentModeInfo = MODES.find(m => m.id === activeMode)!

  return (
    <div className="app-shell">

      {/* ═══ SIDEBAR ═══ */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="brand">
            <div className="brand-icon">⚡</div>
            <div>
              <div className="brand-name">Primeiro LLM</div>
              <div className="brand-version">v2.0 Async</div>
            </div>
          </div>
          <button className="new-chat-btn" onClick={newChat} id="new-chat-btn">
            <span>＋</span> Novo Chat
          </button>
        </div>

        {/* Mode Selector */}
        <div className="mode-section">
          <div className="mode-label">Modo de IA</div>
          <div className="mode-grid">
            {MODES.map(mode => (
              <button
                key={mode.id}
                id={`mode-${mode.id}`}
                className={`mode-btn ${activeMode === mode.id ? "active" : ""}`}
                onClick={() => setActiveMode(mode.id)}
                title={mode.label}
              >
                <span className="mode-btn-icon">{mode.icon}</span>
                {mode.label}
              </button>
            ))}
          </div>
        </div>

        {/* History */}
        <div className="history-section">
          {sessions.length > 0 && (
            <>
              <div className="history-group-label" style={{ marginTop: "16px" }}>Recentes</div>
              {sessions.map(session => (
                <div
                  key={session.id}
                  className={`history-item ${activeSession === session.id ? "active" : ""}`}
                  onClick={() => setActiveSession(session.id)}
                >
                  <span style={{ fontSize: "13px" }}>
                    {MODES.find(m => m.id === session.mode)?.icon}
                  </span>
                  <span className="history-item-text">{session.title}</span>
                </div>
              ))}
            </>
          )}
        </div>

        {/* Footer */}
        <div className="sidebar-footer">
          <div className="model-badge">
            <span className="model-badge-icon">🦙</span>
            <div className="model-badge-text">
              <span className="model-badge-name">Llama 3</span>
              <span className="model-badge-sub">via Ollama · RTX 3060</span>
            </div>
            <div className="status-dot" title="Conectado" />
          </div>
        </div>
      </aside>

      {/* ═══ CHAT MAIN ═══ */}
      <main className="chat-main">

        {/* Topbar */}
        <div className="chat-topbar">
          <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
            <span className="chat-topbar-title">
              {currentModeInfo.icon} {activeSession
                ? sessions.find(s => s.id === activeSession)?.title ?? "Conversa"
                : "Nova Conversa"
              }
            </span>
            <span className={`mode-indicator ${currentModeInfo.color}`}>
              {currentModeInfo.label}
            </span>
          </div>

          <div className="topbar-actions">
            {/* Upload PDF */}
            <label
              id="upload-pdf-btn"
              className={`upload-btn ${uploadStatus === "success" ? "success" : ""} ${uploadStatus === "uploading" ? "uploading" : ""}`}
            >
              {uploadStatus === "success"
                ? `✓ ${uploadedFile.slice(0, 20)}${uploadedFile.length > 20 ? "…" : ""}`
                : uploadStatus === "uploading"
                ? "⏳ Processando…"
                : "📎 Anexar PDF"
              }
              <input
                ref={fileInputRef}
                type="file"
                accept="application/pdf"
                onChange={handleUpload}
                className="hidden"
                style={{ display: "none" }}
              />
            </label>
          </div>
        </div>

        {/* Messages */}
        <div className="messages-area" id="messages-area">

          {messages.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">⚡</div>
              <div className="empty-state-title">Primeiro LLM está pronto</div>
              <div className="empty-state-sub">
                Plataforma de IA local com Ollama, RAG, Agentes Autônomos e Multi-Agentes.
                Selecione um modo na sidebar e inicie uma conversa.
              </div>
              <div className="suggestion-chips">
                {SUGGESTIONS.map((s, i) => (
                  <button
                    key={i}
                    className="chip"
                    onClick={() => sendMessage(s)}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg, idx) => {
              const isUser = msg.role === "user"
              const isEmpty = !msg.content && msg.isStreaming

              return (
                <div key={idx} className={`message-row ${isUser ? "user" : ""}`}>
                  <div className={`avatar ${isUser ? "user" : "ai"}`}>
                    {isUser ? "🧑" : currentModeInfo.icon}
                  </div>
                  <div className={`bubble ${isUser ? "user" : "ai"}`}>
                    {isEmpty ? (
                      <div className="typing-indicator">
                        <div className="typing-dot" />
                        <div className="typing-dot" />
                        <div className="typing-dot" />
                      </div>
                    ) : isUser ? (
                      <span style={{ whiteSpace: "pre-wrap" }}>{msg.content}</span>
                    ) : (
                      <MarkdownMessage content={msg.content} />
                    )}
                  </div>
                </div>
              )
            })
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="input-area">
          <div className="input-wrapper">
            <textarea
              id="chat-input"
              ref={textareaRef}
              className="chat-textarea"
              placeholder={`Envie uma mensagem para o modo ${currentModeInfo.label}… (Enter para enviar, Shift+Enter para nova linha)`}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={1}
              disabled={loading}
            />
            <div className="input-actions">
              <div className="input-left">
                <span className="input-hint">
                  {uploadStatus === "success"
                    ? `📄 ${uploadedFile} indexado`
                    : "Shift+Enter = nova linha"}
                </span>
              </div>
              <button
                id="send-btn"
                className="send-btn"
                onClick={() => sendMessage()}
                disabled={loading || !input.trim()}
              >
                {loading ? (
                  <>
                    <span style={{ display: "inline-block", animation: "spin 1s linear infinite" }}>⟳</span>
                    Gerando…
                  </>
                ) : (
                  <>Enviar ↑</>
                )}
              </button>
            </div>
          </div>
        </div>

      </main>
    </div>
  )
}
