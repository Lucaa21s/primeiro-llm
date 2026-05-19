#!/usr/bin/env bash

ROOT=~/IA/primeiro-llm
DATE=$(date +%Y-%m-%d_%H-%M-%S)

mkdir -p $ROOT/diagnostics/snapshots/$DATE

cp -r \
$ROOT/diagnostics/inventory \
$ROOT/diagnostics/reports \
$ROOT/diagnostics/scans \
$ROOT/diagnostics/benchmarks \
$ROOT/diagnostics/snapshots/$DATE/

echo "Snapshot criado:"
echo $DATE
