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

FASE 2 - INFRAESTRUCTURA
========================

## Instrucciones de uso

Esta fase contiene **todo el código y comandos** que necesitas ejecutar manualmente en tu terminal para levantar la infraestructura del proyecto.

**Orden de ejecución recomendado:**
1. `2.1` → Crear repositorio y .gitignore
2. `2.2` → Configurar entorno Python
3. `2.3` → Crear `pyproject.toml` con dependencias
4. `2.4` → Crear estructura de carpetas
5. `2.5` → Crear archivos de configuración (.env, config.py)
6. `2.6` → Crear Dockerfile
7. `2.7` → Crear docker-compose.yml
8. `2.8` → Crear Nginx config
9. `2.9` → Crear scripts de desarrollo (Makefile)
10. `2.10` → Inicializar Alembic
11. `2.11` → Verificar que todo funciona

---

## 2.1 REPOSITORIO Y GIT

### Paso 1: Inicializar git (si no lo hiciste ya)

```bash
# Desde la raíz del proyecto
git init
git branch -M master
```

### Paso 2: Crear .gitignore

Crea el archivo `.gitignore` en la raíz con este contenido exacto:

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
*.egg
dist/
build/
.eggs/
*.whl

# Environment
.env
.venv/
venv/
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker
docker-compose.override.yml

# Logs
*.log

# Model files (too large for git)
models/
*.bin
*.pt
*.pth
*.gguf

# Testing
.coverage
htmlcov/
.pytest_cache/

# Alembic
src/db/migrations/versions/*.pyc

# Qdrant storage (local dev)
qdrant_storage/

# Postgres data (local dev)
pgdata/
```

---

## 2.2 ENTORNO PYTHON

### Paso 3: Crear y activar el entorno virtual

```bash
# Windows (PowerShell 7+)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 4: Instalar UV (gestor de paquetes ultra-rápido)

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 2.3 DEPENDENCIAS (pyproject.toml)

### Paso 5: Crear pyproject.toml

Crea `pyproject.toml` en la raíz. Este archivo reemplaza a `requirements.txt` y define todo el proyecto:

```toml
[project]
name = "telegram-ai-bot"
version = "0.1.0"
description = "Asistente de IA para Telegram con memoria, RAG y personalidad configurable"
requires-python = ">=3.13"
readme = "README.md"

dependencies = [
    # API
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",

    # Bot
    "aiogram>=3.14.0",

    # DB
    "sqlalchemy[asyncio]>=2.0.36",
    "alembic>=1.14.0",
    "asyncpg>=0.30.0",

    # Cache / Queue
    "redis[hiredis]>=5.2.0",

    # Vectores
    "qdrant-client>=1.12.0",

    # IA
    "sentence-transformers>=3.3.0",
    "torch>=2.5.0",

    # HTTP
    "httpx>=0.28.0",

    # Utilidades
    "pydantic>=2.10.0",
    "pydantic-settings>=2.6.0",
    "python-dotenv>=1.0.0",
    "structlog>=24.4.0",
    "python-multipart>=0.0.12",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=6.0.0",
    "ruff>=0.7.0",
    "mypy>=1.13.0",
    "pre-commit>=4.0.0",
    "ngrok>=1.2.0",
]

[tool.ruff]
target-version = "py313"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.13"
strict = true
ignore_missing_imports = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### Paso 6: Instalar dependencias

```bash
# Con UV (recomendado)
uv sync

# Con pip tradicional
pip install -e .
pip install -e ".[dev]"
```

---

## 2.4 ESTRUCTURA DE CARPETAS

### Paso 7: Crear toda la estructura del proyecto

Ejecuta estos comandos para crear todos los directorios necesarios:

```bash
# Directorios principales
mkdir -p src/api
mkdir -p src/bot/middlewares
mkdir -p src/bot/filters
mkdir -p src/bot/handlers
mkdir -p src/services
mkdir -p src/models
mkdir -p src/db/models
mkdir -p src/db/migrations/versions
mkdir -p src/vector
mkdir -p src/cache
mkdir -p src/core
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p docker/nginx
```

### Paso 8: Crear archivos __init__.py

Cada directorio de Python necesita un `__init__.py`. Crea todos con este comando:

```bash
# Crea __init__.py en cada subdirectorio de src/
New-Item -ItemType File -Path "src/api/__init__.py"
New-Item -ItemType File -Path "src/bot/__init__.py"
New-Item -ItemType File -Path "src/bot/middlewares/__init__.py"
New-Item -ItemType File -Path "src/bot/filters/__init__.py"
New-Item -ItemType File -Path "src/bot/handlers/__init__.py"
New-Item -ItemType File -Path "src/services/__init__.py"
New-Item -ItemType File -Path "src/models/__init__.py"
New-Item -ItemType File -Path "src/db/__init__.py"
New-Item -ItemType File -Path "src/db/models/__init__.py"
New-Item -ItemType File -Path "src/vector/__init__.py"
New-Item -ItemType File -Path "src/cache/__init__.py"
New-Item -ItemType File -Path "src/core/__init__.py"
New-Item -ItemType File -Path "tests/__init__.py"
New-Item -ItemType File -Path "tests/unit/__init__.py"
New-Item -ItemType File -Path "tests/integration/__init__.py"
```

*(En Linux/Mac usa `touch` en lugar de `New-Item -ItemType File`)*

---

## 2.5 CONFIGURACIÓN

### Paso 9: Crear .env.example

Crea `.env.example` en la raíz:

```bash
# Telegram
TELEGRAM_BOT_TOKEN=tu_token_aqui
TELEGRAM_WEBHOOK_SECRET=secret_aleatorio_64_chars_min
TELEGRAM_WEBHOOK_URL=https://tudominio.com/webhook

# Base de datos
DATABASE_URL=postgresql+asyncpg://botuser:botpass@postgres:5432/telegram_bot

# Redis
REDIS_URL=redis://:redispass@redis:6379/0

# Qdrant
QDRANT_URL=http://qdrant:6333
QDRANT_GRPC_PORT=6334

# vLLM
VLLM_URL=http://vllm:8001/v1
VLLM_MODEL_NAME=Qwen/Qwen2.5-7B-Instruct

# Embeddings
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2

# Memoria
MEMORY_WINDOW_SIZE=20

# Rate limiting
RATE_LIMIT_MSG_PER_MIN=10

# Logging
LOG_LEVEL=INFO

# Sentry (opcional)
SENTRY_DSN=

# Búsqueda web (opcional)
SEARCH_API_KEY=
SEARCH_API_URL=

# Entorno
ENVIRONMENT=development
```

Luego cópialo a `.env` para desarrollo:

```bash
Copy-Item .env.example .env   # Windows PowerShell
# cp .env.example .env        # Linux/Mac
```

### Paso 10: Crear módulo de configuración central

Crea `src/core/config.py` — este archivo carga toda la config desde variables de entorno usando Pydantic Settings:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Telegram
    telegram_bot_token: str
    telegram_webhook_secret: str
    telegram_webhook_url: str = ""

    # Database
    database_url: str = "postgresql+asyncpg://botuser:botpass@postgres:5432/telegram_bot"

    # Redis
    redis_url: str = "redis://:redispass@redis:6379/0"

    # Qdrant
    qdrant_url: str = "http://qdrant:6333"
    qdrant_grpc_port: int = 6334

    # vLLM
    vllm_url: str = "http://vllm:8001/v1"
    vllm_model_name: str = "Qwen/Qwen2.5-7B-Instruct"

    # Embeddings
    embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2"

    # Memory
    memory_window_size: int = 20

    # Rate limiting
    rate_limit_msg_per_min: int = 10

    # Logging
    log_level: str = "INFO"

    # Sentry
    sentry_dsn: str = ""

    # Search
    search_api_key: str = ""
    search_api_url: str = ""

    # Environment
    environment: str = "development"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


settings = Settings()
```

---

## 2.6 DOCKERFILE

### Paso 11: Crear Dockerfile

Crea `docker/Dockerfile`:

```dockerfile
FROM python:3.13-slim AS base

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Configurar Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Copiar dependencias primero (cache layer)
COPY pyproject.toml .
RUN uv sync --frozen --no-dev

# Copiar código fuente
COPY src/ src/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]


# --- Etapa de desarrollo (con hot reload) ---
FROM base AS dev

RUN uv sync --frozen

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

## 2.7 DOCKER COMPOSE

### Paso 12: Crear docker-compose.yml

Crea `docker/docker-compose.yml`:

```yaml
services:

  api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
      target: dev
    container_name: telegram-bot-api
    ports:
      - "8000:8000"
    env_file:
      - ../.env
    volumes:
      - ..:/app
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
      qdrant:
        condition: service_started
    networks:
      - internal
    restart: unless-stopped

  postgres:
    image: postgres:16-alpine
    container_name: telegram-bot-postgres
    environment:
      POSTGRES_USER: botuser
      POSTGRES_PASSWORD: botpass
      POSTGRES_DB: telegram_bot
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U botuser -d telegram_bot"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - internal
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: telegram-bot-redis
    command: redis-server --requirepass redispass --appendonly yes
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - internal
    restart: unless-stopped

  qdrant:
    image: qdrant/qdrant:latest
    container_name: telegram-bot-qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - internal
    restart: unless-stopped

  vllm:
    image: vllm/vllm-openai:latest
    container_name: telegram-bot-vllm
    ports:
      - "8001:8001"
    volumes:
      - vllm_models:/root/.cache/huggingface
    environment:
      HUGGING_FACE_HUB_TOKEN: ""  # Opcional para modelos gated
    command:
      - "--model"
      - "Qwen/Qwen2.5-7B-Instruct"
      - "--port"
      - "8001"
      - "--max-model-len"
      - "8192"
      - "--gpu-memory-utilization"
      - "0.90"
      - "--trust-remote-code"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    networks:
      - internal
    restart: unless-stopped
    # Comentar la sección 'deploy' si no tienes GPU

  nginx:
    image: nginx:alpine
    container_name: telegram-bot-nginx
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    networks:
      - internal
    restart: unless-stopped
    profiles:
      - production

volumes:
  postgres_data:
  redis_data:
  qdrant_data:
  vllm_models:

networks:
  internal:
    driver: bridge
```

---

## 2.8 NGINX (Producción)

### Paso 13: Crear configuración de Nginx

Crea `docker/nginx/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    # Limitar tamaño de body (Telegram max ~50MB para documentos)
    client_max_body_size 50M;

    # HTTP → HTTPS redirect
    server {
        listen 80;
        server_name tudominio.com;
        return 301 https://$host$request_uri;
    }

    # HTTPS
    server {
        listen 443 ssl http2;
        server_name tudominio.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Rate limiting
        limit_req_zone $binary_remote_addr zone=webhook:10m rate=10r/s;
        limit_req zone=webhook burst=20 nodelay;

        # Health check (sin rate limit)
        location /health {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /ready {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Webhook endpoint (con rate limit)
        location /webhook {
            limit_req zone=webhook burst=20 nodelay;
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # Timeout más largo para respuestas de IA
            proxy_read_timeout 120s;
            proxy_send_timeout 60s;
        }

        # Métricas (solo acceso interno)
        location /metrics {
            allow 127.0.0.1;
            deny all;
            proxy_pass http://api;
        }
    }
}
```

### Paso 14: Preparar SSL (producción)

```bash
# Crear directorio para SSL
mkdir -p docker/nginx/ssl

# Si tienes dominio con Let's Encrypt:
# sudo apt install certbot
# sudo certbot certonly --standalone -d tudominio.com
# Copiar certificados:
# Copy-Item C:\Certbot\...\fullchain.pem docker/nginx/ssl/
# Copy-Item C:\Certbot\...\privkey.pem docker/nginx/ssl/

# Para desarrollo local (sin HTTPS real), puedes:
# 1. Usar ngrok para exponer tu localhost
# 2. O configurar webhook sin Nginx (solo api directo)
```

---

## 2.9 SCRIPTS DE DESARROLLO

### Paso 15: Crear Makefile (comandos útiles)

Crea `Makefile` en la raíz:

```makefile
.PHONY: help install dev lint typecheck test clean docker-up docker-down

help:  ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Instala dependencias
	uv sync

dev:  ## Inicia servidor en modo desarrollo
	uv run uvicorn src.main:app --reload --port 8000

lint:  ## Ejecuta linter (ruff)
	uv run ruff check src/

lint-fix:  ## Corrige errores automáticamente
	uv run ruff check --fix src/

typecheck:  ## Verifica tipos (mypy)
	uv run mypy src/

test:  ## Ejecuta tests
	uv run pytest tests/ -v

test-cov:  ## Ejecuta tests con cobertura
	uv run pytest tests/ --cov=src --cov-report=term-missing

clean:  ## Limpia archivos temporales
	rm -rf __pycache__ .pytest_cache .ruff_cache
	rm -rf src/**/__pycache__

docker-up:  ## Levanta servicios Docker (sin GPU)
	docker compose -f docker/docker-compose.yml up -d

docker-up-gpu:  ## Levanta servicios Docker (con GPU)
	docker compose -f docker/docker-compose.yml up -d vllm api postgres redis qdrant

docker-down:  ## Detiene servicios Docker
	docker compose -f docker/docker-compose.yml down

docker-logs:  ## Muestra logs de Docker
	docker compose -f docker/docker-compose.yml logs -f

db-migrate:  ## Crea nueva migración
	uv run alembic revision --autogenerate -m "$(message)"

db-upgrade:  ## Aplica migraciones
	uv run alembic upgrade head

db-downgrade:  ## Revierte última migración
	uv run alembic downgrade -1
```

---

## 2.10 ALEMBIC (MIGRACIONES)

### Paso 16: Inicializar Alembic

```bash
# Desde la raíz del proyecto
cd src/db
alembic init migrations
cd ../..
```

### Paso 17: Configurar alembic.ini

Edita `src/db/alembic.ini` y cambia la línea de sqlalchemy.url:

```ini
# Antes:
# sqlalchemy.url = driver://user:pass@localhost/dbname

# Después:
sqlalchemy.url = postgresql+asyncpg://botuser:botpass@localhost:5432/telegram_bot
```

> **Nota:** Para desarrollo local sin Docker, instala PostgreSQL local o usa este connection string. Para Docker, el valor real viene del .env y se sobreescribe en `env.py`.

### Paso 18: Configurar env.py de Alembic

Edita `src/db/migrations/env.py`:

```python
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import settings
from src.db.models import Base  # <- se creará en Fase 3

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = settings.database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = create_async_engine(settings.database_url)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

---

## 2.11 ENTRY POINT

### Paso 19: Crear main.py

Crea `src/main.py` — es el punto de entrada de la aplicación:

```python
import structlog

from src.api.app import create_app
from src.core.config import settings

logger = structlog.get_logger()


def main():
    app = create_app()
    logger.info(
        "Starting application",
        environment=settings.environment,
        log_level=settings.log_level,
    )
    return app


app = main()
```

### Paso 20: Crear app FastAPI

Crea `src/api/app.py`:

```python
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from src.api.health import router as health_router
from src.api.webhook import router as webhook_router
from src.core.config import settings

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja startup y shutdown de la aplicación."""
    logger.info("Application startup")
    # Aquí se inicializarán: DB pool, Redis, Qdrant, Aiogram, etc.
    yield
    # Aquí se cerrarán conexiones
    logger.info("Application shutdown")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Telegram AI Bot",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
    )

    # Rutas
    app.include_router(health_router)
    app.include_router(webhook_router)

    return app
```

### Paso 21: Crear health endpoint

Crea `src/api/health.py`:

```python
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return {"status": "ok", "service": "telegram-ai-bot"}


@router.get("/ready")
async def ready():
    # En el futuro: verificar DB, Redis, Qdrant
    return {"status": "ready"}
```

### Paso 22: Crear webhook endpoint (placeholder)

Crea `src/api/webhook.py`:

```python
import hmac

import structlog
from fastapi import APIRouter, Request

from src.core.config import settings

logger = structlog.get_logger()
router = APIRouter(tags=["webhook"])


def verify_webhook(secret: str, payload: bytes, signature: str) -> bool:
    """Verifica que el webhook venga de Telegram."""
    expected = hmac.new(
        secret.encode(), payload, "sha256"
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


@router.post("/webhook")
async def webhook(request: Request):
    """Recibe updates de Telegram."""
    # Verificar firma (producción)
    # signature = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    # body = await request.body()
    # if not verify_webhook(settings.telegram_webhook_secret, body, signature):
    #     return {"ok": False, "error": "invalid signature"}

    update_data = await request.json()
    logger.info("Webhook received", update_id=update_data.get("update_id"))

    # TODO: Pasar a Aiogram Dispatcher (Fase 4)

    return {"ok": True}
```

---

## 2.12 VERIFICACIÓN

### Paso 23: Probar que todo funciona

```bash
# 1. Verificar que el código arranca
uv run python -c "from src.core.config import settings; print(settings.model_dump())"

# 2. Iniciar servidor de desarrollo
uv run uvicorn src.main:app --reload --port 8000

# 3. Probar health endpoint (en otra terminal)
curl http://localhost:8000/health
# Debería responder: {"status":"ok","service":"telegram-ai-bot"}

# 4. Probar ready endpoint
curl http://localhost:8000/ready
# Debería responder: {"status":"ready"}

# 5. Probar webhook (simulado)
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"update_id": 1, "message": {"text": "hola"}}'
# Debería responder: {"ok": true}

# 6. Lint
uv run ruff check src/

# 7. Type check
uv run mypy src/

# 8. Tests (aunque aún no hay)
uv run pytest tests/ -v
```

### Paso 24: Levantar Docker (cuando todo lo anterior funcione)

```bash
# Desarrollo (sin GPU, sin Nginx)
docker compose -f docker/docker-compose.yml up -d postgres redis qdrant api

# Producción (con GPU, con Nginx)
docker compose -f docker/docker-compose.yml --profile production up -d

# Ver logs
docker compose -f docker/docker-compose.yml logs -f api

# Verificar contenedores
docker compose -f docker/docker-compose.yml ps
```

---

## 2.13 ESTRUCTURA FINAL DEL PROYECTO

Después de ejecutar todos los pasos, tu proyecto debe verse así:

```
telegram-ai-bot/
│
├── .env                        # ← Creado en Paso 9
├── .env.example                # ← Creado en Paso 9
├── .gitignore                  # ← Creado en Paso 2
├── .venv/                      # ← Creado en Paso 3
├── Makefile                    # ← Creado en Paso 15
├── pyproject.toml              # ← Creado en Paso 5
│
├── src/
│   ├── main.py                 # ← Creado en Paso 19
│   │
│   ├── api/
│   │   ├── __init__.py         # ← Creado en Paso 8
│   │   ├── app.py              # ← Creado en Paso 20
│   │   ├── health.py           # ← Creado en Paso 21
│   │   └── webhook.py          # ← Creado en Paso 22
│   │
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── middlewares/__init__.py
│   │   ├── filters/__init__.py
│   │   └── handlers/__init__.py
│   │
│   ├── services/__init__.py
│   ├── models/__init__.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py          # (se creará en Fase 3)
│   │   ├── models/__init__.py
│   │   └── migrations/         # ← Creado en Paso 16
│   │       ├── alembic.ini     # ← Creado en Paso 17
│   │       ├── env.py          # ← Creado en Paso 18
│   │       └── versions/
│   │
│   ├── vector/__init__.py
│   ├── cache/__init__.py
│   └── core/
│       ├── __init__.py
│       └── config.py           # ← Creado en Paso 10
│
├── docker/
│   ├── Dockerfile              # ← Creado en Paso 11
│   ├── docker-compose.yml      # ← Creado en Paso 12
│   └── nginx/
│       └── nginx.conf          # ← Creado en Paso 13
│
└── tests/
    ├── __init__.py
    ├── unit/__init__.py
    └── integration/__init__.py
```

---

## 2.14 COMMIT INICIAL

Cuando todo funcione, haz el primer commit:

```bash
git add .
git commit -m "chore: initial project setup

- Python 3.13+ with FastAPI + Aiogram
- PostgreSQL + Redis + Qdrant + vLLM
- Docker Compose for all services
- Nginx with SSL termination
- Makefile for common tasks
- Pydantic Settings for configuration
- Ruff + MyPy for code quality
- Alembic for DB migrations"
```


FASE 3 - DISEÑO DE BASE DE DATOS
===============================

## Instrucciones de uso

Esta fase contiene **todo el código** para implementar la capa de base de datos: modelos SQLAlchemy, sesión, esquemas Pydantic, y migraciones.

**Orden de ejecución:**
1. `3.1` → Actualizar `src/db/models/__init__.py` con Base y mixins
2. `3.2` → Crear cada modelo en `src/db/models/`
3. `3.3` → Crear `src/db/session.py`
4. `3.4` → Crear esquemas Pydantic en `src/models/`
5. `3.5` → Generar migración inicial con Alembic
6. `3.6` → Verificar que todo funciona

---

## 3.1 MODELO BASE Y MIXINS

### Actualizar `src/db/models/__init__.py`

Reemplaza el contenido actual con:

```python
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )


class UpdateableMixin(TimestampMixin):
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True,
    )


class UUIDMixin:
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: uuid4().hex,
    )
```

---

## 3.2 MODELOS SQLALCHEMY

### Crear `src/db/models/user.py`

```python
from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import UUIDMixin, UpdateableMixin, Base


class User(UUIDMixin, UpdateableMixin, Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False
    )
    username: Mapped[str | None] = mapped_column(String(128), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="es", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    messages = relationship("Message", back_populates="user", lazy="selectin")
    memories = relationship("Memory", back_populates="user", lazy="selectin")
    documents = relationship("Document", back_populates="user", lazy="selectin")
```

### Crear `src/db/models/chat.py`

```python
from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import TimestampMixin, UUIDMixin, Base


class Chat(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "chats"

    telegram_chat_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False
    )
    chat_type: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str | None] = mapped_column(String(512), nullable=True)
    personality_id: Mapped[str | None] = mapped_column(
        UUIDMixin.id.type, ForeignKey("personalities.id"), nullable=True
    )

    messages = relationship("Message", back_populates="chat", lazy="selectin")
    conversations = relationship("Conversation", back_populates="chat", lazy="selectin")
    personality = relationship("Personality", back_populates="chats", lazy="selectin")
    documents = relationship("Document", back_populates="chat", lazy="selectin")
```

### Crear `src/db/models/message.py`

```python
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import TimestampMixin, UUIDMixin, Base


class Message(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "messages"

    chat_id: Mapped[str] = mapped_column(
        UUIDMixin.id.type, ForeignKey("chats.id"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        UUIDMixin.id.type, ForeignKey("users.id"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)

    chat = relationship("Chat", back_populates="messages", lazy="selectin")
    user = relationship("User", back_populates="messages", lazy="selectin")
```

### Crear `src/db/models/conversation.py`

```python
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import TimestampMixin, UUIDMixin, Base


class Conversation(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "conversations"

    chat_id: Mapped[str] = mapped_column(
        UUIDMixin.id.type, ForeignKey("chats.id"), nullable=False, index=True
    )
    title: Mapped[str | None] = mapped_column(String(512), nullable=True)

    chat = relationship("Chat", back_populates="conversations", lazy="selectin")
```

### Crear `src/db/models/personality.py`

```python
from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import UpdateableMixin, UUIDMixin, Base


class Personality(UUIDMixin, UpdateableMixin, Base):
    __tablename__ = "personalities"

    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, default=0.7, nullable=False)
    max_tokens: Mapped[int] = mapped_column(Integer, default=2048, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    chats = relationship("Chat", back_populates="personality", lazy="selectin")
```

### Crear `src/db/models/memory.py`

```python
from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import TimestampMixin, UUIDMixin, Base


class Memory(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "memories"

    user_id: Mapped[str] = mapped_column(
        UUIDMixin.id.type, ForeignKey("users.id"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding_id: Mapped[str | None] = mapped_column(
        String(128), nullable=True, unique=True
    )
    importance: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)

    user = relationship("User", back_populates="memories", lazy="selectin")
```

### Crear `src/db/models/document.py`

```python
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import TimestampMixin, UUIDMixin, Base


class Document(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "documents"

    chat_id: Mapped[str | None] = mapped_column(
        UUIDMixin.id.type, ForeignKey("chats.id"), nullable=True
    )
    user_id: Mapped[str] = mapped_column(
        UUIDMixin.id.type, ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    file_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    status: Mapped[str] = mapped_column(
        String(32), default="pending", nullable=False
    )

    chat = relationship("Chat", back_populates="documents", lazy="selectin")
    user = relationship("User", back_populates="documents", lazy="selectin")
```

---

## 3.3 SESIÓN DE BASE DE DATOS

### Crear `src/db/session.py`

```python
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.is_development,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def init_db() -> None:
    """Crea todas las tablas (útil para desarrollo, no para producción)."""
    from src.db.models import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await engine.dispose()
```

---

## 3.4 ESQUEMAS PYDANTIC

### Actualizar `src/models/__init__.py`

```python
"""
Schemas Pydantic para la API y servicios.

Cada modelo tiene:
- CreateSchema: para crear (sin id, sin timestamps)
- UpdateSchema: para actualizar (todos opcionales)
- ResponseSchema: para devolver al cliente
"""

from src.models.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from src.models.chat import ChatCreate, ChatResponse, ChatUpdate
from src.models.message import (
    MessageCreate,
    MessageResponse,
)
from src.models.personality import (
    PersonalityCreate,
    PersonalityResponse,
    PersonalityUpdate,
)
from src.models.document import DocumentCreate, DocumentResponse
from src.models.memory import MemoryCreate, MemoryResponse

__all__ = [
    "UserCreate", "UserResponse", "UserUpdate",
    "ChatCreate", "ChatResponse", "ChatUpdate",
    "MessageCreate", "MessageResponse",
    "PersonalityCreate", "PersonalityResponse", "PersonalityUpdate",
    "DocumentCreate", "DocumentResponse",
    "MemoryCreate", "MemoryResponse",
]
```

### Crear `src/models/user.py`

```python
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    telegram_id: int
    username: str | None = None
    first_name: str | None = None
    language: str = "es"
    is_active: bool = True


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: str | None = None
    first_name: str | None = None
    language: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime | None = None
```

### Crear `src/models/chat.py`

```python
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChatBase(BaseModel):
    telegram_chat_id: int
    chat_type: str
    title: str | None = None
    personality_id: str | None = None


class ChatCreate(ChatBase):
    pass


class ChatUpdate(BaseModel):
    title: str | None = None
    personality_id: str | None = None


class ChatResponse(ChatBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
```

### Crear `src/models/message.py`

```python
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    chat_id: str
    user_id: str
    role: str
    content: str
    tokens: int | None = None


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
```

### Crear `src/models/personality.py`

```python
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PersonalityBase(BaseModel):
    name: str
    system_prompt: str
    temperature: float = 0.7
    max_tokens: int = 2048
    is_active: bool = True


class PersonalityCreate(PersonalityBase):
    pass


class PersonalityUpdate(BaseModel):
    name: str | None = None
    system_prompt: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    is_active: bool | None = None


class PersonalityResponse(PersonalityBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime | None = None
```

### Crear `src/models/memory.py`

```python
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MemoryBase(BaseModel):
    user_id: str
    content: str
    embedding_id: str | None = None
    importance: float = 0.5


class MemoryCreate(MemoryBase):
    pass


class MemoryResponse(MemoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
```

### Crear `src/models/document.py`

```python
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    chat_id: str | None = None
    user_id: str
    name: str
    status: str = "pending"


class DocumentCreate(DocumentBase):
    file_path: str | None = None


class DocumentResponse(DocumentBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    file_path: str | None = None
    created_at: datetime
```

---

## 3.5 MIGRACIÓN ALEMBIC

### Paso 1: Registrar los modelos en `src/db/models/__init__.py`

Agrega estas líneas **al final** del archivo `src/db/models/__init__.py` (después de la clase Base y mixins):

```python
# Registrar modelos para que Alembic los detecte automáticamente
from src.db.models.user import User
from src.db.models.chat import Chat
from src.db.models.message import Message
from src.db.models.conversation import Conversation
from src.db.models.personality import Personality
from src.db.models.memory import Memory
from src.db.models.document import Document

__all__ = [
    "Base",
    "TimestampMixin",
    "UpdateableMixin",
    "UUIDMixin",
    "User",
    "Chat",
    "Message",
    "Conversation",
    "Personality",
    "Memory",
    "Document",
]
```

### Paso 2: Verificar que alembic.ini apunte al lugar correcto

El archivo `src/db/migrations/alembic.ini` ya debe tener:

```ini
sqlalchemy.url = postgresql+asyncpg://botuser:botpass@localhost:5432/telegram_bot
```

### Paso 3: Verificar que `env.py` importe Base correctamente

El archivo `src/db/migrations/env.py` ya debe tener:

```python
from src.db.models import Base
```

### Paso 4: Si la migración es la primera vez, ajustar el `script_location`

Abre `src/db/migrations/alembic.ini` y asegúrate de que apunte al directorio correcto:

```ini
script_location = src/db/migrations
```

Y que `prepend_sys_path` incluya la raíz del proyecto:

```ini
prepend_sys_path = ../..
```

(Esto es necesario porque el `.ini` está en `src/db/migrations/` y el proyecto en la raíz)

### Paso 5: Generar la migración inicial

```bash
# Desde la raíz del proyecto
uv run alembic -c src/db/migrations/alembic.ini revision --autogenerate -m "initial_tables"
```

Esto debe generar un archivo en `src/db/migrations/versions/` con la migración.

### Paso 6: Revisar la migración generada

Abre el archivo generado en `src/db/migrations/versions/` y verifica que contenga:

- `op.create_table("users", ...)` con todas las columnas
- `op.create_table("chats", ...)` con FK a `personalities`
- `op.create_table("messages", ...)` con FK a `chats` y `users`
- `op.create_table("conversations", ...)` con FK a `chats`
- `op.create_table("personalities", ...)`
- `op.create_table("memories", ...)` con FK a `users`
- `op.create_table("documents", ...)` con FK a `chats` y `users`

Si falta alguna FK o columna, corrígelo manualmente.

### Paso 7: Aplicar la migración

```bash
uv run alembic -c src/db/migrations/alembic.ini upgrade head
```

---

## 3.6 MODELOS DE NEGOCIO (Opcional, para servicios)

### Crear `src/services/__init__.py`

```python
# Servicios de negocio (se implementarán en fases posteriores)
```

No es necesario modificar este archivo ahora.

---

## 3.7 DIAGRAMA ENTIDAD-RELACIÓN

```
┌───────────────────┐     ┌─────────────────────┐
│      users        │     │    personalities     │
├───────────────────┤     ├─────────────────────┤
│ id (PK)           │     │ id (PK)              │
│ telegram_id (UQ)  │     │ name (UQ)            │
│ username          │     │ system_prompt        │
│ first_name        │     │ temperature          │
│ language          │     │ max_tokens           │
│ is_active         │     │ is_active            │
│ created_at        │     │ created_at           │
│ updated_at        │     │ updated_at           │
└────────┬──────────┘     └──────────┬──────────┘
         │                           │
         │ 1:N                       │ 1:N
         ▼                           ▼
┌───────────────────┐     ┌─────────────────────┐
│     messages      │     │       chats          │
├───────────────────┤     ├─────────────────────┤
│ id (PK)           │     │ id (PK)              │
│ chat_id (FK) ─────┼──▶  │ telegram_chat_id(UQ) │
│ user_id (FK) ─────┼──▶  │ chat_type            │
│ role              │     │ title                │
│ content           │     │ personality_id (FK)──┼──▶
│ tokens            │     │ created_at           │
│ created_at        │     └────────┬──────────┘   │
└───────────────────┘              │              │
                                   │ 1:N          │
                                   ▼              │
┌───────────────────┐              │              │
│  conversations    │              │              │
├───────────────────┤              │              │
│ id (PK)           │              │              │
│ chat_id (FK) ─────┼──────────────┘              │
│ title             │                             │
│ created_at        │                             │
└───────────────────┘                             │
                                                  │
┌───────────────────┐     ┌──────────────────────┐│
│     memories      │     │      documents       ││
├───────────────────┤     ├──────────────────────┤│
│ id (PK)           │     │ id (PK)              ││
│ user_id (FK) ─────┼──▶  │ chat_id (FK) ────────┼┘
│ content           │     │ user_id (FK) ────────┼──▶
│ embedding_id (UQ) │     │ name                 │
│ importance        │     │ file_path            │
│ created_at        │     │ status               │
└───────────────────┘     │ created_at           │
                          └──────────────────────┘
```

---

## 3.8 VERIFICACIÓN

### Probar que los modelos se importan correctamente

```bash
uv run python -c "
from src.db.models import Base, User, Chat, Message, Conversation, Personality, Memory, Document
print('✓ Modelos importados correctamente')
print(f'Tablas: {Base.metadata.tables.keys()}')
"
```

### Probar esquemas Pydantic

```bash
uv run python -c "
from src.models import UserCreate, UserResponse
from datetime import datetime

# Crear
data = UserCreate(telegram_id=123456789, username='test')
print(f'✓ UserCreate: {data.model_dump()}')

# Response (from_attributes)
resp = UserResponse(
    id='abc123',
    telegram_id=123456789,
    username='test',
    language='es',
    is_active=True,
    created_at=datetime.now(),
    updated_at=None,
)
print(f'✓ UserResponse: {resp.model_dump()}')
"
```

### Verificar que Alembic detecta los modelos

```bash
uv run alembic -c src/db/migrations/alembic.ini revision --autogenerate -m "test_detect" --sql
```

Si todo está correcto, verás las sentencias SQL de creación de tablas. Luego borra el archivo de migración de prueba:

```bash
# Eliminar el archivo de migración de prueba creado
Remove-Item src/db/migrations/versions/*test_detect*
```

---

## 3.9 SEED DATA (Opcional)

### Crear `scripts/seed.py`

```python
"""Script para poblar la base de datos con datos iniciales."""

import asyncio

from src.core.config import settings
from src.db.models import Personality
from src.db.session import async_session_factory, init_db


async def seed() -> None:
    await init_db()

    async with async_session_factory() as session:
        # Personalidad por defecto
        default = Personality(
            name="default",
            system_prompt=(
                "Eres un asistente técnico experto en programación. "
                "Respondes de forma clara, directa y profesional. "
                "Usas el idioma del usuario."
            ),
            temperature=0.7,
            max_tokens=2048,
            is_active=True,
        )
        session.add(default)

        await session.commit()
        print("✓ Seed completado: personalidad 'default' creada")


if __name__ == "__main__":
    asyncio.run(seed())
```

Para ejecutarlo:

```bash
mkdir -p scripts
# (crea el archivo scripts/seed.py con el contenido de arriba)
uv run python scripts/seed.py
```


FASE 4 - BOT TELEGRAM
========================

## Instrucciones de uso

Esta fase conecta Telegram con nuestra infraestructura usando Aiogram 3.x, middlewares, filtros y handlers.

**Orden de ejecución:**
1. `4.1` → Crear bot en BotFather y configurar webhook
2. `4.2` → Crear el dispatcher de Aiogram
3. `4.3` → Implementar los 4 middlewares
4. `4.4` → Implementar filtros (mención, comando)
5. `4.5` → Implementar handlers (mensajes, comandos)
6. `4.6` → Actualizar `src/api/webhook.py` para integrar Aiogram
7. `4.7` → Actualizar `src/api/app.py` con lifespan del bot
8. `4.8` → Crear cliente Redis (caché + rate limiting)
9. `4.9` → Exponer webhook con ngrok (desarrollo)
10. `4.10` → Verificar que todo funciona

---

## 4.1 CONFIGURAR BOT EN TELEGRAM

### Paso 1: Crear bot con BotFather

1. Abre Telegram y busca `@BotFather`
2. Ejecuta: `/newbot`
3. Nombre: `CustomPerezBot` (o el que quieras)
4. Username: `TuBot_bot` (debe terminar en `bot`)
5. BotFather te dará un **token**. Guárdalo.

### Paso 2: Actualizar .env con el token

```bash
# Edita .env y pega tu token:
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklmNOPqrstUVwxyz
TELEGRAM_WEBHOOK_SECRET=un_secreto_muy_largo_de_64_caracteres_minimo
```

El `TELEGRAM_WEBHOOK_SECRET` es un string que solo tú y Telegram conocen. Genera uno:

```bash
# PowerShell
$random = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | % {[char]$_})
Write-Output $random
```

### Paso 3: Configurar webhook (después de tener ngrok o dominio)

Se hace al final, cuando el servidor esté corriendo (paso 4.9).

---

## 4.2 DISPATCHER DE AIOGRAM

### Crear `src/bot/dispatcher.py`

```python
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.bot.filters.command import CommandFilter
from src.bot.filters.mention import MentionFilter
from src.bot.handlers.commands import router as commands_router
from src.bot.handlers.messages import router as messages_router
from src.bot.middlewares.auth import AuthMiddleware
from src.bot.middlewares.context import ContextMiddleware
from src.bot.middlewares.logging import LoggingMiddleware
from src.bot.middlewares.rate_limit import RateLimitMiddleware
from src.cache.rate_limiter import RateLimiter
from src.core.config import settings

bot = Bot(
    token=settings.telegram_bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()


def setup_dispatcher() -> None:
    # Middlewares (orden: primero en entrar, último en ejecutarse)
    dp.update.middleware(LoggingMiddleware())
    dp.update.middleware(AuthMiddleware())
    dp.update.middleware(RateLimitMiddleware(RateLimiter()))
    dp.update.middleware(ContextMiddleware())

    # Filtros
    dp.message.register(commands_router.message, CommandFilter())
    dp.message.register(messages_router.message, MentionFilter())
    dp.message.register(messages_router.message)

    # Incluir routers
    dp.include_router(commands_router)
    dp.include_router(messages_router)
```

---

## 4.3 MIDDLEWARES

### Crear `src/bot/middlewares/auth.py`

```python
from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TelegramUser

from src.db.models.user import User
from src.db.session import async_session_factory


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, object]], Awaitable[object]],
        event: TelegramObject,
        data: dict[str, object],
    ) -> object:
        telegram_user: TelegramUser | None = data.get("event_from_user")
        if telegram_user and not telegram_user.is_bot:
            async with async_session_factory() as session:
                from sqlalchemy import select

                result = await session.execute(
                    select(User).where(User.telegram_id == telegram_user.id)
                )
                user = result.scalar_one_or_none()
                if user is None:
                    user = User(
                        telegram_id=telegram_user.id,
                        username=telegram_user.username,
                        first_name=telegram_user.first_name,
                        language=telegram_user.language_code or "es",
                    )
                    session.add(user)
                    await session.commit()
                    await session.refresh(user)
                data["user"] = user
        return await handler(event, data)
```

### Crear `src/bot/middlewares/logging.py`

```python
from collections.abc import Awaitable, Callable

import structlog
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = structlog.get_logger()


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, object]], Awaitable[object]],
        event: TelegramObject,
        data: dict[str, object],
    ) -> object:
        update = data.get("event_update")
        user = data.get("event_from_user")
        if update:
            logger.info(
                "Update received",
                update_id=update.update_id,
                user_id=user.id if user else None,
                username=user.username if user else None,
            )
        return await handler(event, data)
```

### Crear `src/bot/middlewares/rate_limit.py`

```python
from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.cache.rate_limiter import RateLimiter


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, rate_limiter: RateLimiter) -> None:
        self.rate_limiter = rate_limiter

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, object]], Awaitable[object]],
        event: TelegramObject,
        data: dict[str, object],
    ) -> object:
        user = data.get("event_from_user")
        if user:
            allowed = await self.rate_limiter.check(str(user.id))
            if not allowed:
                from aiogram.types import Message

                if isinstance(event, Message):
                    await event.answer("⏳ Demasiadas solicitudes. Espera un momento.")
                return None
        return await handler(event, data)
```

### Crear `src/bot/middlewares/context.py`

```python
from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Chat as TelegramChat

from src.db.models.chat import Chat
from src.db.session import async_session_factory


class ContextMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, object]], Awaitable[object]],
        event: TelegramObject,
        data: dict[str, object],
    ) -> object:
        telegram_chat: TelegramChat | None = data.get("event_chat")
        if telegram_chat:
            async with async_session_factory() as session:
                from sqlalchemy import select

                result = await session.execute(
                    select(Chat).where(Chat.telegram_chat_id == telegram_chat.id)
                )
                chat = result.scalar_one_or_none()
                if chat is None:
                    chat = Chat(
                        telegram_chat_id=telegram_chat.id,
                        chat_type=telegram_chat.type,
                        title=telegram_chat.title,
                    )
                    session.add(chat)
                    await session.commit()
                    await session.refresh(chat)
                data["chat"] = chat
        return await handler(event, data)
```

---

## 4.4 FILTROS

### Crear `src/bot/filters/__init__.py`

```python
from src.bot.filters.command import CommandFilter
from src.bot.filters.mention import MentionFilter

__all__ = ["CommandFilter", "MentionFilter"]
```

### Crear `src/bot/filters/mention.py`

```python
from aiogram.filters import BaseFilter
from aiogram.types import Message


class MentionFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        bot = message.bot
        if bot is None:
            return False
        bot_username = (await bot.me()).username
        if bot_username is None:
            return False
        # Detecta @botusername al inicio, medio, o reply al bot
        if f"@{bot_username}" in message.text:
            return True
        if message.reply_to_message and message.reply_to_message.from_user:
            return message.reply_to_message.from_user.id == bot.id
        return False
```

### Crear `src/bot/filters/command.py`

```python
from aiogram.filters import BaseFilter
from aiogram.types import Message


COMMANDS = {"/start", "/help", "/resumen", "/buscar", "/aprende", "/modo", "/personalidad"}


class CommandFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        command = message.text.split()[0].lower()
        return command in COMMANDS
```

---

## 4.5 HANDLERS

### Crear `src/bot/handlers/__init__.py`

```python
```

### Crear `src/bot/handlers/commands.py`

```python
from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def start(message: Message) -> None:
    if message.text and message.text.startswith("/start"):
        await message.answer(
            "¡Hola! Soy tu asistente con IA.\n\n"
            "Puedes hablarme directamente o usar comandos:\n"
            "/resumen - Resumir conversación\n"
            "/buscar - Buscar en internet\n"
            "/aprende - Aprender un documento\n"
            "/modo - Cambiar personalidad"
        )


@router.message()
async def help_command(message: Message) -> None:
    if message.text and message.text.startswith("/help"):
        await message.answer(
            "Comandos disponibles:\n\n"
            "/start - Iniciar bot\n"
            "/help - Mostrar ayuda\n"
            "/resumen - Resumir últimos mensajes\n"
            "/buscar <consulta> - Buscar en internet\n"
            "/aprende - Subir documento para aprender\n"
            "/modo <nombre> - Cambiar personalidad"
        )


@router.message()
async def unknown_command(message: Message) -> None:
    if message.text and message.text.startswith("/"):
        await message.answer("❌ Comando no reconocido. Usa /help para ver los disponibles.")
```

### Crear `src/bot/handlers/messages.py`

```python
from aiogram import Router
from aiogram.types import Message
from aiogram.types import User as TelegramUser

from src.db.models.chat import Chat
from src.db.models.user import User

router = Router()


@router.message()
async def handle_message(
    message: Message,
    user: User | None = None,
    chat: Chat | None = None,
) -> None:
    if not message.text:
        return

    telegram_user: TelegramUser | None = message.from_user
    user_display = telegram_user.first_name if telegram_user else "Usuario"

    # Por ahora, respuesta espejo (se conectará al LLM en Fase 5)
    response = (
        f"👋 Hola {user_display}! Tu mensaje fue recibido.\n\n"
        f"Has dicho: _{message.text}_\n\n"
        "⚠️ El motor de IA aún no está conectado."
    )

    await message.answer(response)
```

---

## 4.6 WEBHOOK (Integración Aiogram + FastAPI)

### Actualizar `src/api/webhook.py`

```python
import structlog
from aiogram.types import Update
from fastapi import APIRouter, Request

from src.bot.dispatcher import bot, dp
from src.core.config import settings

logger = structlog.get_logger()
router = APIRouter(tags=["webhook"])


async def set_webhook() -> None:
    if settings.telegram_webhook_url:
        await bot.set_webhook(
            url=f"{settings.telegram_webhook_url}/webhook",
            secret_token=settings.telegram_webhook_secret,
            drop_pending_updates=True,
        )
        logger.info("Webhook set", url=settings.telegram_webhook_url)


async def delete_webhook() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook deleted")


@router.post("/webhook")
async def webhook(request: Request) -> dict[str, bool | str]:
    token = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")

    if token != settings.telegram_webhook_secret:
        logger.warning("Invalid webhook secret token")
        return {"ok": False, "error": "invalid secret token"}

    body = await request.json()
    update = Update.model_validate(body)
    await dp.feed_update(bot=bot, update=update)
    return {"ok": True}
```

---

## 4.7 LIFESPAN (Integración bot + FastAPI)

### Actualizar `src/api/app.py`

```python
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from src.api.health import router as health_router
from src.api.webhook import delete_webhook, router as webhook_router, set_webhook
from src.bot.dispatcher import bot, setup_dispatcher
from src.core.config import settings

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    logger.info("Starting bot")
    setup_dispatcher()
    if settings.is_production:
        await set_webhook()
    yield
    if settings.is_production:
        await delete_webhook()
    await bot.session.close()
    logger.info("Bot stopped")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Telegram AI Bot",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
    )

    app.include_router(health_router)
    app.include_router(webhook_router)

    return app
```

---

## 4.8 CACHE / RATE LIMITER (Redis)

### Crear `src/cache/client.py`

```python
from redis.asyncio import Redis

from src.core.config import settings

redis_client: Redis | None = None


async def get_redis() -> Redis:
    global redis_client
    if redis_client is None:
        redis_client = Redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )
    return redis_client


async def close_redis() -> None:
    global redis_client
    if redis_client:
        await redis_client.aclose()
        redis_client = None
```

### Crear `src/cache/rate_limiter.py`

```python
import time

from src.cache.client import get_redis
from src.core.config import settings


class RateLimiter:
    def __init__(self, max_requests: int = 1, window: int = 1) -> None:
        self.max_requests = max_requests
        self.window = window

    async def check(self, user_id: str) -> bool:
        client = await get_redis()
        key = f"ratelimit:{user_id}"
        now = time.time()
        window_start = now - self.window

        await client.zremrangebyscore(key, 0, window_start)
        request_count = await client.zcard(key)

        if request_count >= self.max_requests:
            return False

        await client.zadd(key, {str(now): now})
        await client.expire(key, self.window)
        return True
```

---

## 4.9 NGROK (Desarrollo local)

### Paso 1: Instalar ngrok

```bash
# Opción 1: Usar el que viene en dev-dependencies
uv run ngrok --version

# Opción 2: Descargar de https://ngrok.com/download
# O con winget:
winget install ngrok
```

### Paso 2: Exponer el servidor local

```bash
# Terminal 1: Iniciar FastAPI
uv run uvicorn src.main:app --reload --port 8000

# Terminal 2: Exponer con ngrok
ngrok http 8000
```

### Paso 3: Configurar webhook

ngrok te dará una URL como `https://abc123.ngrok-free.app`. Con esa URL, actualiza `.env`:

```bash
TELEGRAM_WEBHOOK_URL=https://abc123.ngrok-free.app
```

### Paso 4: Registrar webhook en Telegram

```bash
# PowerShell (desde raíz del proyecto)
uv run python -c "
import asyncio
from src.bot.dispatcher import bot
from src.core.config import settings

async def main():
    url = f'{settings.telegram_webhook_url}/webhook'
    await bot.set_webhook(
        url=url,
        secret_token=settings.telegram_webhook_secret,
        drop_pending_updates=True,
    )
    info = await bot.get_webhook_info()
    print(f'Webhook URL: {info.url}')
    print(f'Pending updates: {info.pending_update_count}')

asyncio.run(main())
"
```

### Paso 5: Verificar webhook

```bash
uv run python -c "
import asyncio
from src.bot.dispatcher import bot

async def main():
    info = await bot.get_webhook_info()
    print(f'URL: {info.url}')
    print(f'Has custom secret: {info.secret_token is not None}')
    print(f'Pending: {info.pending_update_count}')

asyncio.run(main())
"
```

---

## 4.10 VERIFICACIÓN

### Prueba 1: importar todo sin errores

```bash
uv run python -c "
from src.bot.dispatcher import bot, dp, setup_dispatcher
print('✓ Dispatcher importado')
setup_dispatcher()
print('✓ Dispatcher configurado')
print(f'Bot: {bot.__class__.__name__}')
"
```

### Prueba 2: arrancar servidor y probar health

```bash
# Terminal 1
uv run uvicorn src.main:app --reload --port 8000

# Terminal 2
curl http://localhost:8000/health
# → {"status":"OK","service":"telegram-ai-bot"}

curl http://localhost:8000/ready
# → {"status":"ready"}
```

### Prueba 3: enviar update simulado

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Telegram-Bot-Api-Secret-Token: tu_secreto" \
  -d '{"update_id": 1, "message": {"message_id": 1, "date": 1000000, "text": "hola", "chat": {"id": 1, "type": "private"}, "from": {"id": 1, "is_bot": false, "first_name": "Test"}}}'
```

### Prueba 4: ngrok + Telegram real

```bash
# 1. Iniciar servidor (Terminal 1)
uv run uvicorn src.main:app --reload --port 8000

# 2. Iniciar ngrok (Terminal 2)
ngrok http 8000

# 3. Copiar URL de ngrok a .env
# TELEGRAM_WEBHOOK_URL=https://abc123.ngrok-free.app

# 4. Ejecutar script de registro (Terminal 3)
uv run python -c "
import asyncio
from src.bot.dispatcher import bot
from src.core.config import settings

async def main():
    await bot.set_webhook(
        url=f'{settings.telegram_webhook_url}/webhook',
        secret_token=settings.telegram_webhook_secret,
        drop_pending_updates=True,
    )
    info = await bot.get_webhook_info()
    print(f'✓ Webhook: {info.url}')

asyncio.run(main())
"

# 5. Envía un mensaje a tu bot desde Telegram
```

---

## 4.11 DIAGRAMA DE FLUJO

```
TELEGRAM APP
    │
    │  Usuario envía: "@MiBot hola"
    ▼
TELEGRAM BOT API
    │
    │  POST /webhook (con secret_token)
    ▼
NGINX (producción) / NGROK (desarrollo)
    │
    ▼
FASTAPI - /webhook
    │
    │  verify_webhook() → verificar HMAC
    │  Update.model_validate_json() → parsear
    │  dp.feed_update() → pasar a Aiogram
    ▼
AIOGRAM DISPATCHER
    │
    │  MIDDLEWARE STACK (orden):
    │  1. LoggingMiddleware  → log update
    │  2. AuthMiddleware     → crear/buscar User en DB
    │  3. RateLimitMiddleware→ verificar Redis
    │  4. ContextMiddleware  → crear/buscar Chat en DB
    │
    │  FILTROS:
    │  - MentionFilter?      → ¿tiene @bot?
    │  - CommandFilter?      → ¿empieza con /?
    │
    ▼
HANDLER (commands / messages)
    │
    │  Procesar mensaje
    │  (por ahora: respuesta espejo)
    │  (Fase 5+: enviar a LLM)
    ▼
RESPUESTA A TELEGRAM
```


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
