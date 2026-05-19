import { useEffect, useState } from "react"
import { Moon, Sun } from "lucide-react"

export function ThemeToggle() {
  const [theme, setTheme] = useState<"light" | "dark" | "auto">("auto")
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    const stored = localStorage.getItem("theme") as "light" | "dark" | "auto" | null
    if (stored) {
      setTheme(stored)
      applyTheme(stored)
    }
  }, [])

  const applyTheme = (newTheme: "light" | "dark" | "auto") => {
    const html = document.documentElement
    
    if (newTheme === "auto") {
      const isDark = window.matchMedia("(prefers-color-scheme: dark)").matches
      html.style.colorScheme = isDark ? "dark" : "light"
    } else {
      html.style.colorScheme = newTheme
    }
    
    localStorage.setItem("theme", newTheme)
  }

  const toggleTheme = () => {
    const themes: Array<"light" | "dark" | "auto"> = ["auto", "light", "dark"]
    const currentIndex = themes.indexOf(theme)
    const nextTheme = themes[(currentIndex + 1) % themes.length]
    
    setTheme(nextTheme)
    applyTheme(nextTheme)
  }

  if (!mounted) return null

  return (
    <button
      onClick={toggleTheme}
      className="theme-toggle-btn"
      title={`Tema: ${theme}`}
      aria-label="Alternar tema"
    >
      {theme === "dark" || (theme === "auto" && window.matchMedia("(prefers-color-scheme: dark)").matches) ? (
        <Moon size={16} />
      ) : (
        <Sun size={16} />
      )}
    </button>
  )
}
