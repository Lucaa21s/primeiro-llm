import { useState, useEffect } from "react"
import { Search, X, Filter } from "lucide-react"

interface HistoryItem {
  id: string
  title: string
  timestamp: Date
  mode: string
}

interface HistorySearchProps {
  items: HistoryItem[]
  onSelect: (id: string) => void
  onClose: () => void
}

export function HistorySearch({ items, onSelect, onClose }: HistorySearchProps) {
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedMode, setSelectedMode] = useState<string | null>(null)

  const modes = ["chat", "agent", "multi-agent", "agi"]

  const filtered = items.filter((item) => {
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesMode = !selectedMode || item.mode === selectedMode
    return matchesSearch && matchesMode
  })

  return (
    <div className="history-search-overlay">
      <div className="history-search-modal">
        <div className="history-search-header">
          <div className="history-search-input-wrapper">
            <Search size={18} />
            <input
              type="text"
              placeholder="Buscar no histórico..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              autoFocus
              className="history-search-input"
            />
          </div>
          <button onClick={onClose} className="history-search-close">
            <X size={20} />
          </button>
        </div>

        <div className="history-search-filters">
          <button
            className={`filter-chip ${!selectedMode ? "active" : ""}`}
            onClick={() => setSelectedMode(null)}
          >
            Todos
          </button>
          {modes.map((mode) => (
            <button
              key={mode}
              className={`filter-chip ${selectedMode === mode ? "active" : ""}`}
              onClick={() => setSelectedMode(mode)}
            >
              {mode}
            </button>
          ))}
        </div>

        <div className="history-search-results">
          {filtered.length === 0 ? (
            <div className="history-search-empty">
              <p>Nenhum resultado encontrado</p>
            </div>
          ) : (
            filtered.map((item) => (
              <button
                key={item.id}
                className="history-search-item"
                onClick={() => {
                  onSelect(item.id)
                  onClose()
                }}
              >
                <div className="history-search-item-content">
                  <span className="history-search-item-title">{item.title}</span>
                  <span className="history-search-item-meta">
                    {item.mode} · {formatDate(item.timestamp)}
                  </span>
                </div>
              </button>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

function formatDate(date: Date): string {
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return "Hoje"
  if (days === 1) return "Ontem"
  if (days < 7) return `${days}d atrás`
  if (days < 30) return `${Math.floor(days / 7)}w atrás`
  return date.toLocaleDateString("pt-BR")
}
