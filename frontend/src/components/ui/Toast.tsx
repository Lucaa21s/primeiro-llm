import { useState, useEffect } from "react"
import { Bell, X } from "lucide-react"

export type ToastType = "success" | "error" | "info" | "warning"

interface Toast {
  id: string
  message: string
  type: ToastType
  duration?: number
}

interface ToastContextType {
  toasts: Toast[]
  addToast: (message: string, type: ToastType, duration?: number) => void
  removeToast: (id: string) => void
}

let toastId = 0

export const useToast = (() => {
  let listeners: Array<(toasts: Toast[]) => void> = []
  let toasts: Toast[] = []

  return {
    useToast: () => {
      const [state, setState] = useState<Toast[]>([])

      useEffect(() => {
        setState(toasts)
        const listener = (newToasts: Toast[]) => setState(newToasts)
        listeners.push(listener)

        return () => {
          listeners = listeners.filter((l) => l !== listener)
        }
      }, [])

      return {
        toasts: state,
        addToast: (message: string, type: ToastType = "info", duration = 4000) => {
          const id = `toast-${toastId++}`
          const toast: Toast = { id, message, type, duration }
          toasts = [...toasts, toast]
          listeners.forEach((l) => l(toasts))

          if (duration > 0) {
            setTimeout(() => {
              toasts = toasts.filter((t) => t.id !== id)
              listeners.forEach((l) => l(toasts))
            }, duration)
          }

          return id
        },
        removeToast: (id: string) => {
          toasts = toasts.filter((t) => t.id !== id)
          listeners.forEach((l) => l(toasts))
        },
      }
    },
  }
})()

export function ToastContainer() {
  const { toasts, removeToast } = useToast.useToast()

  return (
    <div className="toast-container">
      {toasts.map((toast) => (
        <Toast
          key={toast.id}
          toast={toast}
          onClose={() => removeToast(toast.id)}
        />
      ))}
    </div>
  )
}

interface ToastProps {
  toast: Toast
  onClose: () => void
}

function Toast({ toast, onClose }: ToastProps) {
  const icons = {
    success: "✓",
    error: "✕",
    warning: "⚠",
    info: "ℹ",
  }

  return (
    <div className={`toast toast-${toast.type}`}>
      <span className="toast-icon">{icons[toast.type]}</span>
      <span className="toast-message">{toast.message}</span>
      <button
        onClick={onClose}
        className="toast-close"
        aria-label="Fechar"
      >
        <X size={14} />
      </button>
    </div>
  )
}
