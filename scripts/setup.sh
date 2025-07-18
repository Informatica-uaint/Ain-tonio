#!/bin/bash

# Script de configuración inicial para el bot de Discord
# Informatica UAIn'T Community Bot

set -e  # Salir si hay algún error

echo "🤖 Configuración inicial del bot Ain'tonio"
echo "=========================================="

# Verificar Python
echo "📋 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION encontrado"

if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
    echo "✅ Versión de Python compatible"
else
    echo "❌ Se requiere Python 3.8 o superior"
    exit 1
fi

# Verificar pip
echo "📦 Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado"
    exit 1
fi
echo "✅ pip3 encontrado"

# Crear entorno virtual (opcional)
read -p "¿Quieres crear un entorno virtual? (recomendado) [y/N]: " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "🔧 Creando entorno virtual..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado en './venv'"
    echo "💡 Para activarlo usa: source venv/bin/activate"

    # Activar entorno virtual
    source venv/bin/activate
    echo "✅ Entorno virtual activado"
fi

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip3 install -r requirements.txt
echo "✅ Dependencias instaladas"

# Configurar archivo .env
echo "⚙️ Configurando variables de entorno..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Archivo .env creado desde .env.example"
else
    echo "⚠️  El archivo .env ya existe"
fi

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p logs
mkdir -p src/bot/resources/images
mkdir -p src/bot/resources/sounds
mkdir -p src/bot/resources/data
mkdir -p src/bot/resources/locales
echo "✅ Directorios creados"

# Información importante
echo ""
echo "🎉 ¡Configuración completada!"
echo "=========================="
echo ""
echo "📝 Próximos pasos:"
echo "1. Edita el archivo .env y configura tu DISCORD_TOKEN"
echo "2. Opcionalmente configura GUILD_ID para tu servidor"
echo "3. Ejecuta el bot con: python3 src/bot/main.py"
echo ""
echo "📖 Información importante:"
echo "• Token del bot: https://discord.com/developers/applications"
echo "• ID del servidor: Habilita modo desarrollador en Discord y haz click derecho en tu servidor"
echo ""
echo "🆘 Si necesitas ayuda, revisa la documentación en docs/"
echo ""

# Verificar si el token está configurado
if grep -q "your_discord_bot_token_here" .env 2>/dev/null; then
    echo "⚠️  IMPORTANTE: Recuerda configurar tu DISCORD_TOKEN en el archivo .env"
fi

echo "✅ ¡Setup completado exitosamente!"