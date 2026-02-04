import requests

try:
    r = requests.post('http://127.0.0.1:8000/chat', json={'query': 'dame juegos de rol'}, timeout=5)
    games = len(r.json()['retrieved_games'])
    print(f'✅ Servidor OK - Encontrados: {games} juegos de rol')
except Exception as e:
    print(f'❌ Error: {e}')
