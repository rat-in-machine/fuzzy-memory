"""
Test diagnóstico 2: Probar con diferentes usuarios
"""

import json
import requests
from uuid import uuid4

API_ENDPOINT = "https://ia-research-dev.codingbuddy-4282826dce7d155229a320302e775459-0000.eu-de.containers.appdomain.cloud/research/llm/stream/openai/clients"
API_KEY = "ips-dev-Imxp8Q2YtcJaReoSytJFbMnzgFmGF9W7"
MODEL = "gpt-4o"

print("\n" + "="*70)
print("DIAGNOSTICO 2: Probando diferentes formatos de usuario")
print("="*70)

# Diferentes variaciones de usuario
users_to_test = [
    "@research.com",
    "ismael@research.com",
    "user@research.com",
    "test@research.com",
    "ia@research.com",
    "bot",
    "chatbot",
    ""
]

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

for user_email in users_to_test:
    print(f"\n{'-'*70}")
    print(f"Probando usuario: '{user_email}'")
    print('-'*70)
    
    body_dict = {
        "model": MODEL,
        "uuid": str(uuid4()),
        "message": {
            "role": "user",
            "content": "Hola"
        },
        "temperature": 0.7,
        "language": "es",
        "user": user_email
    }
    
    try:
        response = requests.post(
            API_ENDPOINT,
            headers=headers,
            json=body_dict,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        try:
            error_detail = response.json().get("detail", response.text[:100])
            print(f"Respuesta: {error_detail}")
        except:
            print(f"Respuesta: {response.text[:100]}")
        
        if response.status_code == 200:
            print("SUCCESS!")
            break
            
    except Exception as e:
        print(f"Error: {str(e)[:100]}")

print("\n" + "="*70)
