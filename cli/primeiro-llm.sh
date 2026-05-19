#!/bin/bash

PROJECT=~/IA/primeiro-llm

clear

show_menu() {
    echo "========================================="
    echo "      PRIMEIRO-LLM CONTROL PANEL"
    echo "========================================="
    echo ""
    echo "1  - Iniciar sistema"
    echo "2  - Parar sistema"
    echo "3  - Reiniciar sistema"
    echo "4  - Status sistema"
    echo "5  - Logs backend"
    echo "6  - Logs frontend"
    echo "7  - Logs ollama"
    echo "8  - Verificar GPU"
    echo "9  - Verificar portas"
    echo "10 - Atualizar backend"
    echo "11 - Atualizar frontend"
    echo "12 - Limpar cache"
    echo "13 - Verificar Ollama"
    echo "14 - Verificar PostgreSQL"
    echo "15 - Abrir projeto VSCode"
    echo "16 - Git status"
    echo "17 - Git push"
    echo "18 - Rodar testes"
    echo "19 - Reiniciar apenas backend"
    echo "20 - Reiniciar apenas frontend"
    echo ""
    echo "0  - Sair"
    echo ""
}

start_system() {

    echo "Iniciando sistema..."

    mkdir -p $PROJECT/logs

    # FRONTEND
    cd $PROJECT/frontend

    pkill -f "next dev" || true

    nohup pnpm dev > $PROJECT/logs/frontend.log 2>&1 &

    # BACKEND
    cd $PROJECT/backend

    source .venv/bin/activate

    pkill -f "uvicorn" || true

    nohup uvicorn app.main:app \
        --reload \
        --host 0.0.0.0 \
        --port 8000 \
        > $PROJECT/logs/backend.log 2>&1 &

    # OLLAMA
    pkill -f "ollama serve" || true

    nohup ollama serve > $PROJECT/logs/ollama.log 2>&1 &

    echo ""
    echo "Sistema iniciado"
    echo ""
    echo "Frontend -> http://localhost:3000"
    echo "Backend  -> http://localhost:8000"
}

stop_system() {

    echo "Parando sistema..."

    pkill -f "next dev" || true
    pkill -f "uvicorn" || true
    pkill -f "ollama serve" || true

    echo "Sistema parado"
}

restart_system() {

    stop_system

    sleep 3

    start_system
}

system_status() {

    echo ""
    echo "========= STATUS ========="
    echo ""

    echo "NEXT:"
    ps aux | grep "next dev" | grep -v grep

    echo ""
    echo "UVICORN:"
    ps aux | grep "uvicorn" | grep -v grep

    echo ""
    echo "OLLAMA:"
    ps aux | grep "ollama" | grep -v grep

    echo ""
    echo "PORTAS:"
    lsof -i :3000
    lsof -i :8000
    lsof -i :11434
}

logs_backend() {
    tail -f $PROJECT/logs/backend.log
}

logs_frontend() {
    tail -f $PROJECT/logs/frontend.log
}

logs_ollama() {
    tail -f $PROJECT/logs/ollama.log
}

gpu_status() {

    echo ""
    nvidia-smi
}

check_ports() {

    echo ""
    lsof -i :3000
    lsof -i :8000
    lsof -i :11434
    lsof -i :5432
}

update_backend() {

    cd $PROJECT/backend

    source .venv/bin/activate

    uv pip install -U -r requirements.txt
}

update_frontend() {

    cd $PROJECT/frontend

    pnpm update
}

clean_cache() {

    echo "Limpando cache..."

    find $PROJECT -type d -name "__pycache__" -exec rm -rf {} +

    rm -rf $PROJECT/frontend/.next

    echo "Cache limpo"
}

check_ollama() {

    ollama list
}

check_postgres() {

    docker ps | grep postgres
}

open_vscode() {

    code $PROJECT
}

git_status() {

    cd $PROJECT

    git status
}

git_push() {

    cd $PROJECT

    git add .

    read -p "Mensagem commit: " msg

    git commit -m "$msg"

    git push origin main
}

run_tests() {

    cd $PROJECT/backend

    source .venv/bin/activate

    pytest
}

restart_backend() {

    pkill -f "uvicorn" || true

    cd $PROJECT/backend

    source .venv/bin/activate

    nohup uvicorn app.main:app \
        --reload \
        --host 0.0.0.0 \
        --port 8000 \
        > $PROJECT/logs/backend.log 2>&1 &
}

restart_frontend() {

    pkill -f "next dev" || true

    cd $PROJECT/frontend

    nohup pnpm dev > $PROJECT/logs/frontend.log 2>&1 &
}

while true; do

    show_menu

    read -p "Escolha: " option

    case $option in

        1) start_system ;;
        2) stop_system ;;
        3) restart_system ;;
        4) system_status ;;
        5) logs_backend ;;
        6) logs_frontend ;;
        7) logs_ollama ;;
        8) gpu_status ;;
        9) check_ports ;;
        10) update_backend ;;
        11) update_frontend ;;
        12) clean_cache ;;
        13) check_ollama ;;
        14) check_postgres ;;
        15) open_vscode ;;
        16) git_status ;;
        17) git_push ;;
        18) run_tests ;;
        19) restart_backend ;;
        20) restart_frontend ;;
        0) exit ;;
        *) echo "Opção inválida" ;;

    esac

    echo ""
    read -p "ENTER para continuar..."

    clear

done
