import React, { useRef, useEffect } from "react"
import { Send, Paperclip, Loader2 } from "lucide-react"

interface EnhancedChatInputProps {
  value: string
  onChange: (value: string) => void
  onSubmit: () => void
  onKeyDown: (e: React.KeyboardEvent<HTMLTextAreaElement>) => void
  isLoading: boolean
  onFileUpload?: () => void
  uploadStatus?: "idle" | "uploading" | "success" | "error"
  uploadedFile?: string
  placeholder?: string
}

export function EnhancedChatInput({
  value,
  onChange,
  onSubmit,
  onKeyDown,
  isLoading,
  onFileUpload,
  uploadStatus = "idle",
  uploadedFile = "",
  placeholder = "Escreva sua mensagem...",
}: EnhancedChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    const ta = textareaRef.current
    if (!ta) return
    ta.style.height = "auto"
    ta.style.height = Math.min(ta.scrollHeight, 160) + "px"
  }, [value])

  return (
    <div className="input-area">
      <div className="input-wrapper">
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder={placeholder}
          className="chat-textarea"
          disabled={isLoading}
        />
        <div className="input-actions">
          <div className="input-left">
            <button
              onClick={onFileUpload}
              className={`input-icon-btn ${uploadStatus === "uploading" ? "uploading" : ""} ${uploadStatus === "success" ? "success" : ""}`}
              title="Anexar arquivo"
              disabled={isLoading}
            >
              {uploadStatus === "uploading" ? (
                <Loader2 size={18} className="animate-spin" />
              ) : (
                <Paperclip size={18} />
              )}
            </button>
            {uploadStatus === "success" && uploadedFile && (
              <span className="upload-indicator">✓ {uploadedFile.slice(0, 15)}</span>
            )}
          </div>
          <button
            onClick={onSubmit}
            disabled={isLoading || !value.trim()}
            className="send-btn"
            title="Enviar (Enter)"
          >
            {isLoading ? (
              <Loader2 size={16} className="animate-spin" />
            ) : (
              <Send size={16} />
            )}
          </button>
        </div>
      </div>
    </div>
  )
}
