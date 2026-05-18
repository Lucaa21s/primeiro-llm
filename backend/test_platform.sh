#!/bin/bash
echo "=== DISPARANDO TESTE DE PRODUÇÃO VIA PORTA DO BACKEND (8000) ==="
curl -X POST "http://127.0.0" \
     -H "Content-Type: application/json" \
     -d '{"messages": [{"role": "user", "content": "Explique de forma simples o que é computação quântica."}]}'

echo -e "\n\n=== DISPARANDO TESTE DE PRODUÇÃO VIA PROXY REVERSO NGINX (8080) ==="
curl -X POST "http://127.0.0" \
     -H "Content-Type: application/json" \
     -d '{"messages": [{"role": "user", "content": "Explique de forma simples o que é computação quântica."}]}'
