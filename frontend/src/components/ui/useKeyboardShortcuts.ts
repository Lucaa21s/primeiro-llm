import { useCallback, useEffect } from "react"

export interface KeyboardShortcuts {
  [key: string]: {
    description: string
    handler: () => void
    ctrlKey?: boolean
    shiftKey?: boolean
    altKey?: boolean
  }
}

export function useKeyboardShortcuts(shortcuts: KeyboardShortcuts) {
  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      for (const [key, config] of Object.entries(shortcuts)) {
        const matchKey = event.key.toLowerCase() === key.toLowerCase()
        const matchCtrl = config.ctrlKey ? event.ctrlKey : !event.ctrlKey
        const matchShift = config.shiftKey ? event.shiftKey : !event.shiftKey
        const matchAlt = config.altKey ? event.altKey : !event.altKey

        if (matchKey && matchCtrl && matchShift && matchAlt) {
          event.preventDefault()
          config.handler()
          break
        }
      }
    },
    [shortcuts]
  )

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown)
    return () => window.removeEventListener("keydown", handleKeyDown)
  }, [handleKeyDown])
}

export const DEFAULT_SHORTCUTS: KeyboardShortcuts = {
  n: {
    description: "Novo chat",
    handler: () => {},
    ctrlKey: true,
  },
  "/": {
    description: "Foco no input",
    handler: () => {
      const input = document.querySelector(".chat-textarea") as HTMLTextAreaElement
      input?.focus()
    },
  },
  "?": {
    description: "Ajuda/Atalhos",
    handler: () => {
      console.log("Exibir ajuda")
    },
    shiftKey: true,
  },
  k: {
    description: "Buscar histórico",
    handler: () => {},
    ctrlKey: true,
  },
}
