import urllib.request
import json

url = "http://localhost:8000/evolve"
data = {
    "messages": [
        {"role": "user", "content": "Explique computação quântica de forma simples."}
    ]
}

headers = {"Content-Type": "application/json"}
req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers)

print("🚀 Enviando requisição segura para o Evolution Manager...")
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
        print("\n✅ RESPOSTA DA IA RECEBIDA COM SUCESSO:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"\n❌ Erro ao conectar na API: {e}")
