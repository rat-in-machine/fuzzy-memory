# Chatbot RAG - Recomendador de Videojuegos

## 📋 Descripción
Sistema conversacional de recomendación de videojuegos basado en búsqueda inteligente en MongoDB, con soporte multiidioma (español e inglés) y precios en EUR desde GG.deals.

**Status Fase 1**: ✅ **COMPLETADA** - Búsqueda por género y nombre funcional

## ✅ Características Implementadas (Fase 1)

- **12 géneros soportados**: Rol/RPG, Acción, Aventura, Estrategia, Simuladores, Deportes, Carreras, Casual, Indie, Multijugador masivo, Acceso anticipado, Free to Play
- **Búsqueda multiidioma**: Detecta keywords en español e inglés, con y sin acentos
- **Búsqueda por nombre**: Encuentra juegos específicos (case-insensitive)
- **Precios EUR**: Muestra retail + keyshop desde GG.deals
- **Sesiones persistentes**: Historial de conversación por usuario
- **Metadatos completos**: Metacritic, desarrolladores, fecha lanzamiento

## 🏗️ Arquitectura Actual (Fase 1)

### Componentes Principales:

1. **FastAPI API** (`src/api/main.py`)
   - 4 endpoints: `/chat`, `/chat/reset`, `/chat/history`, `/chat/stats`
   - Request/Response models con Pydantic
   - Detección inteligente de intención (género vs nombre)

2. **GameSearchService** (`src/services/game_search.py`)
   - Búsqueda por nombre (regex case-insensitive)
   - Búsqueda por género (keyword matching flexible)
   - Búsqueda por Steam ID
   - Formateo de información de juegos

3. **SessionManager** (`src/api/session_manager.py`)
   - Gestiona sesiones independientes (timeout 60 min)
   - Historial de mensajes por sesión
   - Auto-cleanup de sesiones expiradas

4. **MongoDB Connection**
   - 101 juegos en colección `games`
   - Índices optimizados (name, genres)
   - Conexión via PyMongo

### Flujo de Procesamiento:

```
Usuario → /chat endpoint
    ↓
SessionManager: Crear/obtener sesión
    ↓
Detectar intención (género o búsqueda por nombre)
    ↓
GameSearchService: Consultar MongoDB con filtros
    ↓
Formatear respuesta conversacional
    ↓
Guardar en historial de sesión
    ↓
Retornar ChatResponse con juegos + metadata
```

### Componentes Próximos (Fase 2 - RAG)

- **Embeddings** (`src/embeddings/`): Vectorización con OpenAI API
- **FAISS Retriever** (`src/retrieval/`): Búsqueda semántica
- **LLM Chain** (`src/llm/`): Generación de respuestas avanzadas

## 🛠️ Stack Tecnológico

- **API**: FastAPI 0.109+
- **Database**: MongoDB 7.0 (Docker)
- **Client**: PyMongo 4.6+
- **HTTP**: httpx
- **Config**: Pydantic-settings
- **Logging**: Python logging built-in
- **Python**: 3.10+

## 🚀 Instalación y Uso

### 1. Requisitos
```bash
Python 3.10+
MongoDB (Docker: docker-compose up -d)
.env configurado (MONGODB_URI, GGDEALS_API_KEY)
```

### 2. Setup
```bash
cd chatbot
pip install -r requirements.txt
```

### 3. Ejecutar Servidor

**Opción A: Direct uvicorn**
```bash
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --reload
```

**Opción B: Script Windows (recomendado)**
```bash
.\start_server.bat
```

Swagger UI: http://localhost:8000/docs

## 🔌 API Endpoints

### `POST /chat` - Consultar chatbot
```json
Request:
{
  "query": "Dame juegos indie",
  "session_id": "opcional",
  "filters": {"optional": "filters"}
}

Response:
{
  "response": "Encontré 5 juegos para 'género Indie': Palworld, Balatro, Stardew Valley, Hollow Knight, Valheim.",
  "session_id": "abc123",
  "retrieved_games": [
    {
      "name": "Palworld",
      "genres": ["Indie", "Acción"],
      "price": 29.99,
      "description": "..."
    }
  ],
  "message_count": 1,
  "timestamp": "2026-02-04T..."
}
```

### `GET /chat/history/{session_id}` - Ver conversación
```bash
GET /chat/history/abc123
Response: {"session_id": "abc123", "messages": [...], "message_count": 5}
```

### `POST /chat/reset?session_id=abc123` - Limpiar historial
```bash
POST /chat/reset?session_id=abc123
Response: {"message": "Conversación reseteada", "session_id": "abc123"}
```

### `GET /chat/stats/{session_id}` - Estadísticas sesión
```bash
GET /chat/stats/abc123
Response: {"session_id": "abc123", "created_at": "...", "message_count": 5}
```

## 📚 Ejemplos de Uso

### Búsqueda por Género
```bash
POST /chat
{"query": "Juegos de estrategia"}

→ "Encontré 5 juegos para 'género Estrategia': Balatro, Dota 2, 7 Days to Die, ..."
```

### Búsqueda por Nombre
```bash
POST /chat
{"query": "Elden Ring"}

→ "Encontré 'ELDEN RING'! cuesta 46.38€ en retail y 29.22€ en keyshops. Es un juego de Acción, Rol (Metacritic: 94)."
```

### Multiidioma
```bash
POST /chat
{"query": "RPG games"}
→ Detecta "RPG" = Rol, busca en género Rol

POST /chat
{"query": "free to play"}
→ Detecta "free to play", busca en género Free to Play
```

## 🎮 Géneros Soportados (12)

| Género | Keywords |
|--------|----------|
| **Rol** | rol, rpg |
| **Acción** | acción, action, accion |
| **Aventura** | aventura, adventure |
| **Estrategia** | estrategia, strategy |
| **Simuladores** | simuladores, simulator, simulador, simulation |
| **Deportes** | deportes, sports, sport, deporte |
| **Carreras** | carreras, racing, race |
| **Casual** | casual |
| **Indie** | indie |
| **Multijugador** | multijugador, multiplayer, mmorpg |
| **Acceso Anticipado** | acceso anticipado, early access, beta |
| **Free to Play** | free to play, f2p, gratis, gratuito |

## ✅ Restricciones & Mejores Prácticas

**Implementadas**:
- ✅ Solo retorna datos de BD (sin alucinaciones)
- ✅ Regex case-insensitive para búsquedas flexibles
- ✅ Validación de sesiones con timeout
- ✅ Logging detallado de acciones
- ✅ CORS configurado
- ✅ Manejo robusto de excepciones

**Próximas Fases**:
- ⏳ Validación de precios en tiempo real
- ⏳ Búsqueda semántica (embeddings + FAISS)
- ⏳ Explicaciones detalladas (LLM)
- ⏳ Autenticación de usuarios
- ⏳ Wishlists y favoritos

## 🧪 Testing

Scripts de testing disponibles:

**Tests de API (tests/)**:
```bash
cd tests
python test_all_genres.py   # Validar 12/12 géneros soportados
python test_direct_games.py # Validar búsqueda por nombre
```

**Tests Administrativos (../scripts/)**:
```bash
cd ../scripts
python verify_db.py         # Verificar MongoDB conectado
python test_server.py       # Quick health check del servidor
python test_search_service.py # Test unitario GameSearchService
```

## 📖 Documentación

- [FOLDER_STRUCTURE.md](../FOLDER_STRUCTURE.md) - Estructura completa del proyecto
- [API_TESTS.md](../docs/API_TESTS.md) - Ejemplos de requests
- [SETUP_MONGODB.md](../docs/SETUP_MONGODB.md) - Docker instructions

## 📝 Notas

- **Sin web scraping**: APIs HTTP directas (Steam, GG.deals)
- **Educativo**: Proyecto para aprendizaje con datos reales pero limitados
- **Modular**: Cada componente testeable independientemente
- **Open source friendly**: Fácil extensión con nuevas fuentes
