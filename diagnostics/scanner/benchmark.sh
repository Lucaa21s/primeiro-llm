#!/usr/bin/env bash

ROOT=~/IA/primeiro-llm
OUT=$ROOT/diagnostics/benchmarks

echo "GPU" > $OUT/gpu.txt
nvidia-smi >> $OUT/gpu.txt

echo "" >> $OUT/gpu.txt

echo "OLLAMA TEST" > $OUT/inference.txt

time ollama run llama3 "Explique IA em uma frase." \
>> $OUT/inference.txt

echo "Benchmark finalizado."
