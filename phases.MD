FASE 0 - DEFINICION DEL PRODUCTO
===============================

## 0.1 VISIÓN DEL PRODUCTO

**"Asistente de IA conversacional para Telegram, con memoria persistente, personalidad configurable y capacidades de agente, operando completamente con modelos locales."**

---

## 0.2 PERSONA DEL BOT

El bot no es un asistente genérico. Tiene una **identidad definida**:

| Atributo | Decisión |
|---|---|
| **Nombre** | `CustomPerezBot` (o el que defina el dueño) |
| **Tono base** | Profesional pero cercano, claro y directo |
| **Idioma principal** | Español (detecta y responde en el idioma del usuario) |
| **Personalidad** | 100% configurable via DB (system prompt dinámico) |
| **Propósito** | Asistente técnico personal para programación, análisis y productividad |

---

## 0.3 CATÁLOGO DE CAPACIDADES (Priorizado)

### PRIORIDAD P0 — Esencial (MVP)

| # | Capacidad | Descripción |
|---|---|---|
| 1 | **Responder menciones en grupos** | Detecta `@bot` o reply a mensaje del bot y responde en el hilo |
| 2 | **Responder mensajes privados** | Chat 1:1 completo con el bot |
| 3 | **Personalidad configurable** | System prompt, temperatura, max_tokens por personalidad, seleccionable por chat |
| 4 | **Memoria de conversación** | Contexto de últimos N mensajes (ventana deslizante) |
| 5 | **Memoria a largo plazo** | Hechos importantes persistentes con búsqueda semántica (embeddings + Qdrant) |
| 6 | **Comprensión de documentos** | Subir PDF/TXT/MD, el bot lo aprende y puede responder sobre su contenido (RAG) |
| 7 | **Búsqueda en internet** | Busca información actualizada cuando se le solicita explícitamente |
| 8 | **Generación de código** | Escribe, explica y depura código en múltiples lenguajes |
| 9 | **Moderación de grupos** | Detecta y elimina spam, insultos o contenido prohibido (configurable por grupo) |
| 10 | **Análisis de mensajes** | Resumir conversaciones, extraer conclusiones, detectar temas |

### PRIORIDAD P1 — Importante (Post-MVP)

| # | Capacidad | Descripción |
|---|---|---|
| 11 | **Agente programador** | Ejecuta código en sandbox, devuelve resultados |
| 12 | **Agente investigador** | Busca, sintetiza y cita fuentes automáticamente |
| 13 | **Agente analista** | Procesa datos (CSV, JSON) y genera reportes |
| 14 | **Sistema de feedback** | 👍/👎 en respuestas para mejorar calidad |
| 15 | **Multi-personalidad por chat** | Cada grupo/usuario puede tener su propia personalidad asignada |

### PRIORIDAD P2 — Avanzado

| # | Capacidad | Descripción |
|---|---|---|
| 16 | **Fine-tuning con LoRA** | Entrenamiento sobre datos de conversaciones reales |
| 17 | **RLHF** | Optimización con feedback humano |
| 18 | **Plugins / comandos personalizados** | Sistema extensible de comandos custom |
| 19 | **Análisis de sentimiento** | Detectar estado emocional del usuario y adaptar tono |

### PRIORIDAD P3 — Escalado

| # | Capacidad | Descripción |
|---|---|---|
| 20 | **Multi-modelo** | Routing a modelo especializado según tarea |
| 21 | **Cluster de inferencia** | vLLM distribuido para alta concurrencia |
| 22 | **Dashboard web** | UI para monitorear conversaciones, ajustar personalidades, ver métricas |

---

## 0.4 MODOS DE INTERACCIÓN

### Modo 1: Mención en grupo
```
Usuario: @CustomPerezBot ¿cómo ordeno un array en Python?
Bot:     Para ordenar un array en Python puedes usar sorted() o .sort().
         ¿Quieres que te ponga un ejemplo?
```

### Modo 2: Reply al bot
```
Usuario: [responde a mensaje previo del bot] Explícame mejor
Bot:     Claro. Te lo explico paso a paso...
```

### Modo 3: Mensaje privado
```
Usuario: [abre chat con el bot] Hola, ¿qué puedes hacer?
Bot:     ¡Hola! Soy tu asistente. Puedo ayudarte con...
```

### Modo 4: Comando directo
```
Usuario: /resumen
Bot:     [genera resumen de los últimos mensajes del grupo]
```

```
Usuario: /buscar ¿qué es FastAPI?
Bot:     [busca en internet y responde con resumen + fuentes]
```

```
Usuario: /modo programador
Bot:     Cambiado a modo programador. Ahora mis respuestas serán más técnicas.
```

### Modo 5: Moderación (automático, sin invocación)
```
Usuario: [envía mensaje con spam/injurias]
Bot:     [detecta automáticamente] ❌ Mensaje eliminado por infringir normas del grupo.
         (solo visible para admins)
```

---

## 0.5 FLUJOS DETALLADOS

### Flujo A: Consulta con contexto (el más común)

```
Usuario menciona al bot en grupo o escribe al DM
        │
        ▼
┌─────────────────────────────┐
│  1. RECEPCIÓN               │
│  - Aiogram recibe update     │
│  - FastAPI procesa webhook   │
│  - Extrae: usuario, chat,    │
│    mensaje, idioma           │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│  2. PRE-FILTRO              │
│  - RateLimit check          │
│  - Anti-spam check          │
│  - Moderación (contenido    │
│    prohibido?)              │
│  - Auth check               │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│  3. ANÁLISIS DE INTENCIÓN   │
│  - ¿Es pregunta, petición,  │
│    comando, conversación?   │
│  - Clasificar tipo:         │
│    • código                 │
│    • búsqueda               │
│    • documento              │
│    • análisis               │
│    • charla general         │
│  - Detectar entidades       │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│  4. RECUPERACIÓN CONTEXTO   │
│  - Memoria corta: últimos   │
│    20 mensajes del chat     │
│  - Memoria larga: búsqueda  │
│    semántica en Qdrant      │
│    (hechos relevantes)      │
│  - RAG: si hay documentos   │
│    vinculados al chat,      │
│    buscar en ellos          │
│  - Personalidad: cargar     │
│    system prompt asignado   │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│  5. GENERACIÓN              │
│  - Construir prompt final   │
│    (system + contexto +     │
│    historial + pregunta)    │
│  - Enviar a modelo (vLLM)   │
│  - Stream o batch response  │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│  6. POST-PROCESAMIENTO      │
│  - Guardar mensaje + resp.  │
│    en DB                    │
│  - Generar embedding y      │
│    almacenar en Qdrant      │
│  - Detectar hechos          │
│    importantes para memoria │
│    larga                    │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│  7. ENTREGA                 │
│  - Enviar respuesta a       │
│    Telegram                 │
│  - Si es grupo: responder   │
│    en hilo (reply)          │
└─────────────────────────────┘
```

### Flujo B: Subida y aprendizaje de documento

```
Usuario: @bot /aprende [adjunta PDF]
        │
        ▼
1. Validar tipo de archivo (PDF/TXT/MD)
2. Descargar archivo de Telegram
3. Extraer texto (pdfplumber / PyMuPDF)
4. Chunking inteligente (~500 tokens con overlap 50)
5. Generar embeddings por chunk (sentence-transformers)
6. Almacenar en Qdrant con metadatos:
   - chat_id, user_id, source, chunk_index
7. Respuesta: "✅ Documento aprendido. Ya puedo responder sobre él."
```

### Flujo C: Búsqueda en internet

```
Usuario: @bot /buscar últimas noticias de IA 2026
        │
        ▼
1. Extraer query de búsqueda
2. Llamar a API de búsqueda web (configurable)
3. Obtener top N resultados
4. Resumir contenido relevante con el modelo
5. Responder con resumen + fuentes citadas
```

### Flujo D: Moderación automática

```
(En segundo plano, por cada mensaje en grupos moderados)
        │
        ▼
1. Evaluar mensaje contra policy del grupo:
   - Palabras prohibidas (lista configurable)
   - Patrones de spam (URLs repetidas, caracteres extraños)
   - Análisis de sentimiento (opcional)
2. Si viola política:
   - Eliminar mensaje
   - Notificar al admin (DM)
   - Opcional: warn/ban al usuario
3. Si no viola: no hacer nada (fluir normal)
```

### Flujo E: Conversación multi-turno (con memoria)

```
Usuario 1: @bot ¿cuál era el proyecto del que hablamos ayer?
        │
        ▼
1. Embedding de la pregunta
2. Búsqueda semántica en Qdrant (memoria larga)
3. Encontrar hecho relevante: "Usuario X está trabajando en
   una API de pagos con FastAPI"
4. Incorporar al contexto
5. Respuesta: "El proyecto de API de pagos con FastAPI.
   ¿Necesitas que revisemos algo en concreto?"
```

---

## 0.6 DECISIONES CLAVE TOMADAS

| Decisión | Opción elegida | Motivo |
|---|---|---|
| **Modelo base** | Modelo local via vLLM | Privacidad total, sin costos por token, latencia controlable |
| **Framework bot** | Aiogram 3.x | Async nativo, más moderno que python-telegram-bot, buena integración con FastAPI |
| **Webhook vs Polling** | Webhook | Producción, menor latencia, sin consumo innecesario de recursos |
| **API HTTP** | FastAPI | Rendimiento, tipado con Pydantic, documentación automática |
| **Vector DB** | Qdrant | Más rápido que ChromaDB en producción, soporta filtrado, API nativa |
| **Memoria corta** | Últimos 20 mensajes (ventana) | Balance entre contexto útil y tokens de entrada |
| **Memoria larga** | Embeddings + Qdrant + importance scoring | Permite recuperar información relevante aunque no sea exacta |
| **Idioma** | Multilenguaje (detección automática) | El usuario habla en su idioma, el bot responde en ese idioma |
| **Búsqueda web** | API externa (configurable) | Evita depender de un solo proveedor |
| **Cola de mensajes** | Redis Streams (primera versión) | Menos sobrecarga que RabbitMQ inicialmente, escalable después |
| **Personalidad** | System prompt en DB | Cambio sin reentrenar, asignable por chat/usuario |

---

## 0.7 LÍMITES DEL PRODUCTO (Qué NO hará)

| Fuera de alcance (P0-P1) | Razón |
|---|---|
| **Generación de imágenes** | Requiere modelos adicionales pesados |
| **Llamadas de voz/video** | No es un asistente de voz, es texto |
| **Ejecución de código remota** | Inseguro; se hará en sandbox controlado (Fase 10) |
| **Integración con otras plataformas** | Solo Telegram en v1 (Discord/WhatsApp en v2) |
| **Entrenamiento desde cero** | Fine-tuning sobre modelos existentes, no pre-training |
| **Dashboard web** | Prioridad baja (P3); el bot se administra por comandos |

---

## 0.8 MÉTRICAS DE ÉXITO

| Métrica | Objetivo | Cómo se mide |
|---|---|---|
| **Tasa de respuesta** | >95% de mensajes respondidos exitosamente | Logs de errores / total mensajes |
| **Tiempo de respuesta** | <3 segundos (p50), <8 segundos (p95) | Latencia registrada en cada respuesta |
| **Relevancia** | >80% de respuestas útiles según feedback | Ratings 👍/👎 |
| **Memoria** | Recall correcto de hechos en >85% de casos | Tests de memoria periódicos |
| **Moderación** | Falsos positivos <5% | Revisión manual periódica |
| **Uptime** | >99.5% (max 3.5h downtime/mes) | Healthchecks + Prometheus |

---

## 0.9 PÚBLICO OBJETIVO Y CASOS DE USO TÍPICOS

### Perfil 1: Desarrollador individual
- Usa el bot en DM para consultas técnicas
- Sube documentación técnica (PDFs de APIs, specs)
- Pide generación y revisión de código
- **Frecuencia:** varias veces al día

### Perfil 2: Grupo técnico de trabajo
- Bot en grupo de Telegram del equipo
- Responde dudas técnicas, modera spam
- Mantiene contexto de conversaciones anteriores
- **Frecuencia:** constante durante horas laborales

### Perfil 3: Creador de contenido / Investigador
- Pide búsquedas en internet
- Solicita resúmenes de documentos largos
- Usa el bot como asistente de investigación
- **Frecuencia:** uso intensivo por sesiones

---

## 0.10 MODELO DE DATOS FUNCIONAL

(No es el esquema SQL, sino qué datos se gestionan)

```
Usuario
  ├── Telegram ID
  ├── Preferencias (personalidad asignada, idioma)
  ├── Conversaciones
  │     ├── Mensajes (cada interacción)
  │     └── Memoria a largo plazo (hechos + embeddings)
  └── Documentos subidos (fuente de RAG)

Chat (grupo o DM)
  ├── Tipo (grupo/supergrupo/DM)
  ├── Configuración (moderación activa? personalidad?)
  ├── Miembros
  └── Historial de mensajes

Personalidad
  ├── System prompt
  ├── Parámetros (temperature, top_p, max_tokens)
  └── Asignaciones (a qué chats/usuarios aplica)
```

FASE 1 - DISEÑO DE ARQUITECTURA
==============================

## 1.1 ARQUITECTURA GENERAL (Diagrama de capas)

```
┌─────────────────────────────────────────────────────────┐
│                    TELEGRAM                              │
│              (Bot API + Webhook)                         │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS POST /webhook
                       ▼
┌─────────────────────────────────────────────────────────┐
│              CAPA DE ENTRADA (Nginx)                     │
│  - Proxy reverso                                        │
│  - Terminación SSL (Let's Encrypt)                      │
│  - Rate limiting a nivel HTTP                           │
│  - Solo disponible en producción                        │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│              CAPA DE API (FastAPI)                       │
│  ┌──────────────────────────────────────────────────┐    │
│  │  Webhook Handler  ←  Recibe updates de Telegram  │    │
│  │  Health Check     ←  /health, /ready             │    │
│  │  Metrics          ←  /metrics (Prometheus)       │    │
│  └──────────────────────┬───────────────────────────┘    │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              CAPA DE BOT (Aiogram)                       │
│  ┌──────────────────────────────────────────────────┐    │
│  │  Dispatcher (DP)   ←  Router de updates          │    │
│  │  Middleware Stack  ←  Auth, RateLimit, Logging   │    │
│  │  Filtros           ←  Menciones, commands, DM    │    │
│  │  Handlers          ←  Lógica por tipo de msg     │    │
│  └──────────────────────┬───────────────────────────┘    │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              CAPA DE SERVICIOS (Lógica de negocio)       │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ IntentService │  │ ContextService│  │ MemoryService │   │
│  │ - Clasifica   │  │ - Recupera   │  │ - Short-term  │   │
│  │   intención   │  │   contexto   │  │ - Long-term   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ RAGService   │  │ SearchService │  │ ModService   │   │
│  │ - Documentos │  │ - Web search │  │ - Moderación  │   │
│  │ - Embeddings │  │ - Scraping   │  │ - Anti-spam  │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│  ┌──────────────┐  ┌──────────────┐                      │
│  │ LLMService   │  │ Personality  │                      │
│  │ - Prompt     │  │ - System     │                      │
│  │   builder    │  │   prompts    │                      │
│  │ - vLLM call  │  │ - Params     │                      │
│  └──────────────┘  └──────────────┘                      │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              CAPA DE INFRAESTRUCTURA                     │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  PostgreSQL   │  │    Redis     │  │   Qdrant     │   │
│  │  - Datos      │  │  - Caché     │  │  - Vectores  │   │
│  │    relacional │  │  - Sesiones  │  │  - Embeddings│   │
│  │  - SQLAlchemy │  │  - RateLimit │  │  - Búsqueda  │   │
│  │  - Alembic    │  │  - Cola msgs │  │    semántica │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                          │
│  ┌──────────────┐                                        │
│  │   vLLM Server │                                       │
│  │  - Modelo LLM │                                       │
│  │  - Inferencia │                                       │
│  │  - API OpenAI │                                       │
│  │    compatible │                                       │
│  └──────────────┘                                        │
└─────────────────────────────────────────────────────────┘
```

---

## 1.2 FLUJO DE DATOS (Request → Response)

```
TELEGRAM
   │
   │  HTTP POST /webhook  { update_id, message, ... }
   ▼
NGINX (producción)
   │
   │  Proxy pass a FastAPI (localhost:8000)
   ▼
FASTAPI - WebhookHandler
   │
   │  1. Validar token secreto del webhook
   │  2. Parsear update (Pydantic)
   │  3. Pasar a Aiogram Dispatcher
   ▼
AIOGRAM - Dispatcher
   │
   │  4. Pasa por Middleware Stack:
   │     a) AuthMiddleware       → ¿usuario conocido? si no, crear
   │     b) RateLimitMiddleware  → ¿excede límite? si sí, 429
   │     c) LoggingMiddleware    → estructurar log entry
   │     d) ContextMiddleware    → cargar personalidad activa
   │
   │  5. Router determina handler según:
   │     - Tipo de chat (grupo/DM)
   │     - Tipo de mensaje (texto, comando, documento)
   │     - Mención o reply al bot
   ▼
HANDLER específico (ej: mensaje de texto)
   │
   │  6. IntentService.clasify(message)
   │     → código, búsqueda, documento, análisis, charla
   │
   │  7. ContextService.build(user, chat, message)
   │     → memoria corta: últimos 20 mensajes
   │     → memoria larga: búsqueda semántica en Qdrant
   │     → RAG: si hay documentos, buscar chunks relevantes
   │     → personalidad: system prompt asignado
   │
   │  8. LLMService.generate(prompt_final)
   │     → envía a vLLM (API compatible con OpenAI)
   │     → recibe respuesta (stream o completa)
   │
   │  9. Post-process:
   │     → guardar mensaje/respuesta en PostgreSQL
   │     → generar embedding con sentence-transformers
   │     → almacenar en Qdrant (para memoria futura)
   │     → detectar hechos importantes (importance scoring)
   │
   │ 10. Enviar respuesta a Telegram via Aiogram
   ▼
TELEGRAM - Usuario recibe respuesta
```

---

## 1.3 ESTRUCTURA DE CARPETAS (Código)

```
telegram-ai-bot/
│
├── docker/                       # Configuración Docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env.example
│
├── src/
│   ├── main.py                   # Entry point (FastAPI + Aiogram)
│   │
│   ├── api/                      # Capa de API (FastAPI)
│   │   ├── __init__.py
│   │   ├── app.py                # Creación de la app FastAPI
│   │   ├── webhook.py            # Endpoint /webhook
│   │   ├── health.py             # Endpoints /health, /ready
│   │   └── metrics.py            # Endpoint /metrics
│   │
│   ├── bot/                      # Capa de Bot (Aiogram)
│   │   ├── __init__.py
│   │   ├── dispatcher.py         # Setup del Dispatcher
│   │   ├── middlewares/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py           # AuthMiddleware
│   │   │   ├── rate_limit.py     # RateLimitMiddleware
│   │   │   ├── logging.py        # LoggingMiddleware
│   │   │   └── context.py        # ContextMiddleware
│   │   ├── filters/
│   │   │   ├── __init__.py
│   │   │   ├── mention.py        # Filtro de menciones
│   │   │   └── command.py        # Filtro de comandos
│   │   └── handlers/
│   │       ├── __init__.py
│   │       ├── messages.py       # Handler de textos
│   │       ├── commands.py       # Handler de /comandos
│   │       ├── documents.py      # Handler de documentos
│   │       └── moderation.py     # Handler de moderación
│   │
│   ├── services/                 # Capa de servicios (lógica)
│   │   ├── __init__.py
│   │   ├── intent_service.py     # Clasificación de intención
│   │   ├── context_service.py    # Construcción de contexto
│   │   ├── memory_service.py     # Gestión de memoria corta/larga
│   │   ├── rag_service.py        # RAG: ingesta y consulta
│   │   ├── search_service.py     # Búsqueda web
│   │   ├── moderation_service.py # Moderación y anti-spam
│   │   ├── llm_service.py        # Comunicación con vLLM
│   │   └── personality_service.py# Gestión de personalidades
│   │
│   ├── models/                   # Modelos de datos (Pydantic)
│   │   ├── __init__.py
│   │   ├── telegram.py           # Schemas de Telegram
│   │   ├── user.py               # Schema de usuario
│   │   ├── chat.py               # Schema de chat
│   │   └── messages.py           # Schema de mensajes
│   │
│   ├── db/                       # Capa de base de datos
│   │   ├── __init__.py
│   │   ├── session.py            # Engine + SessionFactory
│   │   ├── models/               # Modelos SQLAlchemy
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── chat.py
│   │   │   ├── message.py
│   │   │   ├── conversation.py
│   │   │   ├── personality.py
│   │   │   ├── memory.py
│   │   │   └── document.py
│   │   └── migrations/           # Alembic
│   │       ├── alembic.ini
│   │       ├── env.py
│   │       └── versions/
│   │
│   ├── vector/                   # Capa de vectores (Qdrant)
│   │   ├── __init__.py
│   │   ├── client.py             # Cliente Qdrant
│   │   ├── embeddings.py         # Generación de embeddings
│   │   └── collections.py        # Gestión de colecciones
│   │
│   ├── cache/                    # Capa de caché (Redis)
│   │   ├── __init__.py
│   │   ├── client.py             # Cliente Redis
│   │   ├── rate_limiter.py       # Rate limiting
│   │   └── message_queue.py      # Cola de mensajes (Streams)
│   │
│   └── core/                     # Core compartido
│       ├── __init__.py
│       ├── config.py             # Configuración centralizada
│       ├── logger.py             # Logger estructurado
│       └── exceptions.py         # Excepciones personalizadas
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_intent_service.py
│   │   ├── test_context_service.py
│   │   ├── test_llm_service.py
│   │   └── test_memory_service.py
│   ├── integration/
│   │   ├── test_webhook.py
│   │   ├── test_db.py
│   │   └── test_qdrant.py
│   └── conftest.py
│
├── requirements/
│   └── requirements.txt
│
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

---

## 1.4 TECNOLOGÍAS (Decisiones finales)

### Lenguaje y runtime

| Tecnología | Versión | Decisión |
|---|---|---|
| **Python** | 3.13+ | Async nativo, tipado fuerte, ecosistema IA maduro |
| **UV** | latest | Gestor de paquetes ultra-rápido (alternativa a pip/poetry) |

### Backend

| Tecnología | Decisión | Alternativas descartadas | Motivo |
|---|---|---|---|
| **FastAPI** | ✅ Elegido | Flask, Django | Async nativo, validación Pydantic v2, OpenAPI automático, rendimiento |
| **Aiogram 3.x** | ✅ Elegido | python-telegram-bot | Async de fábrica, mejor manejo de middlewares, filtros avanzados |
| **Pydantic v2** | ✅ Elegido | — | Validación y serialización tipada, integración nativa con FastAPI |
| **Uvicorn** | ✅ Elegido | Gunicorn | ASGI server para FastAPI, alto rendimiento |
| **Structlog** | ✅ Elegido | loguru, logging | Logs estructurados en JSON, integración con Prometheus |

### Base de datos

| Tecnología | Decisión | Alternativas descartadas | Motivo |
|---|---|---|---|
| **PostgreSQL 16** | ✅ Elegido | MySQL, SQLite | Robustez, tipos JSONB, performance, madurez |
| **SQLAlchemy 2.0** | ✅ Elegido | TortoiseORM, DjangoORM | Async support, patrón Unit of Work, flexible |
| **Alembic** | ✅ Elegido | — | Migraciones automáticas desde SQLAlchemy models |
| **Redis 7** | ✅ Elegido | Memcached | Caché + rate limiting + cola de mensajes, multipropósito |
| **Qdrant** | ✅ Elegido | ChromaDB, Pinecone, Weaviate | Open source, filtrado nativo, API REST+gRPC, rendimiento en producción |

### IA / Machine Learning

| Tecnología | Decisión | Alternativas descartadas | Motivo |
|---|---|---|---|
| **vLLM** | ✅ Elegido | Ollama, Transformers directo, TGI | Optimizado para producción: PagedAttention, batching dinámico, API compatible OpenAI |
| **Sentence-Transformers** | ✅ Elegido | OpenAI Embeddings, Cohere | Local, gratuito, sin dependencia externa |
| **PyTorch** | ✅ Elegido | TensorFlow, JAX | Ecosistema HuggingFace, comunidad dominante |

### Observabilidad

| Tecnología | Decisión | Motivo |
|---|---|---|
| **Prometheus** | ✅ Elegido | Estándar de facto para métricas |
| **Grafana** | ✅ Elegido | Dashboards visuales, alertas |
| **Sentry** | ✅ Elegido | Error tracking con contexto, alertas en tiempo real |

### Infraestructura

| Tecnología | Decisión | Motivo |
|---|---|---|
| **Docker Compose** | ✅ Elegido | Orquestación simple para desarrollo y producción small |
| **Nginx** | ✅ Elegido | Proxy reverso, SSL termination, static files |
| **Let's Encrypt** | ✅ Elegido | SSL gratis, automatizable con certbot |

---

## 1.5 DIAGRAMA DE CONTENEDORES (Docker Compose)

```
┌─────────────────────────────────────────────────────────────────┐
│                        DOCKER COMPOSE NETWORK                    │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │    nginx     │───▶│     api      │───▶│  postgres    │       │
│  │  :443→:8000  │    │  FastAPI     │    │  :5432       │       │
│  │  SSL         │    │  Aiogram     │    │  SQLAlchemy  │       │
│  └──────────────┘    │  Services    │    └──────────────┘       │
│                      │              │    ┌──────────────┐       │
│                      │              │───▶│    redis     │       │
│                      │              │    │  :6379       │       │
│                      │              │    │  Caché+Cola  │       │
│                      │              │    └──────────────┘       │
│                      │              │    ┌──────────────┐       │
│                      │              │───▶│   qdrant     │       │
│                      │              │    │  :6333       │       │
│                      │              │    │  Vectores    │       │
│                      │              │    └──────────────┘       │
│                      │              │    ┌──────────────┐       │
│                      │              │───▶│    vllm      │       │
│                      │              │    │  :8001       │       │
│                      │              │    │  LLM API     │       │
│                      │              │    └──────────────┘       │
│                      └──────────────┘                           │
│                                                                  │
│  Volúmenes: postgres_data, redis_data, qdrant_data, vllm_models │
│  Red: internal (bridge)                                          │
└─────────────────────────────────────────────────────────────────┘
```

**Comunicación entre contenedores:**
- `api → postgres`: SQLAlchemy async (via asyncpg)
- `api → redis`: redis-py async
- `api → qdrant`: qdrant-client (gRPC para producción)
- `api → vllm`: httpx (API compatible OpenAI: `/v1/chat/completions`)

---

## 1.6 DECISIONES DE ARQUITECTURA (Architecture Decision Records - ADR)

### ADR-001: Webhook sobre Polling
**Contexto:** Telegram soporta dos métodos para recibir updates: long polling y webhooks.
**Decisión:** Usar webhook.
**Consecuencia:**
- ✅ Menor latencia (Telegram nos llama cuando hay update)
- ✅ Menor consumo de recursos (sin loop constante)
- ✅ Escala mejor (Telegram maneja reintentos)
- ❌ Requiere HTTPS y puerto accesible
- ❌ Más complejo en desarrollo local (ngrok o túnel)

### ADR-002: Redis como cola de mensajes (no RabbitMQ)
**Contexto:** Necesitamos desacoplar la recepción de mensajes del procesamiento pesado (IA).
**Decisión:** Usar Redis Streams en lugar de RabbitMQ para la primera versión.
**Consecuencia:**
- ✅ Menos servicios que mantener (Redis ya está en la stack)
- ✅ Suficiente para volumen inicial (cientos de msg/min)
- ✅ Redis Streams soporta consumer groups, ACKs, y persistencia
- ❌ Si el volumen crece a miles de msg/min, migrar a RabbitMQ
- ❌ No tiene dead-letter queues nativas (implementar manual)

### ADR-003: API compatible OpenAI para vLLM
**Contexto:** El servicio LLM necesita comunicarse con el modelo de IA.
**Decisión:** vLLM expone API compatible con OpenAI (`/v1/chat/completions`), lo usamos directamente.
**Consecuencia:**
- ✅ Podemos cambiar de vLLM a cualquier otro servidor compatible (TGI, Ollama) sin cambiar código
- ✅ Librería `openai` Python funciona directamente
- ✅ Streaming support nativo (Server-Sent Events)
- ❌ Dependemos de que vLLM mantenga compatibilidad

### ADR-004: Embeddings locales con Sentence-Transformers
**Contexto:** Necesitamos generar vectores de texto para búsqueda semántica.
**Decisión:** Usar sentence-transformers local (modelo `paraphrase-multilingual-MiniLM-L12-v2`).
**Consecuencia:**
- ✅ Sin costos de API externa
- ✅ Latencia mínima (local, sin red)
- ✅ Modelo multilingüe (español incluido)
- ❌ Mayor uso de RAM/VRAM
- ❌ Calidad de embeddings inferior a modelos grandes (text-embedding-3-large)

### ADR-005: Memoria de ventana fija (no resumen)
**Contexto:** La memoria corta necesita mantener contexto de conversación.
**Alternativas:** (a) ventana fija de N mensajes, (b) resumen automático cada N mensajes, (c) sliding window con importance scoring.
**Decisión:** Ventana fija de 20 mensajes (toda la conversación reciente). En el futuro, combinar con resumen automático cuando exceda el límite.
**Consecuencia:**
- ✅ Simple de implementar
- ✅ Predecible en consumo de tokens
- ❌ Pierde contexto de mensajes antiguos (solucionado por memoria larga + Qdrant)

### ADR-006: Columna de importancia en memoria larga
**Contexto:** No todos los hechos conversacionales son igual de relevantes.
**Decisión:** Cada entrada de memoria larga tiene un score de importancia (0.0-1.0) calculado al momento de creación. La recuperación prioriza facts con mayor importancia.
**Consecuencia:**
- ✅ Mejor calidad de contexto recuperado
- ✅ Podemos hacer pruning automático (borrar facts con importancia < 0.3)
- ❌ Costo computacional extra al guardar cada mensaje

---

## 1.7 CONFIGURACIÓN CENTRALIZADA (Variables de entorno)

| Variable | Descripción | Default | Obligatoria |
|---|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram | — | ✅ |
| `TELEGRAM_WEBHOOK_SECRET` | Secreto para validar webhooks | — | ✅ |
| `TELEGRAM_WEBHOOK_URL` | URL pública del webhook | — | ✅ (prod) |
| `DATABASE_URL` | URL de conexión PostgreSQL | `postgresql+asyncpg://...` | ✅ |
| `REDIS_URL` | URL de conexión Redis | `redis://redis:6379/0` | ✅ |
| `QDRANT_URL` | URL de conexión Qdrant | `http://qdrant:6333` | ✅ |
| `VLLM_URL` | URL de la API de vLLM | `http://vllm:8001/v1` | ✅ |
| `VLLM_MODEL_NAME` | Nombre del modelo en vLLM | `Qwen/Qwen2.5-7B-Instruct` | ✅ |
| `VLLM_API_KEY` | API key para vLLM (si requiere auth) | — | ❌ |
| `EMBEDDING_MODEL` | Modelo de sentence-transformers | `paraphrase-multilingual-MiniLM-L12-v2` | ❌ |
| `MEMORY_WINDOW_SIZE` | Tamaño de ventana de memoria corta | `20` | ❌ |
| `RATE_LIMIT_MSG_PER_MIN` | Máximo de mensajes por minuto por usuario | `10` | ❌ |
| `LOG_LEVEL` | Nivel de logging | `INFO` | ❌ |
| `SENTRY_DSN` | DSN de Sentry para error tracking | — | ❌ |
| `SEARCH_API_KEY` | API key para búsqueda web | — | ❌ |
| `SEARCH_API_URL` | URL del proveedor de búsqueda | — | ❌ |
| `ENVIRONMENT` | `development`, `staging`, `production` | `development` | ❌ |

---

## 1.8 ESTRATEGIA DE COMUNICACIÓN ENTRE SERVICIOS

| Origen → Destino | Protocolo | Librería | Formato |
|---|---|---|---|
| **Aiogram → FastAPI** | En-proceso (misma app) | Llamada directa | Python objects |
| **FastAPI → PostgreSQL** | TCP (async) | asyncpg via SQLAlchemy | SQL + JSON |
| **FastAPI → Redis** | TCP (async) | redis-py async | Redis protocol + JSON |
| **FastAPI → Qdrant** | gRPC (producción) / REST (dev) | qdrant-client | Protobuf / JSON |
| **FastAPI → vLLM** | HTTP (async) | httpx | JSON (API OpenAI) |
| **FastAPI → Nginx** | HTTP (desde contenedor) | — | HTTP/1.1 |
| **FastAPI → Telegram** | HTTP (async) | Aiogram (httpx) | JSON (Bot API) |

---

## 1.9 ESTRATEGIA DE CONCURRENCIA

| Componente | Estrategia | Detalle |
|---|---|---|
| **FastAPI** | AsyncIO + workers Uvicorn | 1 worker con event loop (o 2-4 workers si es necesario) |
| **Aiogram** | AsyncIO (mismo event loop) | Comparte event loop con FastAPI |
| **vLLM** | Batching dinámico automático | vLLM agrupa requests en lotes para eficiencia |
| **Redis** | Single-threaded (event loop interno) | Maneja colas sin bloqueo |
| **PostgreSQL** | Connection pool (async) | Pool de 10-20 conexiones |
| **Qdrant** | gRPC streaming + batching | Optimizado para alta concurrencia |

**Manejo de picos de tráfico:**
1. Redis Rate Limiter rechaza requests que excedan el límite
2. Redis Streams encola mensajes cuando el sistema está saturado
3. El servicio LLM procesa en batches (vLLM lo maneja automáticamente)
4. Si la cola crece demasiado, se pueden escalar workers horizontalmente

---

## 1.10 ESTRATEGIA DE ERRORES Y REINTENTOS

| Error | Comportamiento | Reintento |
|---|---|---|
| **vLLM timeout** | Reintentar 2 veces con backoff (1s, 3s) | Sí (máx 2) |
| **Qdrant caído** | Degradación: responder sin memoria larga | No, log error |
| **PostgreSQL caído** | Degradación: responder sin persistencia | No, log crítico |
| **Redis caído** | Degradación: sin caché ni rate limit | No, log error |
| **Telegram API error** | Reintentar 3 veces con backoff exponencial | Sí (máx 3) |
| **Web search falla** | Degradación: "No pude buscar en este momento" | No, responder sin búsqueda |
| **Rate limit excedido** | Responder: "⏳ Demasiadas solicitudes. Espera un momento." | No |

---

## 1.11 SEGURIDAD EN LA ARQUITECTURA

| Capa | Medida |
|---|---|
| **Red** | Docker network interna, solo Nginx expone puertos |
| **Nginx** | Rate limiting, tamaño máximo de body, timeout configurable |
| **Webhook** | Secreto compartido para validar origen (Telegram → nuestro server) |
| **API** | Solo responde a webhook de Telegram (por IP si es posible) |
| **vLLM** | API key opcional, solo accesible desde la red interna |
| **PostgreSQL** | Sin puerto expuesto externamente, usuario dedicado por servicio |
| **Redis** | Requiere contraseña (configurable), sin persistence commands |
| **Secrets** | Todas las credenciales via variables de entorno, nunca en código |

---

## 1.12 REQUISITOS DE HARDWARE (Estimación)

### Componente crítico: vLLM (modelo 7B)

| Recurso | Mínimo | Recomendado |
|---|---|---|
| **RAM** | 16 GB | 32 GB |
| **VRAM (GPU)** | 8 GB (modelo 7B cuantizado) | 24 GB (modelo 7B full precision + batch) |
| **CPU** | 4 cores | 8 cores |
| **Disco** | 20 GB SSD (modelos) | 50 GB SSD |
| **GPU** | No obligatorio (CPU inference) | RTX 3090 / A10G / A100 |

### Stack completo (sin GPU)

| Servicio | RAM estimada |
|---|---|
| FastAPI + Aiogram | ~200 MB |
| PostgreSQL | ~500 MB |
| Redis | ~100 MB |
| Qdrant | ~300 MB |
| vLLM (CPU, 7B) | ~14 GB |
| **Total** | **~15 GB RAM** |

### Stack completo (con GPU)

| Servicio | RAM estimada |
|---|---|
| FastAPI + Aiogram | ~200 MB |
| PostgreSQL | ~500 MB |
| Redis | ~100 MB |
| Qdrant | ~300 MB |
| vLLM (GPU, 7B) | ~6 GB RAM + ~8 GB VRAM |
| **Total** | **~7 GB RAM + 8 GB VRAM** |

---

## 1.13 COMPARATIVA: vLLM vs ALTERNATIVAS

| Aspecto | vLLM | Ollama | Transformers directo | TGI (HuggingFace) |
|---|---|---|---|---|
| **Rendimiento** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **Batching dinámico** | ✅ Sí | ❌ No | ❌ No | ✅ Sí |
| **API OpenAI compatible** | ✅ Sí | ✅ Sí | ❌ No | ✅ Sí |
| **PagedAttention** | ✅ Sí (núcleo) | ❌ No | ❌ No | ❌ No |
| **Facilidad setup** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Control de versión** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **LoRA adapters** | ✅ Sí | ❌ No | ✅ Sí (manual) | ⭐⭐⭐ |
| **Documentación** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Comunidad** | Grande y creciendo | Muy grande | Enorme | Mediana |

**Veredicto:** vLLM es la mejor opción para producción por su rendimiento con PagedAttention y batching dinámico. Ollama es mejor para desarrollo local rápido.

Ahora desarrollaremos la siguiente fase completa y avanzada por favor:

FASE 2 - INFRAESTRUCTURA
Crear repositorio

Configurar entorno

Dependencias principales

Docker

Servicios

Proporcioname todas las instrucciones, comandos, codigo si es necesario en esta fase, no hagas ninguna implementacion por tu cuenta, cualquier cosa de esta fase proporcioname todo a mi que yo lo hago por favor. 

FASE 3 - DISEÑO DE BASE DE DATOS
Tabla Users
id
telegram_id
username
first_name
language
is_active
created_at
updated_at
Tabla Chats
id
telegram_chat_id
chat_type
title
created_at
Tabla Messages
id
chat_id
user_id
role
content
tokens
created_at
Tabla Conversations
id
chat_id
title
created_at
Tabla Personalities
id
name
system_prompt
temperature
max_tokens
Tabla Memories
id
user_id
content
embedding_id
importance
Tabla Documents
id
name
file_path
status
created_at

FASE 4 - BOT TELEGRAM
Crear Bot

Usar:

BotFather

Telegram genera un token para acceder a la Bot API.
Configurar Webhook

Telegram
      ↓
Webhook
      ↓
FastAPI

No usar polling en producción.

Detectar menciones

Ejemplo:

@MiBot

o

respuesta al bot

Middleware

Implementar:

AuthMiddleware
LoggingMiddleware
RateLimitMiddleware
ContextMiddleware

FASE 5 - MOTOR DE IA

Aquí empieza la parte interesante.

Selección de modelo
Opción Local
Qwen 3
Llama 3
Mistral
DeepSeek
Gemma
Inferencia
Transformers
vLLM
Ollama

Yo elegiría:

vLLM

para producción.

FASE 6 - SISTEMA DE PERSONALIDAD

Cada personalidad será un System Prompt.

Ejemplo:

Eres TonyAI.

Especialista en programación.

Experto en:
- Python
- React
- NestJS

Siempre respondes de forma clara.

Configuración dinámica

Tabla:

personalities

Permite cambiar personalidad sin reentrenar.

FASE 7 - MEMORIA

Aquí se diferencia un chatbot simple de uno avanzado.

Memoria corta

Últimos mensajes.

20 mensajes

Memoria larga

Guardar:

Hechos importantes
Preferencias
Información histórica
Embeddings

Modelo:

sentence-transformers

Genera:

vector

de cada mensaje.

Almacenamiento
Qdrant
Recuperación

Cuando alguien pregunta:

¿Cuál era mi proyecto?

Se realiza:

Embedding
↓
Búsqueda semántica
↓
Contexto recuperado
↓
Respuesta IA

FASE 8 - RAG

Retrieval Augmented Generation.

Ingesta documental

Subir:

PDF
DOCX
TXT
Markdown
Pipeline
Documento
↓
Chunking
↓
Embeddings
↓
Qdrant
Consulta
Pregunta
↓
Búsqueda vectorial
↓
Contexto
↓
LLM

FASE 9 - DEEP LEARNING

Muchos proyectos no llegan aquí.

Dataset propio

Guardar:

pregunta
respuesta
feedback
Fine Tuning

Framework:

PyTorch
Transformers
PEFT
LoRA
QLoRA
Objetivo

Que la personalidad no dependa únicamente del prompt.

Entrenamiento
Dataset
↓
Tokenización
↓
Fine Tuning
↓
Modelo personalizado

FASE 10 - AGENTES

Dividir la IA en especialistas.

Agente Programador
Genera código
Agente Analista
Analiza datos
Agente Investigador
Busca información
Router
Mensaje
↓
Clasificador
↓
Agente adecuado

FASE 11 - FEEDBACK Y APRENDIZAJE

Cada respuesta recibe:

👍
👎

Guardar:

prompt
respuesta
rating

Utilizar posteriormente para:

RLHF
Fine Tuning

FASE 12 - SEGURIDAD
Rate Limiting
Redis
Anti Spam
Mensajes por minuto
Anti Prompt Injection

Filtrado de instrucciones.

Moderación

Detectar:

Spam
Insultos
Contenido ilegal

FASE 13 - OBSERVABILIDAD
Logs
Structlog
Métricas
Prometheus
Dashboards
Grafana
Errores
Sentry

FASE 14 - DESPLIEGUE
VPS

Opciones:

Hetzner

DigitalOcean

Contabo

Docker Compose
nginx
api
postgres
redis
qdrant
vllm
Producción
Nginx
SSL
Webhook HTTPS
Docker
Backups automáticos
CI/CD

FASE 15 - ESCALADO EMPRESARIAL

Arquitectura final:

Telegram
    ↓
Nginx
    ↓
FastAPI
    ↓
RabbitMQ
    ↓
Workers
    ↓
vLLM Cluster
    ↓
Qdrant
    ↓
PostgreSQL
    ↓
Redis
