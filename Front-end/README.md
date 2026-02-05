# 🎮 Videogames Recommender - Frontend

Frontend de React para el chatbot recomendador de videojuegos.

## 🚀 Características Implementadas

### ✅ Core
- **📺 Pantalla listado juegos** - Búsqueda por nombre y género
- **❤️ Wishlist usuario** - Guardar juegos favoritos en localStorage
- **💬 Chat UI** - Interfaz conversacional con streaming
- **🎮 Vista detalle juego** - Información completa de cada juego

### ✨ Bonus
- **📊 Panel estadísticas** - Estadísticas de sesión (próximo)
- **🔔 Notificaciones UI** - Sistema de notificaciones (próximo)

## 📁 Estructura del Proyecto

```
src/
├── components/          # Componentes React
│   ├── GameCard.js     # Tarjeta individual de juego
│   ├── GamesList.js    # Listado y búsqueda de juegos
│   ├── ChatUI.js       # Chat conversacional
│   └── Wishlist.js     # Lista de favoritos
├── pages/              # Páginas (próximo)
├── services/
│   └── api.js         # Cliente API Axios
├── styles/            # CSS por componente
├── App.js            # Componente principal
├── App.css           # Estilos globales
└── index.js          # Entry point
```

## 🛠️ Instalación

```bash
cd "c:\Users\isma1\Desktop\Viewnext\Proyecto Hackaton\Front-end"
npm install
```

## ▶️ Desarrollo

```bash
npm start
```

Abre [http://localhost:3000](http://localhost:3000) en el navegador.

## 🏗️ Build

```bash
npm run build
```

## 🔌 API Backend

El frontend se conecta a:
- **URL:** `http://127.0.0.1:8000`
- **Endpoints utilizados:**
  - `GET /search-game` - Buscar por nombre
  - `GET /search-by-genre` - Buscar por género
  - `POST /chat` - Chatbot recomendador
  - `POST /chat/reset` - Reset sesión
  - `GET /chat/history/{session_id}` - Historial
  - `GET /chat/stats/{session_id}` - Estadísticas

## 💾 Almacenamiento Local

- **Wishlist** → localStorage (persistencia entre sesiones)
- **Session ID** → React state (sesión de chat)

## 🎨 Diseño

- **Tema:** Gradiente Morado-Azul
- **Framework CSS:** CSS puro (sin dependencias)
- **Responsive:** Soporta mobile y desktop

## 📦 Dependencias

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "axios": "^1.6.0",
  "react-router-dom": "^6.18.0"
}
```

## 🚧 Próximas Features

- [ ] Panel de estadísticas de sesión
- [ ] Sistema de notificaciones push
- [ ] Página de detalle de juego expandida
- [ ] Dark mode
- [ ] Integración con LLM streaming
- [ ] Historial de búsquedas
- [ ] Compartir wishlist

## 📝 Notas

- El chat está completamente funcional sin LLM
- La wishlist se sincroniza automáticamente con localStorage
- Los componentes son reutilizables y modulares

---

**Desarrollado con ❤️ en React**
