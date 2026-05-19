#!/bin/bash

echo "Limpando cache..."

find . -type d -name "__pycache__" -exec rm -rf {} +

find . -type d -name ".next" -exec rm -rf {} +

find . -type d -name ".turbo" -exec rm -rf {} +

echo "Limpeza concluída"
