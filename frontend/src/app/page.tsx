"use client"

import { useState } from "react"
import { MarkdownMessage } from "@/components/chat/MarkdownMessage"
import axios from "axios"

interface Message {
  role: "user" | "assistant"
  content: string
}

export default function Home() {
  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [pdfText, setPdfText] = useState("") // Estado para armazenar o texto extraído do PDF

  // Função para fazer o upload do PDF para o backend FastAPI
  async function uploadPDF(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]
    if (!file) return

    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await axios.post(
        "http://localhost:8000/upload-pdf",
        formData
      )
      setPdfText(res.data.text)
      alert("PDF carregado com sucesso!")
    } catch (error) {
      console.error("Erro ao carregar o PDF:", error)
      alert("Falha ao enviar o arquivo PDF.")
    }
  }

  // Função para enviar mensagem utilizando o contexto do PDF
  async function sendMessage() {
    if (!message.trim()) return

    const updatedMessages: Message[] = [
      ...messages,
      {
        role: "user",
        content: message,
      },
    ]

    setMessages(updatedMessages)
    setMessage("")
    setLoading(true)

    const assistantMessage: Message = {
      role: "assistant",
      content: "",
    }

    setMessages((prev) => [...prev, assistantMessage])

    // Envia o histórico injetando o conteúdo do documento no System Prompt
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages: [
          {
            role: "system",
            content: `Você possui acesso ao seguinte PDF:\n\n${pdfText}`,
          },
          ...updatedMessages,
          ],
      }),
    })

    const reader = res.body?.getReader()
    if (!reader) return

    const decoder = new TextDecoder()
    let fullResponse = ""

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value)
      const lines = chunk
        .split("\n")
        .filter((line) => line.startsWith("data: "))

      for (const line of lines) {
        const text = JSON.parse(line.replace("data: ", ""))
        fullResponse += text

        setMessages((prev) => {
          const updated = [...prev]
          updated[updated.length - 1] = {
            role: "assistant",
            content: fullResponse,
          }
          return updated
        })
      }
    }

    setLoading(false)
  }

  return (
    <main className="flex h-screen bg-zinc-950 text-white">
      <div className="flex flex-col w-full max-w-5xl mx-auto p-6 gap-4">

        {/* Cabeçalho */}
        <header className="flex justify-between items-center border-b border-zinc-800 pb-4">
          <h1 className="text-2xl font-bold tracking-wide">
            AI Assistant Pro <span className="text-xs bg-blue-600 px-2 py-0.5 rounded text-white ml-2">Fase 5</span>
          </h1>
          {/* Seletor de Arquivos Estilizado */}
          <label className="flex items-center gap-2 cursor-pointer bg-zinc-900 border border-zinc-800 hover:border-zinc-700 rounded-xl px-4 py-2 text-xs font-medium transition shadow-sm">
            <span className={pdfText ? "text-green-400" : "text-zinc-400"}>
              {pdfText ? "✓ Documento Pronto" : "Anexar PDF"}
            </span>
            <input
              type="file"
              accept="application/pdf"
              onChange={uploadPDF}
              className="hidden"
            />
          </label>
        </header>

        {/* Histórico de Conversas */}
        <div className="flex-1 overflow-y-auto bg-zinc-900/50 rounded-2xl p-4 space-y-4 border border-zinc-800/80 backdrop-blur-sm">
          {messages.length === 0 && (
            <div className="h-full flex items-center justify-center text-zinc-500 text-sm">
              Faça upload de um PDF ou envie um comando para iniciar.
            </div>
          )}
          {messages.map((msg, index) => {
            // Não renderiza o container vazio do assistente antes do stream começar
            if (msg.role === "assistant" && !msg.content && loading) return null;
            
            return (
              <div
                key={index}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`p-4 rounded-2xl shadow-lg border text-sm max-w-[85%] leading-relaxed
                    ${
                      msg.role === "user"
                        ? "bg-blue-600 border-blue-500 text-white rounded-br-none"
                        : "bg-zinc-900 border-zinc-800 text-zinc-100 rounded-bl-none"
                    }
                  `}
                >
                  <MarkdownMessage content={msg.content} />
                </div>
              </div>
            );
          })}
        </div>

        {/* Barra de Entrada de Mensagem */}
        <footer className="flex gap-2 items-end">
          <textarea
            placeholder={pdfText ? "Pergunte algo sobre o PDF carregado..." : "Digite sua mensagem..."}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
              }
            }}
            className="
              flex-1
              bg-zinc-900
              border
              border-zinc-800
              rounded-2xl
              p-4
              outline-none
              resize-none
              min-h-[60px]
              max-h-[160px]
              text-sm
              focus:border-zinc-700
              transition
            "
          />

          <button
            onClick={sendMessage}
            disabled={loading}
            className="
              rounded-2xl
              px-6
              py-4
              font-medium
              bg-white
              text-black
              hover:bg-zinc-200
              disabled:bg-zinc-800
              disabled:text-zinc-600
              transition
              h-[60px]
            "
          >
            {loading ? "..." : "Enviar"}
          </button>
        </footer>

      </div>
    </main>
  )
}
