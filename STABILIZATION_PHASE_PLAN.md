# Fase de Estabilização — Diagnóstico e Próxima Tarefa

## Diagnóstico rápido da base

1. **Imports inconsistentes e quebrados (backend)**
   - Há mistura de imports de raiz (`agents.*`, `workflows.*`) com imports package-aware (`app.*`).
   - Isso causa `ModuleNotFoundError` dependendo de como a API é inicializada (`python main.py` vs `uvicorn ...`).

2. **Backend acoplado em `main.py`**
   - `main.py` concentra rotas, orquestração de IA, ingestão de PDF e infra distribuída.
   - Alto risco de regressão por efeito colateral entre módulos.

3. **Frontend sem camada de integração explícita com backend**
   - Tendência a chamadas HTTP dispersas em componentes.
   - Dificulta tratamento centralizado de erro/retry/timeouts.

4. **Ausência de service layer consolidada**
   - Regras de negócio estão parcialmente em rotas e parcialmente em módulos utilitários.
   - Reduz testabilidade e previsibilidade.

5. **Código experimental misturado com core**
   - Diretórios como `civilization/`, `interplanetary/`, `agi/` e `self_improving/` convivem com fluxo principal.
   - Eleva ruído arquitetural e risco operacional.

6. **Testes insuficientes para rotas críticas**
   - Sem suíte mínima de smoke/integration para endpoints principais.

7. **Docker/infra ainda não padronizados**
   - Dependências de execução (Ollama, DB vetorial, workers) exigem composição reprodutível.

## Ordem de execução (confirmada)
1. corrigir imports
2. estabilizar backend
3. estabilizar frontend
4. criar service layer
5. separar `experimental/`
6. adicionar testes
7. dockerizar corretamente
8. postgres + pgvector
9. redis
10. celery/workers
11. observabilidade
12. CI/CD

## Tarefa proposta (erro prioritário para correção)

### Tarefa: padronizar imports para o namespace `app.*` no backend

**Erro alvo:** `ModuleNotFoundError` em imports de `agents` e `workflows` fora do namespace `app`.

**Critério de pronto:**
- Todos os imports internos do backend usam caminho canônico (`app.<módulo>` quando aplicável).
- `python -m py_compile` nos arquivos alterados passa sem erro.
- App sobe em modo dev sem erro de import.

**Resultado esperado:**
- Base previsível para a etapa 2 (estabilizar backend), removendo falha estrutural de boot.
