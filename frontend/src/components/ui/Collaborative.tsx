import { useEffect, useState } from "react"
import { Users, Wifi } from "lucide-react"

interface CollaborativeSession {
  id: string
  userId: string
  userName: string
  isActive: boolean
  lastSeen: Date
  color: string
}

interface CollaborativeIndicatorProps {
  sessions: CollaborativeSession[]
  onInvite?: () => void
}

export function CollaborativeIndicator({
  sessions,
  onInvite,
}: CollaborativeIndicatorProps) {
  const [connectionStatus, setConnectionStatus] = useState<"connected" | "disconnected" | "connecting">(
    "connected"
  )

  useEffect(() => {
    const handleOnline = () => setConnectionStatus("connected")
    const handleOffline = () => setConnectionStatus("disconnected")

    window.addEventListener("online", handleOnline)
    window.addEventListener("offline", handleOffline)

    return () => {
      window.removeEventListener("online", handleOnline)
      window.removeEventListener("offline", handleOffline)
    }
  }, [])

  const activeSessions = sessions.filter((s) => s.isActive)

  return (
    <div className="collaborative-indicator">
      <div className={`connection-status ${connectionStatus}`}>
        <Wifi size={14} />
        <span>{connectionStatus === "connected" ? "Conectado" : "Offline"}</span>
      </div>

      {activeSessions.length > 0 && (
        <div className="active-users">
          <Users size={14} />
          <span>{activeSessions.length} usuário(s)</span>
          <div className="user-avatars">
            {activeSessions.map((session) => (
              <div
                key={session.id}
                className="user-avatar"
                style={{
                  backgroundColor: session.color,
                  borderColor: session.color,
                }}
                title={session.userName}
              >
                {session.userName[0].toUpperCase()}
              </div>
            ))}
          </div>
        </div>
      )}

      {onInvite && (
        <button onClick={onInvite} className="invite-btn" title="Convidar usuário">
          ＋ Convidar
        </button>
      )}
    </div>
  )
}

export function useWebSocketConnection(url: string) {
  const [isConnected, setIsConnected] = useState(false)
  const [sessions, setSessions] = useState<CollaborativeSession[]>([])

  useEffect(() => {
    if (typeof window === "undefined") return

    const ws = new WebSocket(url)

    ws.onopen = () => setIsConnected(true)
    ws.onclose = () => setIsConnected(false)
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.type === "user_joined" || data.type === "users_list") {
          setSessions(data.sessions || [])
        }
      } catch (err) {
        console.error("Failed to parse WebSocket message:", err)
      }
    }

    return () => ws.close()
  }, [url])

  return { isConnected, sessions }
}
