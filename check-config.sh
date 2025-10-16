#!/bin/bash

echo "🔍 Verificando configuración del proyecto..."

# Verificar que el archivo .env existe
if [ -f .env ]; then
    echo "✅ Archivo .env encontrado"
    source .env
else
    echo "❌ Archivo .env no encontrado"
    echo "💡 Copia .env.example a .env y configura las variables"
    exit 1
fi

# Verificar variables críticas
required_vars=(
    "MYSQL_ROOT_PASSWORD"
    "MYSQL_DATABASE" 
    "MYSQL_USER"
    "MYSQL_PASSWORD"
    "DATABASE_URL"
    "SECRET_KEY"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Variable $var no está configurada"
        exit 1
    else
        echo "✅ $var: ${!var:0:10}..."  # Mostrar solo primeros 10 caracteres por seguridad
    fi
done

echo "🎉 Configuración verificada correctamente"
echo "🚀 Para iniciar el proyecto ejecuta: docker compose up -d"