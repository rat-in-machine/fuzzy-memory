# Tests del Chatbot

Esta carpeta contiene tests de integración para validar el funcionamiento del chatbot a través de la API REST.

## Tests Disponibles

### `test_all_genres.py` ✅ CRÍTICO
**Propósito**: Valida que los 12 géneros soportados funcionan correctamente

**Géneros testeados**:
- Rol/RPG
- Acción
- Aventura
- Estrategia
- Simuladores
- Deportes
- Carreras
- Casual
- Indie
- Multijugador masivo
- Acceso anticipado
- Free to Play

**Cómo ejecutar**:
```bash
cd chatbot/tests
python test_all_genres.py
```

**Resultado esperado**: 12/12 géneros con al menos 1 juego encontrado


### `test_direct_games.py` ✅ IMPORTANTE
**Propósito**: Valida búsqueda por nombre específico de juego

**Juegos testeados**:
- elden ring
- minecraft (no en DB, debe fallar)
- cyberpunk 2077
- stardew

**Cómo ejecutar**:
```bash
cd chatbot/tests
python test_direct_games.py
```

**Resultado esperado**: Juegos encontrados con precios EUR y géneros correctos


## Pre-requisitos

1. **Servidor FastAPI ejecutándose**:
   ```bash
   cd ../
   python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
   ```

2. **MongoDB operacional**:
   ```bash
   docker ps  # Verificar container MongoDB
   ```

3. **Dependencias instaladas**:
   ```bash
   pip install requests
   ```

## Interpretación de Resultados

### ✓ Éxito
```
✓ ROL: 5 juegos (Cyberpunk 2077, ELDEN RING, ...)
✓ Búsqueda: elden ring
  Resultado: Encontré 'ELDEN RING'! cuesta 46.38€ ...
```

### ✗ Fallo
```
✗ INDIE: Error 500
❌ Sin resultados para minecraft
```

## Tests Administrativos (ver ../scripts/)

Los tests de infraestructura y administración están en `scripts/`:

- `test_server.py` - Quick health check del servidor
- `test_search_service.py` - Test unitario de GameSearchService
- `test_steam_ggdeals_integration.py` - Test de ingesta de datos

## Notas

- Estos tests son de **integración end-to-end** (E2E)
- Requieren servidor activo y MongoDB poblado
- **NO** son tests unitarios (no usan mocking)
- Diseñados para validación post-deployment

## Ejecución Completa

Para ejecutar todos los tests de una vez:

```bash
cd chatbot/tests
python test_all_genres.py && python test_direct_games.py
```

## Troubleshooting

**Error de conexión**: Verificar que servidor esté en http://127.0.0.1:8000
```bash
curl http://127.0.0.1:8000/  # Debe retornar 200
```

**Timeout**: Aumentar timeout en código si la red es lenta
```python
response = requests.post(..., timeout=10)  # Aumentar de 5 a 10 segundos
```

**Sin juegos encontrados**: Verificar que MongoDB tiene los 101 juegos
```bash
cd ../../scripts
python verify_db.py
```
