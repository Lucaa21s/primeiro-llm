#!/bin/bash

# ============================================================================
# Primeiro LLM - Frontend Enhancement Setup
# ============================================================================
# Este script prepara e inicia o frontend com todas as melhorias

echo "🚀 Iniciando Primeiro LLM Frontend v2.0 Enhanced..."
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não está instalado. Instale em: https://nodejs.org"
    exit 1
fi

# Check if npm or pnpm is installed
if ! command -v pnpm &> /dev/null; then
    if ! command -v npm &> /dev/null; then
        echo "❌ npm ou pnpm não está instalado."
        exit 1
    fi
    PACKAGE_MANAGER="npm"
else
    PACKAGE_MANAGER="pnpm"
fi

echo "📦 Gerenciador de pacotes: $PACKAGE_MANAGER"
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/frontend" || exit 1

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📥 Instalando dependências..."
    $PACKAGE_MANAGER install
    echo ""
fi

# Build if needed
if [ ! -d ".next" ]; then
    echo "🔨 Compilando aplicação..."
    $PACKAGE_MANAGER run build
    echo ""
fi

# Start development server
echo "✨ Inicializando servidor de desenvolvimento..."
echo ""
echo "🎨 Recursos Novos:"
echo "  ✅ Notificações Toast Animadas"
echo "  ✅ Atalhos de Teclado (Ctrl+N, Ctrl+K, Ctrl+Shift+T, etc)"
echo "  ✅ Busca de Histórico com Filtros"
echo "  ✅ Customização de Temas (5 temas predefinidos)"
echo "  ✅ Indicador Colaborativo em Tempo Real"
echo ""
echo "🌐 Acesse: http://localhost:3000"
echo "📚 Documentação: veja ENHANCEMENT_GUIDE.md"
echo ""

$PACKAGE_MANAGER run dev
