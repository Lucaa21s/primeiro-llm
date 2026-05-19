#!/usr/bin/env bash

ROOT=~/IA/primeiro-llm
SCAN=$ROOT/diagnostics/scans

tree -L 4 $ROOT > $SCAN/tree.txt

find $ROOT \
-type f \
-not -path "*/node_modules/*" \
-not -path "*/.git/*" \
> $SCAN/files.txt

du -sh $ROOT/* 2>/dev/null \
> $SCAN/storage.txt

echo "Project scan finalizado."
