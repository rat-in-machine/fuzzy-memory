# 📁 Estructura del Proyecto - Guía Completa

> Documento profesional explicando la organización del proyecto educativo de Videogames Recommender
> **Última actualización:** 2024 | **Versión:** 1.0 (Restructured)

---

## 📋 Tabla de Contenidos
1. [Visión General](#visión-general)
2. [Estructura Completa](#estructura-completa)
3. [Carpetas Principales](#carpetas-principales)
4. [Flujos de Datos](#flujos-de-datos)
5. [Quick Start](#quick-start)
6. [Scripts Disponibles](#scripts-disponibles)
7. [Notas Educativas](#notas-educativas)

---

## Visión General

**Proyecto:** Sistema educativo de Recomendación de Videojuegos  
**Stack:** FastAPI + MongoDB + RAG (embeddings + retrieval + LLM)  
**Datos:** 101 juegos desde Steam Web API + precios EUR desde GG.deals  

### Organización Lógica

```
Proyecto Hackaton/
├── 🔴 chatbot/              [PRODUCCIÓN] - Código principal de la aplicación
├── 📋 scripts/              [DESARROLLO] - Herramientas administrativas
├── 📦 data/                 [DATOS] - Datasets y cachés
├── 📚 docs/                 [DOCUMENTACIÓN] - Guías técnicas
├── 🐳 docker-compose.yml    [INFRAESTRUCTURA] - MongoDB containerizado
└── 📖 README.md             [INFO] - Descripción general del proyecto
```

---

## Estructura Completa

```
Proyecto Hackaton/
│
├── 🔴 chatbot/                              [CÓDIGO DE PRODUCCIÓN]
│   ├── src/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── main.py                      ⭐ FastAPI application
│   │   │   └── session_manager.py           Session handling
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── game_search.py               🔍 MongoDB queries
│   │   │
│   │   ├── ingestion/
│   │   │   ├── steam_client.py              🎮 Steam Web API client
│   │   │   └── ggdeals_client.py            💰 GG.deals API client
│   │   │
│   │   ├── embeddings/                      [RAG - En Desarrollo]
│   │   │   ├── vectorizer.py                Generación de embeddings
│   │   │   └── embeddings_cache.py
│   │   │
│   │   ├── retrieval/                       [RAG - En Desarrollo]
│   │   │   └── retriever.py                 📊 FAISS semantic search
│   │   │
│   │   ├── llm/                             [RAG - En Desarrollo]
│   │   │   ├── chain.py                     LLM chains y prompts
│   │   │   └── prompts.py
│   │   │
│   │   └── __init__.py
│   │
│   ├── config/
│   │   └── settings.py                      ⚙️ Configuración centralizada
│   │
│   ├── data/                                [Datos locales]
│   │   ├── raw/                             Datos sin procesar
│   │   ├── processed/                       Datos normalizados
│   │   └── vector_store/                    FAISS indices (futuro)
│   │
│   ├── tests/                               [Pruebas unitarias]
│   │   └── __init__.py
│   │
│   ├── .env                                 🔐 Variables de entorno (NO COMPARTIR)
│   ├── .env.example                         📝 Template .env (COMPARTIR)
│   ├── requirements.txt                     📦 Dependencias Python
│   ├── README.md                            Documentación del chatbot
│   ├── server.log                           📝 Logs del servidor
│   │
│   ├── start_server.bat                     🚀 Lanzador servidor (Windows)
│   ├── ask.ps1                              CLI helper (PowerShell)
│   ├── ask.py                               CLI helper (Python)
│   ├── chat_interactive.py                  Terminal UI (opcional)
│   └── q.json                               Query cache (temporal)
│
├── 📋 scripts/                              [HERRAMIENTAS DE DESARROLLO]
│   ├── verify_db.py                         ✅ Verificar estado MongoDB
│   ├── import_from_json.py                  ⚡ Importar 101 juegos desde JSON
│   ├── export_games.py                      📤 Exportar MongoDB → JSON
│   ├── ingest_games_to_mongodb.py           🔄 Pipeline completo (Steam + GG.deals)
│   ├── clear_db.py                          🗑️ Limpiar colección games
│   │
│   ├── test_server.py                       Probar endpoints
│   ├── test_genres.py                       Probar búsqueda por géneros
│   ├── test_genre_direct.py                 Debug géneros
│   └── test_chat_genres.py                  Probar chat con géneros
│
├── 📦 data/                                 [DATASETS COMPARTIBLES]
│   ├── games_export.json                    📊 101 juegos + precios EUR
│   │   └── Contenido: [game1, game2, ...]
│   │       Campos: steam_id, name, genres[], price_retail_eur, price_keyshop_eur
│   │       Casos: 80 con precio, 14 F2P (0€), 7 sin precio
│   │
│   └── [Futuro]
│       ├── raw/                             Datos crudos de APIs
│       ├── processed/                       Datos normalizados
│       └── vector_store/                    Índices FAISS
│
├── 📚 docs/                                 [DOCUMENTACIÓN TÉCNICA]
│   ├── API_TESTS.md                         📝 Ejemplos de endpoints
│   └── SETUP_MONGODB.md                     🐳 Instrucciones Docker
│
├── 🐳 docker-compose.yml                    MongoDB + Configuración
├── 📖 README.md                             Visión general
├── 📖 FOLDER_STRUCTURE.md                   ⭐ ESTE ARCHIVO
└── 📖 INSTRUCCIONES_ZIP.md                  Guía de entrega
```

---

## Carpetas Principales

### 🔴 `chatbot/` - Código de Producción

**Propósito:** Todo el código de la aplicación principal  
**Responsabilidades:**
- Servir API FastAPI en puerto 8000
- Consultar MongoDB para búsquedas de juegos
- Gestionar sesiones de chat
- Generar embeddings (próximo)
- Recuperar información semánticamente (próximo)
- Integración con LLM (próximo)

**Estructura interna:**
```
chatbot/
├── src/                    Código fuente
│   ├── api/                FastAPI + endpoints
│   ├── services/           Lógica de negocio
│   ├── ingestion/          Clientes de APIs externas
│   └── embeddings/         RAG (vectorización)
├── config/                 Configuración centralizada
├── data/                   Datos locales del chatbot
├── tests/                  Pruebas unitarias
└── [Scripts lanzadores]
    ├── start_server.bat
    ├── ask.ps1
    └── chat_interactive.py
```

**Archivos Críticos:**
- **`src/api/main.py`** (~650 líneas) - FastAPI application con 4 endpoints
- **`src/services/game_search.py`** - Consultas MongoDB
- **`config/settings.py`** - Variables de configuración
- **`requirements.txt`** - Dependencias Python

---

### 📋 `scripts/` - Herramientas de Desarrollo

**Propósito:** Scripts one-off para tareas administrativas  
**Nota:** Estos scripts NO cargan el servidor API

| Script | Función | Comando |
|--------|---------|---------|
| `verify_db.py` | Chequea MongoDB + estadísticas | `python scripts/verify_db.py` |
| `import_from_json.py` | Importa 101 juegos desde JSON | `python scripts/import_from_json.py` |
| `export_games.py` | Exporta MongoDB → JSON | `python scripts/export_games.py` |
| `ingest_games_to_mongodb.py` | Pipeline completo (Steam + GG.deals) | `python scripts/ingest_games_to_mongodb.py` |
| `clear_db.py` | Limpia colección games | `python scripts/clear_db.py` |
| `test_*.py` | Pruebas varias | `python scripts/test_*.py` |

**Responsabilidades:**
- Importación y exportación de datos
- Validación de base de datos
- Testing y debugging
- Mantenimiento administrativo

---

### 📦 `data/` - Datasets Compartibles

**Propósito:** Almacenar datos en formato de archivo

**Contenido actual:**
```json
games_export.json (3.5 MB)
├── 101 juegos completos
├── Campos: steam_id, name, genres[], price_retail_eur, price_keyshop_eur
├── Casos especiales:
│   ├── 80 juegos con precio
│   ├── 14 F2P (price = 0)
│   └── 7 sin precio (null)
└── Uso: Importación rápida a nuevas instancias MongoDB
```

**Políticas:**
- ✅ Compartible dentro del equipo
- ❌ NO público (respeta datos Steam + GG.deals)
- ✅ Versionado en Git (caché, no sensible)

**Estructura futura:**
```
data/
├── raw/                Datos crudos de APIs
├── processed/          Datos limpios y normalizados
└── vector_store/       Índices FAISS (cuando RAG esté listo)
```

---

### 📚 `docs/` - Documentación Técnica

**Propósito:** Guías técnicas y referencias

**Archivos actuales:**
- **`API_TESTS.md`** - Ejemplos de uso de endpoints (cURL, Postman, PowerShell)
- **`SETUP_MONGODB.md`** - Instrucciones para Docker

**Documentos a crear (próximas fases):**
- `ARCHITECTURE.md` - Diagrama del sistema y flujos de datos
- `DATABASE_SCHEMA.md` - Colecciones y índices MongoDB
- `RAG_DESIGN.md` - Embeddings, retrieval y LLM chains
- `SETUP.md` - Guía completa step-by-step

---

## Flujos de Datos

### 1️⃣ Flujo: Búsqueda por Género

```
Usuario pregunta: "dame juegos de rol"
    ↓
POST /chat endpoint (main.py)
    ↓
GameSearchService.search_by_genre("Rol")
    ↓
MongoDB query: db.games.find({"genres": /Rol/i})
    ↓
Formateo con precios EUR
    ↓
Respuesta: "Encontré 5 juegos para género Rol: [list]"
```

### 2️⃣ Flujo: Ingesta Inicial de Datos

```
ingest_games_to_mongodb.py
    ├─→ Steam Web API (GET /appdetails)
    │   └─ Metadatos: name, genres, release_date, developers
    │
    ├─→ GG.deals API (GET /prices)
    │   └─ Precios EUR: retail + keyshop
    │
    └─→ Normalización y MongoDB insert
        └─ db.games.insertOne({...})
```

### 3️⃣ Flujo: Importación Rápida (Testing)

```
import_from_json.py
    ├─ Lee data/games_export.json (101 juegos precargados)
    ├─ MongoDB: db.games.deleteMany({}) [Limpia anterior]
    ├─ MongoDB: db.games.insertMany([...]) [Inserta en lote]
    └─ Verifica conteos y completa
```

### 4️⃣ Flujo: RAG (Próximamente)

```
Usuario: "Dame un juego tipo aventura con buen Metacritic"
    ↓
POST /chat
    ├─ Embeddings: Vectorizar pregunta
    ├─ FAISS: Búsqueda semántica entre juegos
    └─ LLM: GPT-4 genera respuesta con explicación
    ↓
Respuesta personalizada
```

---

## Quick Start

### 1️⃣ Setup Inicial

```bash
# Clonar repo
git clone <repo-url>
cd "Proyecto Hackaton"

# Crear virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Instalar dependencias
pip install -r chatbot/requirements.txt
```

### 2️⃣ Levantar MongoDB

```bash
# En terminal aparte
docker-compose up -d

# Verificar
docker ps  # MongoDB debe estar corriendo
```

### 3️⃣ Importar Datos

```bash
# Opción A: Importación rápida (101 juegos precargados)
python scripts/import_from_json.py

# Opción B: Ingesta completa desde APIs
python scripts/ingest_games_to_mongodb.py

# Verificar
python scripts/verify_db.py
```

### 4️⃣ Iniciar Servidor

```bash
# Windows: Lanzador visual
chatbot\start_server.bat

# O manual:
cd chatbot
uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```

### 5️⃣ Probar Endpoints

```bash
# Health check
curl http://127.0.0.1:8000/

# Búsqueda
curl "http://127.0.0.1:8000/search-game?name=minecraft&limit=5"

# Chat (POST)
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"dame juegos de rol"}'

# O usar PowerShell helper
.\chatbot\ask.ps1 "dame juegos de rol"
```

---

## Scripts Disponibles

### Verificación
```bash
python scripts/verify_db.py
# Output:
# ✓ Conexión a MongoDB exitosa
# ✓ Database: videogames_recommender
# ✓ Colección games: 101 documentos
# ✓ Juegos con precio: 80
# ✓ F2P (0€): 14
# ✓ Sin precio: 7
```

### Importación
```bash
python scripts/import_from_json.py
# Importa 101 juegos desde data/games_export.json
# Velocidad: ~10 segundos
# Windows-compatible: Sin emojis
```

### Ingesta desde APIs
```bash
python scripts/ingest_games_to_mongodb.py
# Pipeline completo: Steam + GG.deals → MongoDB
# Velocidad: ~5 minutos para 100 juegos
# Nota: Respetar rate limits de APIs
```

### Testing
```bash
python scripts/test_server.py          # Prueba endpoints básicos
python scripts/test_genres.py          # Prueba búsqueda por géneros
python scripts/test_chat_genres.py     # Prueba chat
```

---

## Notas Educativas

### Conceptos Implementados

**1. API REST con FastAPI**
- Routing (@app.get, @app.post)
- Request/Response models
- Query parameters
- Status codes HTTP

**2. Consultas MongoDB**
- PyMongo client
- Operadores regex ($regex)
- Filtros y proyecciones
- Optimización con índices

**3. Gestión de Configuración**
- Variables de entorno (.env)
- Secretos seguros
- Múltiples ambientes
- Defaults inteligentes

**4. Procesamiento de Datos Externos**
- HTTP requests asincronos (httpx)
- Rate limiting
- Error handling
- Parsing JSON
- Normalización de datos

**5. Session Management**
- Almacenamiento de estado
- User context
- Conversation history
- Limpieza de sesiones antiguas

### Próximas Fases: RAG

Cuando estés listo para implementar RAG:

```
Fase 1: Embeddings
├─ Implementar vectorizer.py
├─ OpenAI Embeddings o SentenceTransformers
├─ Generar embeddings para cada juego
└─ Guardar en FAISS

Fase 2: Retrieval
├─ Implementar retriever.py
├─ FAISS similarity search
├─ Rerank resultados
└─ Integrar en /chat endpoint

Fase 3: LLM Chain
├─ OpenAI API integration
├─ Custom prompts
├─ Context enrichment
└─ Explicaciones generadas
```

### Decisiones Arquitectónicas

**¿Por qué esta estructura?**
- ✅ Separación clara: producción | desarrollo | datos | docs
- ✅ Modular: fácil agregar RAG, LLM, Auth
- ✅ Escalable: preparado para crecimiento
- ✅ Educativo: claro para estudiantes

**¿Por qué MongoDB?**
- ✅ Flexible schema (géneros array, precios dinámicos)
- ✅ Ideal para documentos (metadatos juegos)
- ✅ Escalable horizontalmente
- ✅ Native JSON (REST ↔ DB sin mapping)

**¿Por qué FastAPI?**
- ✅ Async by default (concurrencia)
- ✅ Validación automática (Pydantic)
- ✅ OpenAPI/Swagger integrado
- ✅ Performance similar a Node.js
- ✅ Type hints (IDE support)

---

## Checklist de Validación

- [ ] MongoDB corriendo (`docker ps`)
- [ ] 101 juegos en colección (`python scripts/verify_db.py`)
- [ ] API responde (`curl http://127.0.0.1:8000/`)
- [ ] Search funciona (`/search-game?name=minecraft`)
- [ ] Genre search funciona (`/search-by-genre?genre=Rol`)
- [ ] Chat responde (`POST /chat`)
- [ ] Precios en EUR mostrados correctamente

---

## Troubleshooting

| Problema | Solución |
|----------|----------|
| "Connection refused MongoDB" | `docker-compose up -d mongodb` |
| "ModuleNotFoundError: pymongo" | `pip install -r chatbot/requirements.txt` |
| "No module named 'src.api'" | `cd chatbot` antes de ejecutar |
| "Encoding error Windows" | Python 3.10+ + UTF-8 locale |
| "/chat devuelve vacío" | Verificar MongoDB tiene datos |

---

## Recursos Educativos

- **FastAPI:** https://fastapi.tiangolo.com/
- **MongoDB:** https://docs.mongodb.com/
- **PyMongo:** https://pymongo.readthedocs.io/
- **FAISS:** https://github.com/facebookresearch/faiss
- **LangChain:** https://python.langchain.com/

---

## Estado Actual del Proyecto

### ✅ Completado
- FastAPI server con 4 endpoints
- MongoDB con 101 juegos + precios EUR
- Búsqueda por nombre y género
- Chat conversacional (keyword-based)
- Scripts de ingesta/exportación
- **Estructura profesional reorganizada** ← NUEVO
- **Documentación completa** ← NUEVO

### ⏳ En Desarrollo
- RAG: Embeddings
- RAG: FAISS retrieval
- RAG: LLM integration

### ❌ Próximo (No iniciado)
- Users & Authentication
- Wishlists
- Advanced filtering
- Power BI dashboards
- Frontend UI

---

**Última actualización:** 2024  
**Versión:** 1.0 (Restructured)  
**Mantenedor:** Equipo Proyecto Hackaton  
**Licencia:** Educativa
