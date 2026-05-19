#!/bin/bash

echo "Iniciando frontend..."

pkill -f next

cd ~/IA/primeiro-llm/frontend

nohup pnpm dev > frontend.log 2>&1 &
