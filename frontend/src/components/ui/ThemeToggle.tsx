import { useState } from "react"
import { Moon, Sun } from "lucide-react"

export function ThemeToggle() {
  const [theme, setTheme] = useState<"light" | "dark" | "auto">(() => {
    if (typeof window === "undefined") return "auto"
    const stored = localStorage.getItem("theme") as "light" | "dark" | "auto" | null
    return stored ?? "auto"
  })

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

  const isDarkPreferred =
    typeof window !== "undefined" && window.matchMedia("(prefers-color-scheme: dark)").matches

  return (
    <button
      onClick={toggleTheme}
      className="theme-toggle-btn"
      title={`Tema: ${theme}`}
      aria-label="Alternar tema"
    >
      {theme === "dark" || (theme === "auto" && isDarkPreferred) ? (
        <Moon size={16} />
      ) : (
        <Sun size={16} />
      )}
    </button>
  )
}
