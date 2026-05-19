import React, { useState } from "react"
import { Menu, X } from "lucide-react"

interface SidebarNavProps {
  isOpen?: boolean
  onToggle?: () => void
  children: React.ReactNode
}

export function SidebarNav({ isOpen = true, onToggle, children }: SidebarNavProps) {
  const [mobileOpen, setMobileOpen] = useState(false)

  const handleToggle = () => {
    setMobileOpen(!mobileOpen)
    onToggle?.()
  }

  return (
    <>
      {/* Mobile Toggle */}
      <button
        onClick={handleToggle}
        className="sidebar-mobile-toggle"
        aria-label="Abrir/fechar menu"
      >
        {mobileOpen ? <X size={20} /> : <Menu size={20} />}
      </button>

      {/* Sidebar */}
      <aside className={`sidebar ${mobileOpen ? "open" : ""}`}>
        {children}
      </aside>

      {/* Mobile Backdrop */}
      {mobileOpen && <div className="sidebar-backdrop" onClick={handleToggle} />}
    </>
  )
}
