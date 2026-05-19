import React from "react"

interface MessageCardProps {
  role: "user" | "assistant"
  children: React.ReactNode
  isStreaming?: boolean
  mode?: string
}

export function MessageCard({ role, children, isStreaming, mode }: MessageCardProps) {
  return (
    <div className={`message-row ${role}`}>
      <div className={`avatar ${role}`}>
        {role === "assistant" ? "🤖" : "👤"}
      </div>
      <div className={`bubble ${role} ${isStreaming ? "streaming" : ""}`}>
        {children}
      </div>
    </div>
  )
}
