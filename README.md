# 📚 Sistema RAG para Juegos (MongoDB + Milvus + LLM)

Este proyecto implementa un **sistema RAG (Retrieval-Augmented Generation)** completo y funcional cuyo objetivo es permitir consultas en lenguaje natural sobre información de juegos almacenada en una base de datos documental y enriquecida mediante modelos de lenguaje y búsqueda vectorial.

La solución integra **MongoDB** como fuente de datos primaria, **Milvus** como base de datos vectorial y **LLMs** tanto para la transformación semántica de los datos como para la generación final de respuestas, cubriendo así **todo el ciclo de vida de un sistema RAG moderno**.

---

## 🧠 Alcance funcional del sistema

La aplicación cubre de forma integral las siguientes etapas:

- **Ingesta de datos** desde una base de datos documental.
- **Transformación semántica** de datos estructurados (JSON) a texto natural.
- **Chunking semántico** con solapamiento para preservar contexto.
- **Vectorización** mediante embeddings.
- **Almacenamiento vectorial** en Milvus.
- **Recuperación híbrida** con expansión de consultas (*multi-query*).
- **Generación de respuestas** contextualizadas mediante un LLM.

Este enfoque permite responder preguntas complejas incluso cuando la información no aparece de forma literal en los datos originales.

---

## 🧠 Visión general del funcionamiento

A alto nivel, el sistema se organiza en **dos grandes fases bien diferenciadas**:

---

### 🔹 Fase 1: Ingesta de información

Durante esta fase el sistema prepara el conocimiento que posteriormente será consultado:

- Se recuperan documentos de juegos desde **MongoDB**.
- Cada documento JSON se transforma en un texto descriptivo rico y coherente utilizando un **modelo de lenguaje**, guiado por un prompt de sistema.
- El texto generado se concatena y se divide en fragmentos (*chunks*) de tamaño controlado con solapamiento para preservar continuidad semántica.
- Cada fragmento se convierte en un **embedding vectorial**.
- Los fragmentos y sus embeddings asociados se almacenan en una colección de **Milvus**.

El resultado es una base de conocimiento vectorizada, preparada para búsquedas semánticas eficientes.

---

### 🔹 Fase 2: Consulta y generación (RAG)

Esta fase se activa cuando el usuario realiza una pregunta:

- El usuario introduce una consulta en lenguaje natural.
- La consulta se expande automáticamente en varias reformulaciones semánticamente equivalentes (*multi-query*).
- Cada reformulación se vectoriza y se utiliza para ejecutar una búsqueda híbrida en Milvus.
- Los resultados se fusionan, deduplican y priorizan.
- Se construye un contexto limitado con los fragmentos más relevantes.
- El modelo de lenguaje genera una **respuesta final fundamentada exclusivamente en ese contexto**.

Este flujo reduce alucinaciones y mejora la precisión de las respuestas.

---

## 🧩 Arquitectura lógica del sistema

````
MongoDB
   │
   ▼
Transformación con LLM (JSON → texto natural)
   │
   ▼
Chunking semántico con solapamiento
   │
   ▼
Generación de embeddings
   │
   ▼
Milvus (Base de Datos Vectorial)
   │
   ▼
Búsqueda híbrida + Multi-query
   │
   ▼
LLM (Generación de respuesta final)
````

--- 

## 📂 Estructura del proyecto

```
.
├── main.py
│   └─ Punto de entrada de la aplicación y consola interactiva
│
├── process.py
│   └─ Lógica de ingesta, transformación semántica, chunking y vectorización
│
├── rag_pipeline.py
│   └─ Orquestación completa del pipeline RAG (multi-query, búsqueda y respuesta)
│
├── services.py
│   └─ Acceso a MongoDB, serialización de documentos y servicios externos

```

La separación modular facilita el mantenimiento, la extensibilidad y la evolución del sistema.
🚀 Flujo de ejecución detallado
## 1️⃣ Ingesta de datos

Durante la ingesta:

    Se consultan documentos de juegos desde MongoDB.

    Se limpian y serializan los documentos eliminando campos internos.

    Cada documento se transforma en texto natural usando un LLM.

    El texto se divide en fragmentos solapados para maximizar la recuperación semántica.

    Se generan embeddings para cada fragmento.

    Los datos se insertan en una colección de Milvus y se confirman mediante flush.

### ⚠️ Importante
La ingesta solo debe ejecutarse una vez por colección para evitar duplicados y ruido semántico.
## 2️⃣ Consulta RAG

Cuando el usuario consulta:

    Se recibe la pregunta en lenguaje natural.

    Se generan múltiples reformulaciones automáticas de la consulta.

    Cada reformulación se transforma en un embedding.

    Se ejecuta una búsqueda híbrida por cada reformulación.

    Los resultados se combinan y se eliminan duplicados.

    Se seleccionan los fragmentos más relevantes como contexto.

    El LLM genera la respuesta final basada únicamente en ese contexto.

Si no se recupera contexto relevante, el sistema responde de forma controlada indicando falta de información.
## 3️⃣ Pruebas del modelo

El sistema incluye un modo de prueba que permite:

    Realizar llamadas directas al modelo de lenguaje.

    Verificar conectividad, credenciales y comportamiento del LLM.

    Aislar problemas sin depender del pipeline RAG completo.

## 🖥️ Interfaz de uso

La aplicación se ejecuta desde consola mediante un menú interactivo:

CONSOLA DE RAG
1) Probar modelo
2) Preguntar con RAG
3) Ingestar datos de prueba en Milvus
4) Salir

Este menú permite:

    Validar el modelo LLM de forma independiente.

    Realizar consultas RAG sobre los datos indexados.

    Ejecutar la ingesta de datos de manera explícita y controlada.

## 🧪 Tecnologías utilizadas

    MongoDB Atlas → Almacenamiento de datos documentales

    Milvus → Base de datos vectorial para búsqueda semántica

    LLMs → Transformación de texto y generación de respuestas

    Embeddings → Representación numérica del significado

    LangChain utilities → Chunking y herramientas auxiliares

    Python → Lenguaje principal de implementación