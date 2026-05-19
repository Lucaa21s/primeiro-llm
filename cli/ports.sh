#!/bin/bash

echo ""
echo "PORTAS EM USO"
echo ""

lsof -i :3000
lsof -i :3001
lsof -i :8000
lsof -i :11434
