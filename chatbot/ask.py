import requests
import json
import sys

if len(sys.argv) < 2:
    print("Uso: python ask.py <pregunta>")
    print()
    print("Ejemplos:")
    print('  python ask.py "dame juegos de rol"')
    print('  python ask.py "precio de elden ring"')
    print('  python ask.py "juegos de aventura"')
    sys.exit(1)

query = " ".join(sys.argv[1:])

try:
    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"query": query},
        timeout=5
    )
    
    data = response.json()
    print(f"\n{data['response']}\n")
    
except Exception as e:
    print(f"Error: {e}")
