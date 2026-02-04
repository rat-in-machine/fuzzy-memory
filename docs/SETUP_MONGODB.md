# 🗄️ Instalación de MongoDB

## Opción 1: Docker (Recomendado - Más rápido)

### Paso 1: Verificar Docker
```powershell
docker --version
```

### Paso 2: Levantar MongoDB con Docker
```powershell
# En la raíz del proyecto
docker-compose up -d mongodb
```

Si no tienes `docker-compose.yml`, usa:
```powershell
docker run -d --name mongodb -p 27017:27017 -e MONGO_INITDB_DATABASE=videogames_recommender mongo:7.0
```

### Paso 3: Verificar que está corriendo
```powershell
docker ps
```

### Paso 4: Ejecutar la ingesta
```powershell
python ingest_games_to_mongodb.py
```

---

## Opción 2: Instalación Local (Windows)

### Paso 1: Descargar MongoDB
Visita: https://www.mongodb.com/try/download/community

Selecciona:
- Version: 7.0.x (Current)
- Platform: Windows
- Package: MSI

### Paso 2: Instalar
1. Ejecuta el archivo `.msi` descargado
2. Selecciona "Complete" installation
3. **IMPORTANTE**: Marca "Install MongoDB as a Service"
4. Marca "Install MongoDB Compass" (GUI opcional pero útil)

### Paso 3: Verificar instalación
```powershell
# Verifica el servicio
Get-Service MongoDB
```

Si está "Stopped", inícialo:
```powershell
Start-Service MongoDB
```

### Paso 4: Ejecutar la ingesta
```powershell
cd "c:\Users\isma1\Desktop\Viewnext\Proyecto Hackaton"
python ingest_games_to_mongodb.py
```

---

## Opción 3: MongoDB Atlas (Cloud - Gratis)

Si prefieres no instalar nada localmente:

### Paso 1: Crear cuenta
1. Ve a https://www.mongodb.com/cloud/atlas/register
2. Crea cuenta gratuita

### Paso 2: Crear cluster
1. Selecciona el tier **FREE** (M0)
2. Región: Closest to you
3. Cluster Name: gamebot-cluster

### Paso 3: Configurar acceso
1. Database Access → Add New Database User
   - Username: `gamebot`
   - Password: (genera una segura)
   
2. Network Access → Add IP Address
   - Allow access from anywhere: `0.0.0.0/0` (para desarrollo)

### Paso 4: Obtener connection string
1. Cluster → Connect → Connect your application
2. Copia la URI: `mongodb+srv://gamebot:<password>@...`

### Paso 5: Actualizar `.env`
```dotenv
MONGODB_URI=mongodb+srv://gamebot:<password>@gamebot-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=videogames_recommender
```

### Paso 6: Ejecutar la ingesta
```powershell
python ingest_games_to_mongodb.py
```

---

## 🚀 Verificar que funciona

Una vez MongoDB esté corriendo, prueba:

```powershell
# Instalar pymongo si no lo tienes
pip install pymongo

# Ejecutar la ingesta
python ingest_games_to_mongodb.py
```

Deberías ver:
```
================================================================================
  🎮 PIPELINE DE INGESTA: STEAM + GG.DEALS → MONGODB
================================================================================

🔧 Inicializando pipeline...
   MongoDB: mongodb://localhost:27017
   Base de datos: videogames_recommender
   Región de precios: EU (euros)

📋 Juegos a procesar: 100

📥 Obteniendo datos de 100 juegos desde Steam...
   [1/100] ✅ Cyberpunk 2077
   [2/100] ✅ Elden Ring
   ...
```

---

## 📊 Ver los datos (opcional)

### Con MongoDB Compass (GUI)
1. Abre MongoDB Compass
2. Conecta a: `mongodb://localhost:27017`
3. Base de datos: `videogames_recommender`
4. Colección: `games`

### Con mongo shell
```powershell
# Si tienes mongosh instalado
mongosh

use videogames_recommender
db.games.count()
db.games.findOne()
```

### Con Python
```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['videogames_recommender']

print(f"Total juegos: {db.games.count_documents({})}")
print(f"Con precios: {db.games.count_documents({'current_price_retail': {'$ne': None}})}")
```
