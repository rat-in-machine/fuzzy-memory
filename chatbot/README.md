# Chatbot RAG - Recomendador de Videojuegos

## 📋 Descripción
Sistema conversacional inteligente de recomendación de videojuegos con búsqueda avanzada en MongoDB, integración con LLM (CodingBuddy gpt-5), UI interactiva con Streamlit y soporte para búsquedas normalizadas (sin acentos ni mayúsculas).

**Status Actual**: ✅ **BÚSQUEDA + LLM COMPLETADO** - Sistema conversacional funcional e integrado

## ✅ Características Implementadas

### Búsqueda Inteligente
- **3-tier Priority System**: 
  1. Búsqueda específica por nombre (detecta palabras capitalizadas)
  2. Búsqueda por género (keywords flexibles)
  3. Búsqueda general por palabras clave
- **Normalización de texto**: Funciona con o sin acentos/mayúsculas (Pokémon/pokemon/POKEMON)
- **12 géneros soportados**: Rol/RPG, Acción, Aventura, Estrategia, Simuladores, Deportes, Carreras, Casual, Indie, Multijugador masivo, Acceso anticipado, Free to Play
- **Detección de juegos mencionados**: El LLM puede recomendar juegos alternativos y el sistema intenta encontrarlos en BD

### Generación de Respuestas
- **LLM Integrado**: CodingBuddy gpt-5 con experto gaming
- **Respuestas conversacionales**: Explicaciones contextuales y recomendaciones personalizadas
- **Sesiones persistentes**: Historial de conversación con timeout configurable (60 min)
- **Metadatos completos**: Metacritic, desarrolladores, fecha lanzamiento, precios EUR

### Interfaz
- **Streamlit UI** (`ui/app.py`): Chat interactivo en navegador
- **FastAPI API** (`src/api/main.py`): 6 endpoints RESTful
- **Visualización de juegos**: Cards con imagen, precio, géneros, descripción

## 🏗️ Arquitectura Actual

### Componentes Principales:

1. **FastAPI API** (`src/api/main.py`)
   - 6 endpoints: `/chat`, `/chat/reset`, `/chat/history`, `/chat/stats`, `/games/all`, `/health`
   - Request/Response models con Pydantic
   - 3-tier search priority (específico → género → general)
   - Integración con LLM para respuestas conversacionales

2. **GameSearchService** (`src/services/game_search.py`)
   - Búsqueda normalizada: elimina acentos y mayúsculas automáticamente
   - Búsqueda por nombre (con límite configurable)
   - Búsqueda por género (keyword matching flexible)
   - Búsqueda por Steam ID
   - Formateo de información de juegos

3. **LLM Client** (`src/llm/client.py`)
   - Integración CodingBuddy gpt-5
   - Generación de respuestas conversacionales
   - System prompt especializado en gaming
   - Timeout configurable (60 segundos)

4. **SessionManager** (`src/api/session_manager.py`)
   - Gestiona sesiones independientes (timeout 60 min)
   - Historial de mensajes por sesión
   - Auto-cleanup de sesiones expiradas
   - Estadísticas por sesión

5. **Streamlit UI** (`ui/app.py`)
   - Chat interactivo en tiempo real
   - Visualización de cardas de juegos
   - Estado de conexión a API
   - Historial de conversaciones

6. **MongoDB Connection**
   - 101 juegos en colección `games`
   - Índices optimizados
   - Conexión via PyMongo

### Flujo de Procesamiento:

```
Usuario → Streamlit Chat UI
    ↓
FastAPI /chat endpoint
    ↓
SessionManager: Crear/obtener sesión
    ↓
GameSearchService: 3-tier search
    ├─ Detectar búsqueda específica (palabras capitalizadas)
    ├─ Detectar búsqueda por género
    └─ Búsqueda general por palabras clave
    ↓
LLM Client: Generar respuesta conversacional
    ├─ Context: Juegos encontrados
    └─ Output: Respuesta + metadata
    ↓
Detectar juegos mencionados en respuesta LLM
    ↓
Retornar ChatResponse con juegos visualizables
    ↓
Streamlit: Mostrar chat + cards de juegos
```

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
Dependencias: pip install -r requirements.txt
.env configurado (ver variables requeridas abajo)
```

### 2. Variables de Entorno (.env)
```bash
# MongoDB
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=videogames_recommender

# LLM (CodingBuddy)
LLM_API_ENDPOINT=https://ia-research-dev.codingbuddy-...
LLM_API_KEY=tu_api_key_aqui
LLM_USER_EMAIL=tu_email@example.com
LLM_MODEL=gpt-5

# Timeouts
API_TIMEOUT=60
SESSION_TIMEOUT=3600
```

### 3. Setup
```bash
cd chatbot
pip install -r requirements.txt
```

### 4. Ejecutar Sistema Completo

**Opción A: Windows Batch Script (RECOMENDADO)**
```bash
.\START_ALL.bat
```
Inicia ambos servicios en ventanas separadas:
- Backend FastAPI: http://localhost:8000
- Frontend Streamlit: http://localhost:8501

**Opción B: Manualmente**

Terminal 1 - Backend:
```bash
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Terminal 2 - Frontend:
```bash
streamlit run ui/app.py --server.port 8501
```

### 5. Acceso

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Chat UI** | http://localhost:8501 | Interfaz Streamlit |
| **API** | http://localhost:8000 | FastAPI |
| **API Docs** | http://localhost:8000/docs | Swagger interactivo |
| **Health Check** | http://localhost:8000/health | Estado del servidor |

## 🔌 API Endpoints

### `POST /chat` - Chat conversacional con LLM
```json
Request:
{
  "query": "Háblame de Pokémon",
  "session_id": "opcional"
}

Response:
{
  "response": "No tenemos Pokémon, pero te recomiendo Palworld que es muy similar...",
  "session_id": "sess-abc123",
  "retrieved_games": [
    {
      "name": "Palworld",
      "genres": ["Indie", "Acción"],
      "current_price_retail": 29.99,
      "current_price_keyshop": 19.99,
      "description": "Monster catching adventure...",
      "metacritic": 85,
      "header_image": "url...",
      "ggdeals_url": "url..."
    }
  ],
  "message_count": 1,
  "timestamp": "2026-02-05T..."
}
```

**Características**:
- Búsqueda automática 3-tier (específico → género → general)
- Respuesta generada por LLM especializado
- Detección de juegos en la respuesta para mostrar visuales
- Normalización: busca sin acentos ni mayúsculas

### `GET /health` - Estado del servidor
```bash
GET /health
Response: {"status": "ok", "timestamp": "2026-02-05T..."}
```

### `GET /chat/history/{session_id}` - Historial de conversación
```bash
GET /chat/history/sess-abc123
Response: {
  "session_id": "sess-abc123",
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "message_count": 5
}
```

### `POST /chat/reset` - Limpiar historial
```bash
POST /chat/reset?session_id=sess-abc123
Response: {"message": "Conversación reseteada", "session_id": "sess-abc123"}
```

### `GET /chat/stats/{session_id}` - Estadísticas de sesión
```bash
GET /chat/stats/sess-abc123
Response: {
  "session_id": "sess-abc123",
  "created_at": "2026-02-05T...",
  "last_message_at": "2026-02-05T...",
  "message_count": 5,
  "status": "active"
}
```

### `GET /games/all` - Listar todos los juegos
```bash
GET /games/all?page=1&page_size=25
Response: {
  "games": [...],
  "total": 101,
  "page": 1,
  "page_size": 25,
  "total_pages": 5
}
```

## 📚 Ejemplos de Uso

### Búsqueda Específica (nombre de juego)
```
Usuario: "Qué tal es Valheim?"
LLM: "Valheim es un videojuego de mundo abierto con mecánicas de supervivencia... cuesta 19.99€"
Visualización: [Card con Valheim]
```

### Búsqueda por Género
```
Usuario: "Juegos de estrategia"
LLM: "Te recomiendo juegos como Balatro, Dota 2, StarCraft 2... perfecto para pensar estrategias"
Visualización: [5 cards de juegos estrategia]
```

### Juego no en BD con Alternativa
```
Usuario: "Háblame de Pokémon"
LLM: "No tenemos Pokémon, pero Palworld es muy similar - es un creature collector con mecánicas de acción"
Visualización: [Card con Palworld]
```

### Búsqueda Normalizada
```
Usuario: "pokemon" / "Pokémon" / "POKEMON"
→ Sistema busca sin acentos/mayúsculas
```

### Historial de Conversación
```
Usuario pregunta 1: "RPG baratos"
→ Se crea sesión, se guardan preguntas
Usuario pregunta 2: "¿Cuánto cuesta el primero?"
→ Historial disponible en /chat/history/session-id
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

## ✅ Restricciones & Guía de Uso

**Implementadas**:
- ✅ Búsqueda normalizada (sin acentos/mayúsculas)
- ✅ 3-tier priority system (específico → género → general)
- ✅ LLM conversacional integrado
- ✅ Detección de juegos en respuestas LLM
- ✅ Sesiones persistentes con timeout
- ✅ Logging detallado de búsquedas
- ✅ CORS configurado
- ✅ Manejo robusto de excepciones
- ✅ UI interactiva Streamlit

**Límites de Búsqueda**:
- Búsqueda específica: retorna **1 juego** (si existe)
- Búsqueda por género: retorna **5 juegos**
- Búsqueda general: retorna **5 juegos**
- Juegos mencionados por LLM: extrae hasta **3** automáticamente

**Próximas Mejoras**:
- ⏳ Búsqueda semántica con embeddings
- ⏳ Cache de respuestas frecuentes
- ⏳ Análisis de sentimiento de preguntas
- ⏳ Autenticación y wishlists de usuario

## 📖 Documentación

Estructura de carpetas:
- `src/api/` - Endpoints FastAPI y lógica principal
- `src/services/` - GameSearchService y utilidades
- `src/llm/` - Integración CodingBuddy LLM
- `ui/` - Interfaz Streamlit
- `config/` - Configuración general
- `data/` - Datos de ejemplo y esquemas
- `.env.example` - Variables de entorno necesarias

## 📊 Stack Tecnológico

| Componente | Versión | Usar |
|-----------|---------|------|
| **Python** | 3.10+ | Lenguaje base |
| **FastAPI** | 0.109+ | API REST |
| **Streamlit** | 1.53+ | UI Chat |
| **MongoDB** | 7.0+ | Base de datos |
| **PyMongo** | 4.6+ | Driver MongoDB |
| **httpx** | 0.26+ | HTTP Client para LLM |
| **Pydantic** | 2.0+ | Validación de datos |
| **python-dotenv** | 1.0+ | Variables de entorno |

## 📝 Notas

- **Educativo**: Proyecto para aprendizaje con datos reales pero limitados (101 juegos)
- **Modular**: Cada componente testeable independientemente
- **Extensible**: Fácil agregar nuevas fuentes de datos o LLMs
- **Production-ready**: Logging, error handling, timeouts configurables
- **Clean code**: Siguiendo PEP 8 y best practices Python
