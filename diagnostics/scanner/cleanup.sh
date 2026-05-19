#!/usr/bin/env bash

ROOT=~/IA/primeiro-llm

find $ROOT -type d -name "__pycache__" -exec rm -rf {} +
find $ROOT -type f -name "*.pyc" -delete
find $ROOT -type f -name "*.log" -size +50M -delete

echo "Cleanup finalizado."
