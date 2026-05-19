import { useState } from "react"
import { Palette } from "lucide-react"

interface ThemeCustomizer {
  primaryColor: string
  accentColor: string
  backgroundColor: string
  surfaceColor: string
}

const PRESET_THEMES: Record<string, ThemeCustomizer> = {
  default: {
    primaryColor: "#6366f1",
    accentColor: "#8b5cf6",
    backgroundColor: "#09090b",
    surfaceColor: "#18181b",
  },
  ocean: {
    primaryColor: "#0ea5e9",
    accentColor: "#06b6d4",
    backgroundColor: "#0f172a",
    surfaceColor: "#1e293b",
  },
  sunset: {
    primaryColor: "#f97316",
    accentColor: "#ec4899",
    backgroundColor: "#1f1f23",
    surfaceColor: "#2a2a2f",
  },
  forest: {
    primaryColor: "#10b981",
    accentColor: "#14b8a6",
    backgroundColor: "#0f2f1f",
    surfaceColor: "#1a3a2a",
  },
  cyberpunk: {
    primaryColor: "#ff00ff",
    accentColor: "#00ffff",
    backgroundColor: "#0a0e27",
    surfaceColor: "#151b3a",
  },
}

interface ThemeCustomizerProps {
  onClose: () => void
  onApply: (theme: ThemeCustomizer) => void
}

export function ThemeCustomizerModal({
  onClose,
  onApply,
}: ThemeCustomizerProps) {
  const [customTheme, setCustomTheme] = useState<ThemeCustomizer>(
    PRESET_THEMES.default
  )
  const [activePreset, setActivePreset] = useState("default")

  const applyPreset = (presetName: string) => {
    const preset = PRESET_THEMES[presetName]
    setCustomTheme(preset)
    setActivePreset(presetName)
  }

  const handleColorChange = (
    key: keyof ThemeCustomizer,
    value: string
  ) => {
    const updated = { ...customTheme, [key]: value }
    setCustomTheme(updated)
    setActivePreset("")
  }

  const handleApply = () => {
    onApply(customTheme)
    // Persist to localStorage
    localStorage.setItem("customTheme", JSON.stringify(customTheme))
    onClose()
  }

  return (
    <div className="theme-customizer-overlay">
      <div className="theme-customizer-modal">
        <div className="theme-customizer-header">
          <h2>Customizar Tema</h2>
          <button onClick={onClose} className="close-btn">✕</button>
        </div>

        {/* Preset Themes */}
        <div className="theme-customizer-section">
          <h3>Temas Predefinidos</h3>
          <div className="preset-grid">
            {Object.entries(PRESET_THEMES).map(([name, theme]) => (
              <button
                key={name}
                className={`preset-btn ${activePreset === name ? "active" : ""}`}
                onClick={() => applyPreset(name)}
                title={name}
              >
                <div className="preset-preview">
                  <div
                    className="preset-swatch-primary"
                    style={{ backgroundColor: theme.primaryColor }}
                  />
                  <div
                    className="preset-swatch-accent"
                    style={{ backgroundColor: theme.accentColor }}
                  />
                </div>
                <span>{name}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Custom Colors */}
        <div className="theme-customizer-section">
          <h3>Cores Personalizadas</h3>
          <div className="color-picker-group">
            {(Object.entries(customTheme) as Array<[keyof ThemeCustomizer, string]>).map(
              ([key, value]) => (
                <div key={key} className="color-picker-item">
                  <label>{key.replace(/([A-Z])/g, " $1")}</label>
                  <div className="color-input-wrapper">
                    <input
                      type="color"
                      value={value}
                      onChange={(e) => handleColorChange(key, e.target.value)}
                      className="color-input"
                    />
                    <span className="color-value">{value}</span>
                  </div>
                </div>
              )
            )}
          </div>
        </div>

        {/* Preview */}
        <div className="theme-customizer-section">
          <h3>Pré-visualização</h3>
          <div
            className="theme-preview"
            style={{
              backgroundColor: customTheme.backgroundColor,
              borderColor: customTheme.primaryColor,
            }}
          >
            <div
              className="preview-box"
              style={{
                backgroundColor: customTheme.surfaceColor,
                borderColor: customTheme.primaryColor,
              }}
            >
              <button
                style={{
                  background: `linear-gradient(135deg, ${customTheme.primaryColor} 0%, ${customTheme.accentColor} 100%)`,
                }}
                className="preview-btn"
              >
                Enviar
              </button>
              <div
                className="preview-message"
                style={{
                  background: `linear-gradient(135deg, ${customTheme.primaryColor}22 0%, ${customTheme.accentColor}11 100%)`,
                  borderColor: customTheme.primaryColor + "33",
                }}
              >
                Mensagem de exemplo
              </div>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="theme-customizer-actions">
          <button onClick={onClose} className="btn-cancel">
            Cancelar
          </button>
          <button onClick={handleApply} className="btn-apply">
            Aplicar Tema
          </button>
        </div>
      </div>
    </div>
  )
}
