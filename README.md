# Chatbot RAG - Recomendador de Videojuegos

Sistema educativo de recomendación de videojuegos basado en **FastAPI**, **MongoDB** y preparado para **RAG** (Retrieval-Augmented Generation).

## 📋 Descripción

Chatbot conversacional que:
- ✅ Responde consultas sobre videojuegos
- ✅ Busca juegos por nombre y género en MongoDB
- ✅ Muestra precios en EUR (retail + keyshop)
- ✅ Mantiene historial de sesiones
- ✅ Usa datos reales de Steam y GG.deals

## 🏗️ Arquitectura

```
Usuario → FastAPI /chat endpoint
    ↓
GameSearchService (MongoDB queries)
    ↓
Response con juegos relevantes + precios EUR
```

**Componentes principales**:
- **FastAPI**: REST API con endpoints
- **MongoDB**: 101 videojuegos con metadatos
- **GameSearchService**: Búsqueda por nombre/género
- **Steam Web API**: Metadatos de juegos
- **GG.deals API**: Precios EUR (retail + keyshop)
- **RAG Pipeline**: Embeddings y retrieval (próximamente)

## 📁 Estructura del Proyecto

**Organización profesional y escalable:**

```
Proyecto Hackaton/
├── 🔴 chatbot/              [PRODUCCIÓN] Código principal de aplicación
│   ├── src/api/             FastAPI endpoints
│   ├── src/services/        Lógica MongoDB
│   ├── src/ingestion/       Clientes APIs externas
│   ├── src/embeddings/      RAG (en desarrollo)
│   ├── src/retrieval/       RAG (en desarrollo)
│   └── tests/               Tests de integración API
│
├── 📋 scripts/              [DESARROLLO] Herramientas administrativas
│   ├── verify_db.py         Chequear MongoDB
│   ├── import_from_json.py  Importar 101 juegos
│   └── test_*.py            Tests administrativos
│
├── 📦 data/                 [DATOS] Datasets compartibles
│   └── games_export.json    101 juegos + precios EUR
│
├── 📚 docs/                 [DOCUMENTACIÓN] Guías técnicas
│   ├── API_TESTS.md         Ejemplos de endpoints
│   └── SETUP_MONGODB.md     Instrucciones Docker
│
├── 📖 FOLDER_STRUCTURE.md   ⭐ GUÍA COMPLETA (LEE ESTO PRIMERO)
├── README.md                Este archivo
└── docker-compose.yml       MongoDB
```

**Para entender cada carpeta, lee [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md)** ← RECOMENDADO

## 🚀 Inicio Rápido

### 1. Requisitos
```bash
Python 3.13+
MongoDB (local o remoto)
OpenAI API Key
```

### 2. Instalación
```bash
cd chatbot
pip install -r requirements.txt
```

### 3. Configuración
```bash
# Crear .env en /chatbot/
OPENAI_API_KEY=tu_clave
MONGODB_URI=mongodb://localhost:27017
```

### 4. Ejecutar
```bash
python -m uvicorn src.api.main:app --reload
# Swagger UI: http://localhost:8000/docs
```

## 🔌 API Endpoints

```
POST   /chat                    → Chat principal
POST   /chat/reset              → Limpiar historial
GET    /chat/history/{id}       → Ver conversación
GET    /chat/stats/{id}         → Estadísticas sesión
GET    /                        → Health check
```

**Ejemplo request**:
```json
POST /chat
{
  "query": "Recomendame juegos de rol épicos",
  "filters": {
    "genres": ["RPG"],
    "max_price": 60,
    "min_year": 2015
  }
}
```

**Response**:
```json
{
  "response": "[Recomendaciones con explicaciones]",
  "session_id": "abc123",
  "retrieved_games": [...],
  "message_count": 1,
  "timestamp": "2026-02-04T..."
}
```

## 💬 Ejemplos de Conversación

```
Usuario: "Juegos de rol épicos"
Sistema: "Encontré 5 juegos para 'género Rol': Cyberpunk 2077, ELDEN RING, Black Myth: Wukong, Palworld, The Witcher 3."

Usuario: "¿Cuánto cuesta ELDEN RING?"
Sistema: "Encontré 'ELDEN RING'! cuesta 46.38€ en retail y 29.22€ en keyshops. Es un juego de Acción, Rol (Metacritic: 94/100)."

Usuario: "Dame juegos indie"
Sistema: "Encontré 5 juegos para 'género Indie': Palworld, Balatro, Stardew Valley, Hollow Knight, Valheim."

Usuario: "Free to play"
Sistema: "Encontré 5 juegos para 'género Free to Play': NARAKA: BLADEPOINT, Counter-Strike 2, Dota 2, PUBG: BATTLEGROUNDS, Apex Legends™."
```

## 📊 Estado Actual

| Componente | Estado |
|-----------|--------|
| SessionManager | ✅ Completado |
| Endpoints FastAPI | ✅ Completado |
| Búsqueda por género (12 géneros) | ✅ Completado |
| Búsqueda por nombre de juego | ✅ Completado |
| Precios EUR (retail + keyshop) | ✅ Completado |
| MongoDB conexión | ✅ Operacional (101 juegos) |
| Historial de sesiones | ✅ Completado |
| HybridRetriever | ⏳ Próxima fase (RAG avanzado) |
| RecommendationChain LLM | ⏳ Próxima fase (RAG avanzado) |
| FAISS vector store | ⏳ Próxima fase (embeddings) |

## 🎯 Próximos Pasos (RAG Avanzado)

1. **Generar embeddings FAISS** (vectorización de descripciones)
2. **Implementar HybridRetriever** (búsqueda semántica + filtros)
3. **Conectar RecommendationChain** (LLM para explicaciones detalladas)
4. **Sistema de Usuarios & Wishlists** (autenticación y favoritos)
5. **Dashboards Power BI** (análisis de datos)
6. **Frontend UI** (React/Vue para mejor UX)

## 🛠️ Stack Tecnológico

- **API**: FastAPI 0.109
- **LLM**: GPT-4-turbo (OpenAI)
- **Embeddings**: text-embedding-3-small (OpenAI)
- **Vector DB**: FAISS 1.7
- **Database**: MongoDB 4.6
- **Chains**: LangChain 0.1
- **HTTP Clients**: httpx (APIs directas, sin scraping)

## 📝 Notas

- **Sin web scraping**: Todo usa APIs HTTP directas
- **Anti-fabricación**: System prompt prohíbe inventar datos
- **Memoria conversacional**: 60 min timeout, auto-cleanup
- **Multi-usuario**: Sesiones aisladas por session_id
- **Educativo**: Proyecto para aprendizaje, datos reales limitados

## 📄 Licencia

Proyecto educativo - Viewnext 2026
