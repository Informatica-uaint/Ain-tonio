# 📖 Guía de Instalación

Guía paso a paso para instalar y configurar el bot **Ain'tonio** para la comunidad de Informática UAIn'T.

## 📋 Requisitos Previos

### Sistema
- **Python 3.8+** (recomendado Python 3.10+)
- **pip** (gestor de paquetes de Python)
- **Git** (para clonar el repositorio)

### Discord
- Una **aplicación de bot** creada en [Discord Developer Portal](https://discord.com/developers/applications)
- **Token del bot** de la aplicación
- **Permisos necesarios** en tu servidor de Discord

## 🚀 Instalación Rápida

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd discord_bot
```

### 2. Ejecutar Script de Configuración

```bash
# Hacer ejecutable el script
chmod +x scripts/setup.sh

# Ejecutar configuración
./scripts/setup.sh
```

El script automáticamente:
- ✅ Verifica Python y pip
- ✅ Crea entorno virtual (opcional)
- ✅ Instala dependencias
- ✅ Crea archivo .env
- ✅ Crea directorios necesarios

### 3. Configurar Variables de Entorno

Edita el archivo `.env` y configura:

```bash
# OBLIGATORIO
DISCORD_TOKEN=tu_token_aqui

# RECOMENDADO
GUILD_ID=id_de_tu_servidor

# OPCIONAL
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### 4. Ejecutar el Bot

```bash
python3 src/bot/main.py
```

## 🔧 Instalación Manual

Si prefieres no usar el script de configuración:

### 1. Crear Entorno Virtual (Recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Crear directorios
mkdir -p logs src/bot/resources/{images,sounds,data,locales}
```

### 4. Configurar .env

Edita `.env` con tu editor favorito:

```bash
nano .env
# o
code .env
```

## 🔑 Configuración del Bot de Discord

### 1. Crear Aplicación

1. Ve a [Discord Developer Portal](https://discord.com/developers/applications)
2. Click en "New Application"
3. Nombra tu aplicación (ej: "Ain'tonio UAIn'T")
4. Guarda los cambios

### 2. Crear Bot

1. Ve a la sección "Bot" en el panel izquierdo
2. Click en "Add Bot"
3. Copia el **Token** (¡mantenlo seguro!)
4. Pégalo en tu archivo `.env` como `DISCORD_TOKEN`

### 3. Configurar Permisos

En la sección "Bot", habilita los siguientes **Privileged Gateway Intents**:
- ✅ **Message Content Intent**
- ✅ **Server Members Intent**
- ✅ **Presence Intent** (opcional)

### 4. Invitar Bot al Servidor

1. Ve a la sección "OAuth2" > "URL Generator"
2. Selecciona **Scopes**: `bot` y `applications.commands`
3. Selecciona **Bot Permissions**:
   - ✅ Read Messages/View Channels
   - ✅ Send Messages
   - ✅ Use Slash Commands
   - ✅ Embed Links
   - ✅ Read Message History
   - ✅ Add Reactions
   - ✅ Manage Messages (para moderación futura)
4. Copia la URL generada y úsala para invitar el bot

### 5. Obtener Guild ID (Opcional pero Recomendado)

1. Habilita **Modo Desarrollador** en Discord (Configuración > Avanzado > Modo desarrollador)
2. Haz click derecho en tu servidor
3. Click en "Copiar ID"
4. Pégalo en tu archivo `.env` como `GUILD_ID`

## ✅ Verificación

### 1. Verificar Configuración

```bash
# El bot debería mostrar información de configuración al iniciar
python3 src/bot/main.py
```

Si todo está correcto, verás:
```
🤖 Ain'tonio v1.0.0
Bot multifuncional para la comunidad de Informática UAIn'T

📋 Información:
• Entorno: DEVELOPMENT
• Log Level: INFO
• Guild ID: 1234567890

🚀 Iniciando bot...
```

### 2. Probar Comandos

En tu servidor de Discord, prueba:
- `!ping` - Verifica latencia
- `!info` - Información del bot
- `/servidor` - Información del servidor
- `/usuario` - Tu información

## 🐛 Solución de Problemas

### Error: "DISCORD_TOKEN es obligatorio"
- ✅ Verifica que el archivo `.env` existe
- ✅ Verifica que `DISCORD_TOKEN` está configurado correctamente
- ✅ Asegúrate de que no hay espacios extra en el token

### Error: "Privileged intent provided when not enabled"
- ✅ Habilita los **Privileged Gateway Intents** en Discord Developer Portal
- ✅ Reinicia el bot después de cambiar los intents

### Bot aparece offline
- ✅ Verifica que el token es correcto
- ✅ Verifica que el bot tiene permisos en el servidor
- ✅ Revisa los logs en consola para errores

### Comandos slash no aparecen
- ✅ Asegúrate de que el bot tiene permiso `applications.commands`
- ✅ Los comandos pueden tardar hasta 1 hora en sincronizarse globalmente
- ✅ En desarrollo, configura `GUILD_ID` para sincronización inmediata

## 📚 Próximos Pasos

Una vez que el bot esté funcionando:

1. **Familiarízate** con los comandos básicos
2. **Configura roles** de admin/moderador en `.env`
3. **Configura canales** específicos para logs
4. **Lee la documentación** en `docs/` para más funcionalidades

## 🆘 Soporte

Si tienes problemas:
- 📖 Revisa la documentación en `docs/`
- 🐛 Reporta bugs en el repositorio
- 💬 Contacta a los administradores de la comunidad