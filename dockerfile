FROM python:3.12-slim

WORKDIR /app

# Configurar Python path
ENV PYTHONPATH=/app

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY app/ .

# Verificar que los archivos estén correctos
RUN echo "=== Verificando estructura ===" && \
    ls -la && \
    echo "=== Verificando routes ===" && \
    cat routes/user_routes.py && \
    echo "=== Verificando schemas ===" && \
    cat schemas/user_schema.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]