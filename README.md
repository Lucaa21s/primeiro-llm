# Primeiro LLM

Infraestrutura moderna de IA local com:

- Ollama
- Llama3
- Mistral
- FastAPI
- Next.js
- PostgreSQL
- pgvector
- ChromaDB
- RAG
- Multi Agents
- Streaming
- Memória IA
- Upload PDF
- MCP Tools

## Stack

- Python 3.14
- Node.js 24
- pnpm
- WSL2 Ubuntu
- CUDA 13
- RTX 3060

## Executar backend

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

## 📦 ESTRATÉGIA DO `.gitignore`

### O que NÃO é enviado (Bloqueado)
```
❌ .venv/               ← Ambiente virtual INSTALADO
❌ node_modules/        ← Dependências Node INSTALADAS
❌ __pycache__/         ← Cache Python compilado
❌ *.sqlite3, *.db      ← Dados do banco (acumulam)
❌ uploads/             ← Arquivos do usuário carregados
❌ *.bin, *.gguf        ← Modelos IA compilados (muito grandes)
❌ data/chroma/         ← Vector store acumulado
❌ .next/, dist/        ← Build compilados
```

### O que É enviado (Configurações)
```
✅ requirements.txt                ← Dependências Python
✅ backend/requirements.txt         ← Dependências backend específicas
✅ package.json, pnpm-lock.yaml    ← Dependências Node
✅ init_db.py, database.py         ← Configuração do banco
✅ models.py                        ← Esquema de dados
✅ docker-compose.yml              ← Orquestração containers
✅ .env.example                     ← Template de variáveis
✅ Todos os arquivos .py, .ts, .tsx← Código-fonte
✅ .gitignore com documentação     ← Configuração git
```

## 🏗️ ARQUITETURA REAL - O QUE VAI SUBIR

```
primeiro-llm/ (GitHub)
│
├── 📄 README.md, LICENSE, .gitignore
├── 📄 requirements.txt (Python root)
├── 📄 docker-compose.yml
│
├── 📁 backend/
│   ├── 📄 requirements.txt ✅
│   ├── 📄 main.py ✅
│   ├── 📄 init_db.py ✅
│   ├── 📄 database.py ✅
│   ├── 📄 models.py ✅
│   ├── 📄 auth.py ✅
│   ├── 📁 agents/ (✅ .py files)
│   ├── 📁 agi/ (✅ .py files)
│   ├── 📁 autonomous/ (✅ .py files)
│   ├── 📁 civilization/ (✅ .py files)
│   ├── 📁 distributed/ (✅ .py files)
│   ├── 📁 rag_db/ (.gitkeep - pasta vazia para reconstrução)
│   ├── 📁 uploads/ (❌ .gitignore)
│   └── ❌ .venv/ (não sobe)
│
├── 📁 frontend/
│   ├── 📄 package.json ✅
│   ├── 📄 pnpm-lock.yaml ✅
│   ├── 📄 tsconfig.json ✅
│   ├── 📄 next.config.ts ✅
│   ├── 📁 src/ (✅ .ts, .tsx files)
│   ├── 📁 public/ (✅ assets)
│   └── ❌ node_modules/ (não sobe)
│
├── 📁 scripts/
│   ├── 📄 *.py ✅
│   └── 📄 *.sh ✅
│
├── 📁 deployment/
│   ├── 📁 docker/ ✅
│   ├── 📁 kubernetes/ ✅
│   ├── 📁 nginx/ ✅
│   └── 📁 scripts/ ✅
│
└── 📁 notebooks/ (✅ documentação)
```

## 🚀 QUICK START (Clone & Setup)

```bash
# 1. Clonar repositório
git clone https://github.com/Lucaa21s/primeiro-llm
cd primeiro-llm

# 2. Instalar dependências Python
pip install -r requirements.txt
pip install -r backend/requirements.txt

# 3. Instalar dependências Node
npm install
# ou
pnpm install

# 4. Configurar banco de dados
python backend/init_db.py

# 5. Executar backend
cd backend
source .venv/bin/activate
uvicorn main:app --reload

# 6. Em outro terminal, executar frontend
cd frontend
npm run dev
```

Pronto! Sistema 100% funcional sem nenhum arquivo de dados ou instalações pré-compiladas.

