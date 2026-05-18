# Deployment — Railway

Guía para deployar el proyecto en Railway.

## Requisitos previos

- Repositorio en GitHub con el código en `main` o `develop`
- Cuenta en [Railway](https://railway.app)
- OpenAI API Key con saldo disponible

---

## Setup inicial

### 1. Crear proyecto en Railway

1. Ir a https://railway.app y hacer login
2. Click en **New Project** → **Deploy from GitHub repo**
3. Autorizar Railway en GitHub y seleccionar el repositorio `promptior-rag-challenge`

### 2. Configurar rama de deploy

1. En el dashboard del proyecto, ir a **Settings**
2. Sección **Deploy** → **Deploy from branch**
3. Seleccionar `main` (o `develop` si se quiere deployar desde ahí)
4. Guardar

Railway hace deploy automático en cada push a esa rama.

### 3. Verificar detección del framework

Railway detecta proyectos Python por la presencia de `requirements.txt` y `Procfile`. Si el build falla por no encontrar el entrypoint, verificar que el `Procfile` existe y tiene el contenido correcto:

```
web: uvicorn server:app --host 0.0.0.0 --port $PORT
```

---

## Variables de entorno

En el dashboard del proyecto, ir a **Variables** y agregar:

| Variable | Requerida | Valor por defecto |
|----------|-----------|-------------------|
| `OPENAI_API_KEY` | Sí | — |
| `LLM_MODEL` | No | `gpt-4o-mini` |
| `EMBEDDING_MODEL` | No | `text-embedding-3-small` |
| `TOP_K` | No | `3` |
| `LLM_TEMPERATURE` | No | `0.7` |

No commitear variables sensibles al repositorio. Railway las inyecta en el runtime.

---

## Deploy

El deploy se dispara automáticamente con cada push a la rama configurada. Para hacer un deploy manual:

1. Ir a **Deployments** en el dashboard
2. Click en **Deploy Now**

El estado pasa por `Building` → `Deploying` → `Success`. El tiempo típico es 2-5 minutos.

**URL de producción**: `https://promptior-rag-challenge-production.up.railway.app`

---

## Verificar que funciona

Una vez completado el deploy, validar los endpoints:

```bash
# Health check
curl https://promptior-rag-challenge-production.up.railway.app/

# Swagger UI
curl https://promptior-rag-challenge-production.up.railway.app/docs

# Query al RAG
curl -X POST https://promptior-rag-challenge-production.up.railway.app/promptior/invoke \
  -H "Content-Type: application/json" \
  -d '{"input": "¿Qué es Promtior?"}'
```

Los tres deberían retornar `200 OK`.

### Cold start

En el primer deploy, el servidor tarda entre 30 y 60 segundos adicionales porque construye el vectorstore desde cero (descarga web + PDF, genera embeddings, persiste en ChromaDB). Los deploys posteriores arrancan más rápido porque el índice ya existe.

Secuencia esperada en logs:

```
[ingest] Cargando web...
[ingest] Cargando PDF...
[ingest] Vectorstore built successfully
INFO: Application startup complete
INFO: Uvicorn running on http://0.0.0.0:8080
```

---

## Troubleshooting

**Build falla con `BUILD FAILED`**
- Revisar logs exactos en el dashboard
- Correr `pip install -r requirements.txt` localmente para descartar errores en el archivo

**Servidor no inicia**
- Verificar que `OPENAI_API_KEY` está configurada en Variables
- Verificar el contenido del `Procfile`
- Correr `python server.py` localmente para reproducir el error

**502 Bad Gateway**
- Esperar 60 segundos y reintentar (puede ser cold start aún en progreso)
- Revisar los logs de `[ingest]` por errores de construcción del vectorstore
- Si persiste, hacer redeploy desde **Deployments** → **Redeploy**

**`ValueError: OPENAI_API_KEY no configurada`**
- Confirmar que la variable existe en Railway Variables y no está vacía
- Hacer redeploy después de agregar la variable

**Vectorstore tarda 2-3 minutos en construirse**
- Es el comportamiento esperado en el primer deploy
- Los deploys siguientes son más rápidos

---

Versión 1.0 — Mayo 2026
