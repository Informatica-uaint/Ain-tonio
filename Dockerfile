# ====================================
# DOCKERFILE - Ain'tonio Discord Bot
# ====================================

# Base image con Python 3.10
FROM python:3.10-slim

# Metadata
LABEL maintainer="Raztor"
LABEL description="Ain'tonio Discord Community Bot"
LABEL version="1.0.0"

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app/src/bot

# Crear usuario no-root para seguridad
RUN groupadd -r botuser && useradd -r -g botuser botuser

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ ./src/
COPY config/ ./config/

# Crear directorios necesarios
RUN mkdir -p logs && \
    mkdir -p src/bot/resources/images && \
    mkdir -p src/bot/resources/sounds && \
    mkdir -p src/bot/resources/data && \
    mkdir -p src/bot/resources/locales

# Cambiar propietario de archivos al usuario no-root
RUN chown -R botuser:botuser /app

# Cambiar a usuario no-root
USER botuser

# Puerto (aunque el bot de Discord no expone puertos HTTP por ahora)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Comando por defecto
CMD ["python", "src/bot/main.py"]