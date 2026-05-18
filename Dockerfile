# ---- Stage 1: build del frontend ----
# Node solo se usa para compilar la SPA; no queda en la imagen final.
FROM node:20-slim AS web-build
WORKDIR /web

# Cacheable: instala deps antes de copiar el código.
COPY web/package.json web/package-lock.json ./
RUN npm ci

COPY web/ ./
RUN npm run build


# ---- Stage 2: runtime Python ----
FROM python:3.11-slim AS runtime
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=utf-8

# Cacheable: deps Python antes del código.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Backend (solo lo necesario; chroma_db NO se copia: se reconstruye en
# el primer arranque, igual que en el proceso actual).
COPY app/ ./app/
COPY data/ ./data/
COPY server.py ./

# Frontend ya buildeado, en la ruta que espera server.py (web/dist).
COPY --from=web-build /web/dist ./web/dist

EXPOSE 8000

# Railway inyecta $PORT; fallback a 8000 para correr la imagen en local.
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}"]
