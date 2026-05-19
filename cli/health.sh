#!/bin/bash

echo ""
echo "=== BACKEND ==="

curl -s http://localhost:8000/

echo ""
echo ""
echo "=== FRONTEND ==="

curl -I http://localhost:3000
