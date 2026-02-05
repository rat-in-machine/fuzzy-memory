# 🎮 Interfaz Streamlit - Chatbot de Videojuegos

Interfaz gráfica de usuario basada en Streamlit para interactuar con el chatbot de recomendación de videojuegos. Diseñada como herramienta educativa y plataforma de pruebas para el sistema RAG.

## 📋 Contenido

```
ui/
├── app.py              # Aplicación principal (punto de entrada)
├── config.py           # Configuración centralizada
├── api_client.py       # Cliente HTTP para la API backend
├── components.py       # Componentes visuales reutilizables
├── __init__.py         # Inicializador del paquete
└── requirements.txt    # Dependencias específicas de la UI
```

## 🚀 Instalación

### 1. Instalar dependencias

```bash
# Instalar desde la carpeta raíz del chatbot
pip install -r ui/requirements.txt

# O instalar manualmente
pip install streamlit==1.31.1 httpx==0.26.0 streamlit-option-menu==0.3.6
```

### 2. Verificar que la API está funcionando

Antes de iniciar la UI, asegúrate de que la API FastAPI está ejecutándose:

```bash
# En otra terminal
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --reload

# O usa el script indicado
.\start_server.bat
```

## 🎯 Uso

### Opción A: Script Batch (Windows - Recomendado)

```bash
.\start_ui.bat
```

### Opción B: Comando directo

```bash
streamlit run ui/app.py
```

### Opción C: Script Python

```bash
python ui_launcher.py
```

La aplicación se abrirá en: **http://localhost:8501**

## 📖 Características

### 1. **Gestión de Sesión**
- Generación automática de session_id único
- Monitoreo de estadísticas (fecha creación, conteo de mensajes)
- Reset de conversación

### 2. **Interfaz de Chat**
- Área de conversación con scroll automático
- Visualización clara de mensajes usuario/asistente
- Input de texto con validación
- Indicador de carga durante procesamiento

### 3. **Visualización de Juegos**
- Tarjetas con información completa:
  - Nombre y portada
  - Géneros
  - Precio (retail + keyshop)
  - Puntuación Metacritic
  - Descripción breve
  - Enlace a GG.deals

### 4. **Feedback del Sistema**
- Indicador de estado API (conectado/desconectado)
- Botón de reconexión
- Manejo elegante de errores
- Mensajes informativos claros

### 5. **Configuración**
- URL del backend configurable
- Sidebar con info educativa
- Acceso a documentación de la API (Swagger)

## 🔧 Configuración

La configuración se gestiona mediante la clase `UIConfig` en `config.py`:

```python
# Backend URL (default: http://127.0.0.1:8000)
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Timeout para llamadas HTTP (default: 10 segundos)
API_TIMEOUT = int(os.getenv("API_TIMEOUT", 10))

# Máximo de mensajes a mostrar
MAX_MESSAGES_DISPLAY = 50

# Límite de juegos a mostrar
GAMES_DISPLAY_LIMIT = 5
```

Para cambiar valores, edita `config.py` o establece variables de entorno:

```bash
set BACKEND_URL=http://192.168.1.100:8000
set API_TIMEOUT=15
```

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────┐
│      Interfaz Streamlit (UI)            │
│  (app.py - Lógica y renderizado)        │
└────────────────────┬────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼─────┐           ┌─────▼────────┐
    │ components.py│      │  api_client.py│
    │ (Elementos    │      │  (HTTP calls) │
    │  visuales)    │      │               │
    └───────────┘           └────────┬────┘
                                     │
                            ┌────────▼────────┐
                            │  FastAPI Backend│
                            │  /chat endpoint │
                            └─────────────────┘
```

## 🛠️ Componentes Principales

### `app.py` - Aplicación Principal
- Orquesta toda la UI
- Gestiona el estado con `st.session_state`
- Coordina llamadas a API y renderizado

### `api_client.py` - Cliente HTTP
- Wrapper para los endpoints `/chat`, `/chat/reset`, `/chat/stats`
- Singleton pattern para reutilizar conexión
- Manejo de errores y timeouts

### `components.py` - Componentes Visuales
- `render_game_card()` - Tarjeta individual
- `render_games_section()` - Sección de múltiples juegos
- `render_chat_message()` - Mensaje del chat
- `render_connection_status()` - Estado API
- `render_session_info()` - Info de sesión
- Y más...

### `config.py` - Configuración
- `UIConfig` - Clase con todas las constantes
- Configuración centralizada
- Fácil de modificar y mantener

## 📊 Ejemplo de Uso

1. **Iniciar la UI**: `.\start_ui.bat`
2. **Se crea automáticamente una sesión**
3. **Escribir consulta**: "Dame juegos indie"
4. **Ver recomendaciones**: Aparecen como tarjetas
5. **Explorar**: Hacer clic en enlaces a GG.deals
6. **Resetear**: Botón para nueva conversación

## 🐛 Troubleshooting

### "No se puede conectar a 127.0.0.1:8000"
- Verifica que la API FastAPI está ejecutándose
- Abre otra terminal y usa `.\start_server.bat`

### "ModuleNotFoundError: No module named 'streamlit'"
- Instala streamlit: `pip install streamlit`
- O usa `pip install -r ui/requirements.txt`

### "Port 8501 is already in use"
- La aplicación anterior no se cerró correctamente
- Espera 30 segundos o usa: `streamlit run ui/app.py --server.port 8502`

### Los imports no funcionan
- Asegúrate de ejecutar desde la carpeta `chatbot`
- Usa `streamlit run ui/app.py` (no `python ui/app.py`)

## 🚀 Mejoras Futuras

- [ ] Streaming de respuestas LLM
- [ ] Integración RAG avanzada
- [ ] Filtros de búsqueda dinámicos
- [ ] Historial persistente en MongoDB
- [ ] Autenticación de usuarios
- [ ] Dashboard con analytics
- [ ] Dark mode mejorado
- [ ] Búsqueda por rango de precio

## 📚 Documentación Relacionada

- [Backend README](../README.md) - Info de la API
- [Swagger UI](http://localhost:8000/docs) - Documentación interactiva de la API
- [Streamlit Docs](https://docs.streamlit.io) - Documentación oficial de Streamlit

## 🤝 Contribuciones

Esta es una interfaz educativa para el Hackathon. Las mejoras y sugerencias son bienvenidas.

---

**Versión:** 0.1.0  
**Estado:** Desarrollo  
**Última actualización:** 2026-02-05
