"""
Test rápido de conectividad LLM con endpoint CodingBuddy
"""

import sys
from pathlib import Path

# Añadir rutas
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.llm.client import LLMStreamingClient
from config.settings import settings

print("\n" + "="*70)
print("TEST RÁPIDO: Conectividad LLM con CodingBuddy")
print("="*70)

print(f"\n📝 Configuración:")
print(f"   API Endpoint: {settings.llm_api_endpoint}")
print(f"   Modelo: {settings.llm_model}")
print(f"   API Key configurada: {'SÍ' if settings.llm_api_key else 'NO'}")
print(f"   Temperatura: {settings.llm_temperature}")
print(f"   Max Tokens: {settings.llm_max_tokens}")

print(f"\n🚀 Iniciando streaming...")
print("-"*70)

try:
    client = LLMStreamingClient(
        api_endpoint=settings.llm_api_endpoint,
        api_key=settings.llm_api_key,
        model=settings.llm_model
    )
    
    # Test simple
    response = ""
    chunk_count = 0
    
    for chunk in client.stream(
        message="¿Qué es un RPG en videojuegos? Responde en una sola línea.",
        temperature=0.5,
        language="es"
    ):
        response += chunk
        chunk_count += 1
        print(chunk, end="", flush=True)
    
    print("\n" + "-"*70)
    print(f"\n✅ ÉXITO!")
    print(f"   Chunks recibidos: {chunk_count}")
    print(f"   Caracteres totales: {len(response)}")
    print(f"   Respuesta completada: {'Sí' if len(response) > 0 else 'No'}")
    print("\n🎉 Sistema LLM operacional - Listo para producción\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)
