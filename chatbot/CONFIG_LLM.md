"""
CONFIGURACIÓN DEL ENDPOINT LLM CODINGBUDDY

El endpoint de CodingBuddy requiere:
1. Usuario registrado en la plataforma
2. API Key válida
3. Estructura correcta de request JSON

PASOS PARA CONFIGURAR:
======================

1. REGISTRAR USUARIO EN CODINGBUDDY
   - Accede a https://ia-research-dev.codingbuddy.../admin
   - Crea un nuevo usuario (ej: ismael@viewnext.com)
   - Guarda las credenciales

2. OBTENER/CREAR API KEY
   - Desde el dashboard de CodingBuddy
   - Genera una nueva API key
   - Copia la key (ej: ips-dev-Imxp8Q2YtcJaReoSytJFbMnzgFmGF9W7)

3. ACTUALIZAR .env
   ```
   LLM_API_ENDPOINT=https://ia-research-dev.codingbuddy-..../research/llm/stream/openai/clients
   LLM_API_KEY=tu-api-key-aqui
   LLM_MODEL=gpt-4o
   LLM_USER_EMAIL=ismael@viewnext.com   <-- TU USUARIO
   ```

4. VERIFICAR CONEXIÓN
   ```bash
   cd chatbot
   python tests/test_llm_quick.py
   ```

ESTRUCTURA DEL REQUEST:
=======================

Content-Type: application/json
X-API-KEY: tu-api-key

{
    "model": "gpt-4o",
    "uuid": "uuid-de-sesion",
    "message": {
        "role": "user",
        "content": "Tu pregunta aquí"
    },
    "temperature": 0.7,
    "language": "es",
    "user": "tu-email-registrado@domain.com"
}

SOLUCIÓN ALTERNATIVA:
======================

Si prefieres no usar CodingBuddy:
1. Usa OpenAI API directamente (requiere openai_api_key)
2. Usa Tavily LLM (requiere tavily_api_key)

Actualiza src/llm/client.py para soportar otros proveedores.
"""

print(__doc__)
