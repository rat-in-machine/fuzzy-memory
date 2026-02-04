# Chatbot RAG - Recomendador de Videojuegos

## Descripción
Chatbot basado en RAG (Retrieval-Augmented Generation) que recomienda videojuegos basándose en preferencias del usuario en lenguaje natural.

## Arquitectura

### Componentes principales:

1. **Ingestion Pipeline** (`src/ingestion/`)
   - Obtención de datos de Steam API
   - Obtención de precios de GG.deals API
   - Normalización y validación de datos
   - Almacenamiento en BD interna

2. **Embeddings** (`src/embeddings/`)
   - Generación de embeddings de descripciones de juegos
   - Vectorización de géneros y tags
   - Almacenamiento en base vectorial (FAISS/ChromaDB)

3. **Retrieval** (`src/retrieval/`)
   - Búsqueda semántica por similitud
   - Filtrado por géneros y preferencias
   - Ranking y reordenamiento

4. **LLM Chain** (`src/llm/`)
   - Prompts estructurados para recomendación
   - Integración con OpenAI/Anthropic
   - Generación de explicaciones
   - Validación de respuestas (no inventar datos)

5. **API REST** (`src/api/`)
   - Endpoints para chat
   - Gestión de sesiones de conversación
   - Historial de recomendaciones

## Stack Tecnológico

- **Framework**: LangChain / LlamaIndex
- **LLM**: OpenAI GPT-4 / Claude
- **Vector Store**: FAISS / ChromaDB
- **API**: FastAPI
- **Embeddings**: OpenAI text-embedding-3-small / sentence-transformers
- **BD**: MongoDB (datos estructurados)

## Flujo de trabajo

```
Usuario → Query en lenguaje natural
    ↓
Retrieval → Búsqueda vectorial en BD interna
    ↓
Context → Top-K juegos relevantes
    ↓
LLM → Generación de recomendación + explicación
    ↓
Respuesta → Justificada y basada en datos reales
```

## Restricciones
- ❌ No inventa juegos ni precios
- ❌ No accede en tiempo real a APIs externas
- ✅ Solo responde con información de la BD interna
- ✅ Explica el por qué de cada recomendación
- ✅ Atribuye fuentes (Steam, GG.deals)

## Instalación

```bash
cd chatbot
pip install -r requirements.txt
cp .env.example .env
# Configurar variables de entorno
```

## Uso

```bash
# Ingesta de datos (ejecutar una vez)
python -m src.ingestion.pipeline

# Generar embeddings
python -m src.embeddings.vectorizer

# Iniciar API
python -m src.api.main
```
