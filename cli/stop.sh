#!/bin/bash

echo "Parando serviços..."

pkill -f uvicorn
pkill -f next
pkill -f ollama

echo "Serviços parados"
