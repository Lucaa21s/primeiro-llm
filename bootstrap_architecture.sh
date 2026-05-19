#!/usr/bin/env bash

set -e

ROOT=~/IA/primeiro-llm
DIAG=$ROOT/diagnostics

echo "======================================="
echo "BOOTSTRAP AI ARCHITECTURE"
echo "======================================="

########################################
# ESTRUTURA
########################################

mkdir -p \
$DIAG/inventory \
$DIAG/logs \
$DIAG/reports \
$DIAG/scans \
$DIAG/benchmarks \
$DIAG/snapshots \
$DIAG/scanner

########################################
# INVENTORY.SH
########################################

cat > $DIAG/scanner/inventory.sh << 'SCRIPT'
#!/usr/bin/env bash

ROOT=~/IA/primeiro-llm
OUTPUT=$ROOT/diagnostics/inventory/system_inventory.md

echo "# SYSTEM INVENTORY" > "$OUTPUT"
echo "" >> "$OUTPUT"

########################################
# OS
########################################

echo "## OPERATING SYSTEM" >> "$OUTPUT"
echo '```' >> "$OUTPUT"

echo "User: $(whoami)" >> "$OUTPUT"
echo "Host: $(hostname)" >> "$OUTPUT"
echo "Kernel: $(uname -r)" >> "$OUTPUT"

grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '"' \
>> "$OUTPUT"

echo '```' >> "$OUTPUT"
echo "" >> "$OUTPUT"

########################################
# HARDWARE
########################################

echo "## HARDWARE" >> "$OUTPUT"
echo '```' >> "$OUTPUT"

lscpu | grep "Model name" >> "$OUTPUT"

echo "" >> "$OUTPUT"

free -h | grep Mem >> "$OUTPUT"

echo '```' >> "$OUTPUT"
echo "" >> "$OUTPUT"

########################################
# NVIDIA
########################################

echo "## NVIDIA / CUDA" >> "$OUTPUT"
echo '```' >> "$OUTPUT"

nvidia-smi \
--query-gpu=name,driver_version,memory.total \
--format=csv,noheader \
2>/dev/null \
>> "$OUTPUT"

echo "" >> "$OUTPUT"

nvcc --version 2>/dev/null | tail -n 1 \
>> "$OUTPUT"

echo '```' >> "$OUTPUT"
echo "" >> "$OUTPUT"

########################################
# PYTHON
########################################

echo "## PYTHON STACK" >> "$OUTPUT"
echo '```' >> "$OUTPUT"

echo "Python: $(python --version 2>&1)" >> "$OUTPUT"
echo "Pip: $(pip --version 2>&1)" >> "$OUTPUT"

uv --version 2>/dev/null >> "$OUTPUT"

echo "" >> "$OUTPUT"

pip list 2>/dev/null | grep -E \
"torch|transformers|ollama|chromadb|sentence|langchain|openai|fastapi|uvicorn|numpy|pandas|matplotlib|jupyter" \
>> "$OUTPUT"

echo '```' >> "$OUTPUT"
echo "" >> "$OUTPUT"

########################################
# NODE
########################################

echo "## NODE STACK" >> "$OUTPUT"
echo '```' >> "$OUTPUT"

echo "Node: $(node -v 2>&1)" >> "$OUTPUT"
echo "NPM: $(npm -v 2>&1)" >> "$OUTPUT"
echo "PNPM: $(pnpm -v 2>&1)" >> "$OUTPUT"
echo "BUN: $(bun --version 2>&1)" >> "$OUTPUT"

echo '```' >> "$OUTPUT"
echo "" >> "$OUTPUT"

########################################
# FRONTEND
########################################

echo "## FRONTEND STACK" >> "$OUTPUT"
echo '```' >> "$OUTPUT"

cd ~/IA/primeiro-llm/frontend 2>/dev/null || true

pnpm list --depth 0 2>/dev/null | grep -E \
"next|react|tailwind|axios|markdown|lucide|shadcn" \
>> "$OUTPUT"

echo '```' >> "$OUTPUT"
echo "" >> "$OUTPUT"

########################################
# OLLAMA
########################################

echo "## OLLAMA" >> "$OUTPUT"
echo '```' >> "$OUTPUT"

ollama --version 2>/dev/null >> "$OUTPUT"

echo "" >> "$OUTPUT"

ollama list 2>/dev/null >> "$OUTPUT"

echo '```' >> "$OUTPUT"
echo "" >> "$OUTPUT"

########################################
# SERVICES
########################################

echo "## RUNNING SERVICES" >> "$OUTPUT"
echo '```' >> "$OUTPUT"

ps aux | grep -E \
"ollama|uvicorn|next-server|node" \
| grep -v grep \
>> "$OUTPUT"

echo '```' >> "$OUTPUT"
echo "" >> "$OUTPUT"

########################################
# GIT
########################################

echo "## GIT" >> "$OUTPUT"
echo '```' >> "$OUTPUT"

cd ~/IA/primeiro-llm

echo "Branch:" >> "$OUTPUT"
git branch --show-current >> "$OUTPUT"

echo "" >> "$OUTPUT"

echo "Remote:" >> "$OUTPUT"
git remote -v >> "$OUTPUT"

echo '```' >> "$OUTPUT"

echo "Inventory gerado em:"
echo "$OUTPUT"
SCRIPT

########################################
# PROJECT_SCAN.SH
########################################

cat > $DIAG/scanner/project_scan.sh << 'SCRIPT'
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
SCRIPT

########################################
# BENCHMARK.SH
########################################

cat > $DIAG/scanner/benchmark.sh << 'SCRIPT'
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
SCRIPT

########################################
# SNAPSHOT.SH
########################################

cat > $DIAG/scanner/snapshot.sh << 'SCRIPT'
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
SCRIPT

########################################
# CLEANUP.SH
########################################

cat > $DIAG/scanner/cleanup.sh << 'SCRIPT'
#!/usr/bin/env bash

ROOT=~/IA/primeiro-llm

find $ROOT -type d -name "__pycache__" -exec rm -rf {} +
find $ROOT -type f -name "*.pyc" -delete
find $ROOT -type f -name "*.log" -size +50M -delete

echo "Cleanup finalizado."
SCRIPT

########################################
# PERMISSÕES
########################################

chmod +x $DIAG/scanner/*.sh

########################################
# EXECUÇÃO
########################################

echo ""
echo "Executando scanners..."
echo ""

bash $DIAG/scanner/inventory.sh
bash $DIAG/scanner/project_scan.sh
bash $DIAG/scanner/benchmark.sh

echo ""
echo "======================================="
echo "ARQUITETURA IMPLEMENTADA"
echo "======================================="
echo ""
echo "Estrutura criada em:"
echo "$DIAG"
echo ""
echo "Scanners disponíveis:"
echo ""
echo "inventory.sh"
echo "project_scan.sh"
echo "benchmark.sh"
echo "snapshot.sh"
echo "cleanup.sh"

