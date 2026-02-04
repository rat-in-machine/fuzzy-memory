# 🎮 CHATBOT API - TEST RESULTS

## ✅ Servidor Operativo

El servidor FastAPI está corriendo exitosamente en `http://127.0.0.1:8000`

### Endpoints Disponibles

#### 1. **Health Check** - `GET /`
```
curl.exe -s http://127.0.0.1:8000/
```
Respuesta: Estado del servidor y componentes

#### 2. **Test** - `GET /test`
```
curl.exe -s http://127.0.0.1:8000/test
```
Respuesta: `{"message":"Server is working"}`

#### 3. **Búsqueda de Juegos** - `GET /search-game?name={nombre}&limit={cantidad}`
```
curl.exe -s "http://127.0.0.1:8000/search-game?name=elden&limit=3"
```

### Resultados de Pruebas

#### Test 1: Búsqueda de "ELDEN RING"
```
curl.exe -s "http://127.0.0.1:8000/search-game?name=elden&limit=1"
```
✅ **Resultado:** Encontrado
- Nombre: ELDEN RING
- Steam ID: 1245620
- Precio Retail: 46.38 EUR
- Precio Keyshop: 29.22 EUR
- Estado: Disponible
- Géneros: Acción, Rol
- Desarrollador: FromSoftware, Inc.
- Metacritic: 94

#### Test 2: Búsqueda de "CYBERPUNK 2077"
```
curl.exe -s "http://127.0.0.1:8000/search-game?name=cyberpunk"
```
✅ **Resultado:** Encontrado
- Nombre: Cyberpunk 2077
- Precio: 21.04 EUR

#### Test 3: Búsqueda de "APEX LEGENDS" (F2P)
```
curl.exe -s "http://127.0.0.1:8000/search-game?name=apex"
```
✅ **Resultado:** Encontrado (FREE-TO-PLAY)
- Nombre: Apex Legends™
- Steam ID: 1172470
- Precio Retail: GRATIS
- Precio Keyshop: GRATIS
- Estado: FREE-TO-PLAY
- Géneros: Acción, Aventura, Free to Play
- Desarrollador: Respawn
- Metacritic: 88

### Cómo Iniciar el Servidor

1. **Desde línea de comandos CMD:**
```batch
cd c:\Users\isma1\Desktop\Viewnext\Proyecto Hackaton\chatbot
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

2. **O usar el script batch (en PowerShell):**
```powershell
Start-Process "c:\Users\isma1\Desktop\Viewnext\Proyecto Hackaton\chatbot\start_server.bat" -WindowStyle Normal
```

### Característica Importante

✅ **El endpoint `/search-game` retorna:**
- Información completa del juego (nombre, ID Steam, géneros, desarrollador, Metacritic)
- **Precios en EUR** (tanto retail como keyshop)
- Detecta automáticamente juegos **FREE-TO-PLAY** y los marca como "GRATIS"
- Maneja juegos sin precio disponible correctamente

### Formato de Respuesta

```json
{
    "query": "elden",
    "found": 1,
    "results": [
        {
            "name": "ELDEN RING",
            "steam_id": 1245620,
            "price_retail_eur": "46.38",
            "price_keyshop_eur": "29.22",
            "status": "Disponible",
            "genres": ["Acción", "Rol"],
            "developer": "FromSoftware, Inc.",
            "metacritic": 94,
            "description": "..."
        }
    ]
}
```

---

**Estado:** ✅ OPERACIONAL
**Fecha:** 4 de febrero de 2026
**Componentes Activos:**
- ✅ FastAPI Server
- ✅ MongoDB (101 juegos disponibles)
- ✅ GameSearchService
- ✅ API Endpoints
