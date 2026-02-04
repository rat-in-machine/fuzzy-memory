"""
Test de diagnóstico para entender la request al endpoint
"""

import json
import requests
import sys
from pathlib import Path
from uuid import uuid4

# Parámetros del endpoint
API_ENDPOINT = "https://ia-research-dev.codingbuddy-4282826dce7d155229a320302e775459-0000.eu-de.containers.appdomain.cloud/research/llm/stream/openai/clients"
API_KEY = "ips-dev-Imxp8Q2YtcJaReoSytJFbMnzgFmGF9W7"
MODEL = "gpt-4o"

print("\n" + "="*70)
print("DIAGNÓSTICO: Formato de Request a CodingBuddy")
print("="*70)

print(f"\nEndpoint: {API_ENDPOINT}")
print(f"Modelo: {MODEL}")
print(f"API Key: {API_KEY[:20]}...")

# Formato 1: Igual al ejemplo (data + body_str como string)
print("\n" + "-"*70)
print("Intento 1: Formato body_str (como en ejemplo)")
print("-"*70)

body_dict = {
    "model": MODEL,
    "uuid": str(uuid4()),
    "message": {
        "role": "user",
        "content": "¿Qué es RPG?"
    },
    "temperature": 0.7,
    "language": "es",
    "user": "@research.com"
}

body_str = json.dumps(body_dict, ensure_ascii=False)

print(f"Body string:\n{body_str}\n")

data = {"body_str": body_str}

headers = {
    "X-API-KEY": API_KEY
}

try:
    print("Enviando request con data...")
    response = requests.post(
        API_ENDPOINT,
        headers=headers,
        data=data,
        stream=True,
        timeout=10
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Error: {response.text[:200]}")
    else:
        print("✅ ÉXITO!")
        chunk = response.iter_content(chunk_size=64).__next__()
        print(f"Primera respuesta: {chunk[:100]}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Formato 2: JSON directo en lugar de data
print("\n" + "-"*70)
print("Intento 2: JSON directo (json parameter)")
print("-"*70)

try:
    print("Enviando request con json...")
    response = requests.post(
        API_ENDPOINT,
        headers={**headers, "Content-Type": "application/json"},
        json=body_dict,
        stream=True,
        timeout=10
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Error: {response.text[:200]}")
    else:
        print("✅ ÉXITO!")
        chunk = response.iter_content(chunk_size=64).__next__()
        print(f"Primera respuesta: {chunk[:100]}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Formato 3: Con message como objeto
print("\n" + "-"*70)
print("Intento 3: Message como objeto (probando variación)")
print("-"*70)

try:
    print("Enviando request con variación...")
    
    body_dict_var = {
        "model": MODEL,
        "uuid": str(uuid4()),
        "message": {"role": "user", "content": "¿Qué es RPG?"},
        "temperature": 0.7,
        "language": "es",
        "user": "@research.com"
    }
    
    body_str_var = json.dumps(body_dict_var, ensure_ascii=False)
    data_var = {"body_str": body_str_var}
    
    response = requests.post(
        API_ENDPOINT,
        headers=headers,
        data=data_var,
        timeout=10
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Error: {response.text[:300]}")
    else:
        print("✅ ÉXITO!")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*70)
