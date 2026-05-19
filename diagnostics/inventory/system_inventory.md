# SYSTEM INVENTORY

## OPERATING SYSTEM
```
User: mmt
Host: Lucas
Kernel: 6.6.114.1-microsoft-standard-WSL2
Ubuntu 26.04 LTS
```

## HARDWARE
```
Model name:                              Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz

Mem:           7.8Gi       3.0Gi       1.5Gi        33Mi       3.5Gi       4.7Gi
```

## NVIDIA / CUDA
```
NVIDIA GeForce RTX 3060, 596.36, 12288 MiB

```

## PYTHON STACK
```
Python: /home/mmt/IA/primeiro-llm/diagnostics/scanner/inventory.sh: line 70: python: command not found
Pip: pip 25.1.1 from /usr/lib/python3/dist-packages/pip (python 3.14)
uv 0.11.14 (x86_64-unknown-linux-gnu)

chromadb                                 1.5.9
fastapi                                  0.136.1
numpy                                    2.4.5
ollama                                   0.6.2
sentence-transformers                    5.5.0
torch                                    2.12.0
transformers                             5.8.1
uvicorn                                  0.47.0
```

## NODE STACK
```
Node: v24.15.0
NPM: 11.12.1
PNPM: 11.1.2
BUN: 1.3.14
```

## FRONTEND STACK
```
├── axios@1.16.1
├── lucide-react@1.16.0
├── next@16.2.6
├── react@19.2.4
├── react-dom@19.2.4
├── react-markdown@10.1.0
├── react-syntax-highlighter@16.1.1
├── shadcn@4.7.0
├── tailwind-merge@3.6.0
├── @tailwindcss/postcss@4.3.0
├── @types/react@19.2.14
├── @types/react-dom@19.2.3
├── @types/react-syntax-highlighter@15.5.13
├── eslint-config-next@16.2.6
├── tailwindcss@4.3.0
```

## OLLAMA
```
ollama version is 0.24.0

NAME                       ID              SIZE      MODIFIED     
gemma4:31b                 6316f0629137    19 GB     23 hours ago    
gemma2:9b                  ff02c3702f32    5.4 GB    23 hours ago    
nomic-embed-text:latest    0a109f422b47    274 MB    32 hours ago    
llama3:latest              365c0bd3c000    4.7 GB    2 days ago      
mistral:latest             6577803aa9a0    4.4 GB    2 days ago      
```

## RUNNING SERVICES
```
ollama     127  0.0  1.2 2264120 100684 ?      Ssl  16:20   0:10 /usr/local/bin/ollama serve
mmt       1358  0.1  1.6 11925412 132460 pts/2 Sl+  16:25   0:32 /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/node /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/out/server-main.js --host=127.0.0.1 --port=0 --connection-token=3101051879-1315853121-3707927806-892141436 --use-host-proxy --without-browser-env-var --disable-websocket-compression --accept-server-license-terms --telemetry-level=all
mmt       1372  0.0  0.5 1025736 40864 pts/3   Ssl+ 16:25   0:05 /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/node -e const net = require('net'); process.stdin.pause(); const client = net.createConnection({ host: '127.0.0.1', port: 46523 }, () => { client.pipe(process.stdout); process.stdin.pipe(client); }); client.on('close', function (hadError) { console.error(hadError ? 'Remote close with error' : 'Remote close'); process.exit(hadError ? 1 : 0); }); client.on('error', function (err) { process.stderr.write(err && (err.stack || err.message) || String(err)); });
mmt       1381  0.0  0.4 1024128 39264 pts/4   Ssl+ 16:25   0:12 /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/node -e const net = require('net'); process.stdin.pause(); const client = net.createConnection({ host: '127.0.0.1', port: 46523 }, () => { client.pipe(process.stdout); process.stdin.pipe(client); }); client.on('close', function (hadError) { console.error(hadError ? 'Remote close with error' : 'Remote close'); process.exit(hadError ? 1 : 0); }); client.on('error', function (err) { process.stderr.write(err && (err.stack || err.message) || String(err)); });
mmt       1389  0.0  1.0 1462504 85252 pts/2   Sl+  16:25   0:11 /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/node /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/out/bootstrap-fork --type=fileWatcher
mmt       1762  4.4  8.1 55709388 659512 pts/2 Sl+  16:25  13:51 /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/node --dns-result-order=ipv4first /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/out/bootstrap-fork --type=extensionHost --transformURIs --useHostProxy=true
mmt       1843  0.1  0.6 1167912 53368 pts/2   Sl+  16:25   0:36 /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/node /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/out/bootstrap-fork --type=ptyHost --logsPath /home/mmt/.vscode-server/data/logs/20260518T162529
mmt       1867  0.0  0.2 1015816 19760 pts/5   Sl+  16:25   0:00 /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/node /home/mmt/.vscode-remote-containers/dist/vscode-remote-containers-server-0.459.0.js
mmt       3207  0.0  0.3 1094696 30516 pts/2   Sl+  16:25   0:01 /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/node /home/mmt/.vscode-server/extensions/ms-azuretools.vscode-containers-2.4.4/dist/dockerfile-language-server-nodejs/lib/server.js --node-ipc --node-ipc --clientProcessId=1762
mmt       3213  0.0  0.3 1021260 29288 pts/2   Sl+  16:25   0:01 /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/node /home/mmt/.vscode-server/extensions/ms-azuretools.vscode-containers-2.4.4/dist/compose-language-service/lib/server.js --node-ipc --node-ipc --clientProcessId=1762
mmt       3968  0.3  2.5 1479500 210424 pts/2  Sl+  16:25   1:00 /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/node /home/mmt/.vscode-server/extensions/streetsidesoftware.code-spell-checker-4.5.6/packages/_server/dist/main.cjs --node-ipc --clientProcessId=1762
mmt       4194  0.5  9.0 23997304 736308 pts/2 Sl+  16:25   1:34 /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/node /home/mmt/.vscode-server/extensions/ms-python.vscode-pylance-2026.2.1/dist/server.bundle.js --cancellationReceive=file:e7bb398a293cb00fa44fe3507c64b0f5c5f573bcae --node-ipc --clientProcessId=1762
mmt       4200  0.0  0.5 1105788 48480 pts/2   Sl+  16:25   0:03 /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/node /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/extensions/json-language-features/server/dist/node/jsonServerMain --node-ipc --clientProcessId=1762
mmt      52884  0.0  0.6 1098296 52696 pts/2   Sl+  20:13   0:02 /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/node /home/mmt/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/extensions/markdown-language-features/dist/serverWorkerMain --node-ipc --clientProcessId=1762
```

## GIT
```
Branch:
main

Remote:
origin	git@github.com:Lucaa21s/primeiro-llm.git (fetch)
origin	git@github.com:Lucaa21s/primeiro-llm.git (push)
```
