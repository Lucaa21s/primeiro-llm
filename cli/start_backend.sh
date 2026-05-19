#!/bin/bash

echo "Iniciando backend..."

pkill -f uvicorn

cd ~/IA/primeiro-llm/backend

source .venv/bin/activate

nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
