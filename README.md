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

graph LR
    A["🔗 GitHub<br/>primeiro-llm"] -->|git clone| B["📥 Local<br/>Repo Clone"]
    
    B -->|pip install| C["🐍 Python<br/>Environment"]
    B -->|npm install| D["⚛️ Node<br/>Modules"]
    
    C -->|init_db.py| E["🗄️ Database<br/>Criado"]
    D -->|next build| F["⚙️ Frontend<br/>Build"]
    
    E --> G["✅ Sistema<br/>Pronto!"]
    F --> G
    
    H["❌ NÃO desce<br/>do GitHub:<br/>.venv/<br/>node_modules/<br/>*.db"] -.->|localmente criado| C
    H -.->|localmente criado| D
    
    style A fill:#4CAF50,color:#fff
    style G fill:#4CAF50,color:#fff
    style H fill:#f44336,color:#fff
    style C fill:#2196F3,color:#fff
    style D fill:#2196F3,color:#fff
    style E fill:#FF9800,color:#fff
    style F fill:#FF9800,color:#fff

    graph TD
    A["📦 GitHub Repository<br/>primeiro-llm"] --> B["📄 Configuração"]
    A --> C["🐍 Backend"]
    A --> D["⚛️ Frontend"]
    A --> E["🛠️ Deployment"]
    A --> F["📚 Scripts"]
    
    B --> B1["✅ .gitignore"]
    B --> B2["✅ docker-compose.yml"]
    B --> B3["✅ README.md"]
    
    C --> C1["✅ requirements.txt"]
    C --> C2["✅ main.py, init_db.py"]
    C --> C3["✅ agents/, agi/, autonomous/"]
    C --> C4["✅ models.py, database.py"]
    C --> C5["❌ .venv/ bloqueado"]
    C --> C6["❌ *.sqlite3 bloqueado"]
    
    D --> D1["✅ package.json"]
    D --> D2["✅ src/, components/"]
    D --> D3["✅ next.config.ts"]
    D --> D4["❌ node_modules/ bloqueado"]
    
    E --> E1["✅ docker/"]
    E --> E2["✅ kubernetes/"]
    E --> E3["✅ nginx/"]
    
    F --> F1["✅ *.py scripts"]
    F --> F2["✅ *.sh scripts"]
    
    style A fill:#4CAF50,color:#fff
    style C5 fill:#f44336,color:#fff
    style C6 fill:#f44336,color:#fff
    style D4 fill:#f44336,color:#fff
    style B1 fill:#2196F3,color:#fff
    style B2 fill:#2196F3,color:#fff
    style C1 fill:#2196F3,color:#fff
    style D1 fill:#2196F3,color:#fff