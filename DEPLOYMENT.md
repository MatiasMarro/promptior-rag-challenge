# Deployment — Railway

Guía para deployar el proyecto en Railway usando el `Dockerfile`.

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

### 3. Configurar el builder (importante)

Railway usa **Railpack** por defecto, que **ignora `nixpacks.toml`** y solo
detecta Python — por lo que el frontend nunca se buildea. Este proyecto se
deploya con un **Dockerfile multi-stage** (Node compila la SPA, Python sirve
todo). Configurar:

1. **Settings → Build → Builder** → seleccionar **Dockerfile**
2. **Custom Build Command** → dejar **vacío** (lo maneja el Dockerfile)
3. **Custom Start Command** → dejar **vacío** (usa el `CMD` del Dockerfile,
   que ya bindea `$PORT`)
4. **Settings → Deploy → Healthcheck Path** → `/health`
5. **Healthcheck Timeout** → `300` (ver sección Cold start)

> El `Procfile` y `nixpacks.toml` quedan inertes con el builder Dockerfile;
> no hace falta borrarlos.

---

## Variables de entorno

En el dashboard del proyecto, ir a **Variables** y agregar:

| Variable | Requerida | Notas |
|----------|-----------|-------|
| `OPENAI_API_KEY` | Sí | Única variable leída del entorno |

`app/config.py` lee **solo `OPENAI_API_KEY`**. El resto (`LLM_MODEL`,
`EMBEDDING_MODEL`, `TOP_K=4`, `LLM_TEMPERATURE=0`, paths, URLs) son
**constantes hardcodeadas** en ese archivo — no se overridean por entorno.
Sin `OPENAI_API_KEY`, la app tira `ValueError` al importar y no arranca.

---

## Deploy

El deploy se dispara automáticamente con cada push a la rama configurada. Para hacer un deploy manual:

1. Ir a **Deployments** en el dashboard
2. Click en **Redeploy**

El estado pasa por `Building` → `Deploying` → `Success`. Con el Dockerfile el
build tarda unos minutos (instala deps Python + `npm ci` + `npm run build`).

**URL de producción**: `https://promtior-rag-challenge-production.up.railway.app`

---

## Verificar que funciona

Una vez completado el deploy, validar los endpoints (reemplazar `<URL>`):

```bash
# Frontend (debe devolver el HTML de la SPA, con id="root")
curl https://<URL>/

# Health check (JSON de estado)
curl https://<URL>/health

# Query al RAG
curl -X POST https://<URL>/promtior/invoke \
  -H "Content-Type: application/json" \
  -d '{"input": "What is Promtior?"}'
```

`GET /` debe devolver HTML con `<div id="root">` (SPA sirviéndose),
`/health` un JSON `200`, y `/promtior/invoke` `{"output": "..."}`.

> Nota: `/docs` puede mostrar el Swagger vacío porque `/openapi.json` da 500
> por un desajuste pre-existente de LangServe/Pydantic. No afecta a
> `/promtior/invoke` ni al playground.

### Cold start

`chroma_db/` **no está versionado** (decisión del proyecto). Por eso, en cada
deploy nuevo (contenedor fresco) el primer arranque reconstruye el vectorstore
desde cero (descarga web + PDF, genera embeddings, persiste en ChromaDB),
agregando 30-90 segundos. Dentro de la misma instancia, los reinicios
posteriores cargan el índice ya persistido.

Por eso conviene subir el **Healthcheck Timeout a ~300s**: si el healthcheck
expira durante la reconstrucción, Railway marca el deploy como fallido aunque
el build esté bien.

Secuencia esperada en logs:

```
[ingest] Loading web: https://promtior.ai/
[ingest] Loading PDF: ./data/AI_Engineer.pdf
[ingest] Vectorstore built successfully
INFO: Application startup complete
INFO: Uvicorn running on http://0.0.0.0:<PORT>
```

---

## Troubleshooting

**En los Build Logs no aparece `npm`/`vite`**
- El builder no es Dockerfile. Ir a **Settings → Build → Builder** y
  seleccionar **Dockerfile**. Redeploy.

**`GET /` devuelve 404 o el JSON de `/health` en vez de la SPA**
- `web/dist` no quedó en la imagen. Revisar en los Build Logs que la etapa
  Node corrió `npm run build` y que el `COPY --from=web-build` no falló.

**Build falla en `pip install` (ej. compilando una wheel)**
- `python:3.11-slim` no trae toolchain. Cambiar la imagen base del stage
  runtime del `Dockerfile` a `python:3.11` (full) y redeploy.

**Servidor no inicia / `ValueError: OPENAI_API_KEY no configurada`**
- Confirmar que `OPENAI_API_KEY` existe en Railway Variables y no está vacía
- Redeploy después de agregar la variable

**502 Bad Gateway o "healthcheck failed" tras el deploy**
- Suele ser el cold start del vectorstore aún en progreso
- Subir el **Healthcheck Timeout** a ~300s
- Revisar los logs de `[ingest]` por errores de construcción

---

Versión 1.0 — Mayo 2026
