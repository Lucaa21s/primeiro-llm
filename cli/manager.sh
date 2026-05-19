#!/bin/bash

clear

while true
do
    echo "==============================="
    echo " PRIMEIRO-LLM PLATFORM MANAGER "
    echo "==============================="
    echo ""
    echo "1 - Start Backend"
    echo "2 - Start Frontend"
    echo "3 - Start Full Stack"
    echo "4 - Restart Everything"
    echo "5 - Stop Everything"
    echo "6 - Health Check"
    echo "7 - View Ports"
    echo "8 - Ollama Status"
    echo "9 - GPU Status"
    echo "10 - Clean Cache"
    echo "11 - Exit"
    echo ""

    read -p "Escolha: " option

    case $option in

        1)
            bash cli/start_backend.sh
            ;;

        2)
            bash cli/start_frontend.sh
            ;;

        3)
            bash cli/start_full.sh
            ;;

        4)
            bash cli/restart.sh
            ;;

        5)
            bash cli/stop.sh
            ;;

        6)
            bash cli/health.sh
            ;;

        7)
            bash cli/ports.sh
            ;;

        8)
            bash cli/ollama.sh
            ;;

        9)
            bash cli/gpu.sh
            ;;

        10)
            bash cli/cleanup.sh
            ;;

        11)
            exit
            ;;

        *)
            echo "Opção inválida"
            ;;
    esac

    echo ""
    read -p "Pressione ENTER para continuar..."
    clear

done
