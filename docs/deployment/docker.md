# 🐳 Despliegue con Docker

Guía completa para desplegar **Ain'tonio** usando Docker y Docker Compose.

## 📋 Requisitos Previos

- **Docker** 20.10+ instalado
- **Docker Compose** 2.0+ instalado
- **Token de Discord** del bot
- **Cuenta de DockerHub** (para el workflow de CI/CD)

## 🚀 Despliegue Rápido

### 1. Clonar el Repositorio

```bash
git clone <tu-repositorio>
cd discord_bot
```

### 2. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.docker.example .env

# Editar configuración
nano .env
```

**Configuración mínima requerida:**
```bash
DISCORD_TOKEN=tu_token_del_bot_discord
GUILD_ID=id_de_tu_servidor_discord
```

### 3. Ejecutar con Docker Compose

```bash
# Iniciar el bot
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener el bot
docker-compose down
```

## ⚙️ Configuración Detallada

### Variables de Entorno Importantes

| Variable | Descripción | Requerido | Ejemplo |
|----------|-------------|-----------|---------|
| `DISCORD_TOKEN` | Token del bot de Discord | ✅ | `MTEx...` |
| `GUILD_ID` | ID del servidor principal | 🔄 | `123456789` |
| `ENVIRONMENT` | Entorno de ejecución | ❌ | `production` |
| `LOG_LEVEL` | Nivel de logging | ❌ | `INFO` |
| `ADMIN_ROLE_IDS` | Roles de administrador | ❌ | `123,456,789` |

### Estructura de Archivos

```
discord_bot/
├── Dockerfile                 # Imagen del bot
├── docker-compose.yml        # Orquestación
├── .env                      # Variables de entorno
├── logs/                     # Logs persistentes
└── bot_data/                 # Datos del bot
```

## 🔧 Comandos Útiles

### Gestión del Contenedor

```bash
# Ver estado de los servicios
docker-compose ps

# Reiniciar el bot
docker-compose restart discord-bot

# Ver logs en tiempo real
docker-compose logs -f discord-bot

# Ejecutar comando dentro del contenedor
docker-compose exec discord-bot python -c "print('Hello from bot!')"

# Actualizar a la última imagen
docker-compose pull && docker-compose up -d
```

### Gestión de Logs

```bash
# Ver logs de las últimas 100 líneas
docker-compose logs --tail=100 discord-bot

# Ver logs desde una fecha específica
docker-compose logs --since="2024-01-01" discord-bot

# Limpiar logs viejos
docker system prune -f
```

### Backup de Datos

```bash
# Backup de logs
tar -czf backup-logs-$(date +%Y%m%d).tar.gz logs/

# Backup de datos del bot
tar -czf backup-data-$(date +%Y%m%d).tar.gz bot_data/
```

## 🔄 CI/CD con GitHub Actions

### Configurar Secrets en GitHub

Ve a tu repositorio → **Settings** → **Secrets and variables** → **Actions**

Crear los siguientes secrets:

| Secret | Descripción | Valor |
|--------|-------------|-------|
| `DOCKERHUB_USERNAME` | Usuario de DockerHub | `tu_usuario` |
| `DOCKERHUB_TOKEN` | Token de acceso | `dckr_pat_...` |

### Crear Token de DockerHub

1. Ve a [DockerHub](https://hub.docker.com) → **Account Settings**
2. **Security** → **New Access Token**
3. Nombre: `github-actions-aintonio`
4. Permisos: **Read, Write, Delete**
5. Copia el token generado

### Workflow Automático

El workflow se ejecuta automáticamente cuando:
- ✅ Haces push a `main`
- ✅ Creas un tag `v*` (ej: `v1.0.0`)
- ✅ Abres un Pull Request

**Para crear una nueva versión:**
```bash
git tag v1.0.1
git push origin v1.0.1
```

## 🛡️ Monitoreo y Salud

### Health Checks

El contenedor incluye health checks automáticos:

```bash
# Verificar salud del contenedor
docker-compose ps

# Ver detalles del health check
docker inspect aintonio-discord-bot | grep -A 10 Health
```

### Logs Estructurados

Los logs se guardan en formato JSON con rotación automática:
- **Tamaño máximo por archivo:** 10MB
- **Archivos máximos:** 3
- **Ubicación:** `./logs/`

### Métricas Básicas

```bash
# Uso de recursos del contenedor
docker stats aintonio-discord-bot

# Información del contenedor
docker inspect aintonio-discord-bot
```

## 🐛 Solución de Problemas

### El bot no se conecta

1. **Verificar token:**
   ```bash
   docker-compose logs discord-bot | grep -i token
   ```

2. **Verificar permisos:**
   - El bot tiene permisos en el servidor
   - Los Privileged Gateway Intents están habilitados

3. **Verificar conectividad:**
   ```bash
   docker-compose exec discord-bot ping discord.com
   ```

### Comandos no aparecen

1. **Verificar sincronización:**
   ```bash
   docker-compose logs discord-bot | grep -i "comandos"
   ```

2. **Para desarrollo (respuesta inmediata):**
   ```bash
   # En .env
   ENVIRONMENT=development
   GUILD_ID=tu_guild_id
   ```

3. **Para producción (hasta 1 hora):**
   ```bash
   # En .env
   ENVIRONMENT=production
   ```

### Logs no aparecen

```bash
# Verificar configuración de logging
docker-compose exec discord-bot ls -la logs/

# Verificar permisos
docker-compose exec discord-bot whoami
```

### Actualizar el Bot

```bash
# Método 1: Usando docker-compose
docker-compose pull
docker-compose up -d

# Método 2: Forzar recreación
docker-compose up -d --force-recreate

# Método 3: Imagen específica
docker-compose down
docker rmi raztor/aintonio-bot:latest
docker-compose up -d
```

## 📊 Configuración de Producción

### Límites de Recursos

Agrega al `docker-compose.yml`:

```yaml
services:
  discord-bot:
    # ... otras configuraciones
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.1'
          memory: 128M
```

### Reinicio Automático

```yaml
services:
  discord-bot:
    restart: unless-stopped  # Ya incluido
```

### Variables de Seguridad

```bash
# .env
ENVIRONMENT=production
LOG_LEVEL=WARNING  # Menos verboso en producción
```

## 🔄 Actualizaciones

### Automatización con Watchtower

```yaml
# Agregar al docker-compose.yml
services:
  watchtower:
    image: containrrr/watchtower
    container_name: watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_INCLUDE_STOPPED=true
      - WATCHTOWER_SCHEDULE=0 0 2 * * *  # Diario a las 2 AM
```

### Actualización Manual

```bash
# 1. Parar el bot
docker-compose down

# 2. Hacer backup
tar -czf backup-$(date +%Y%m%d).tar.gz logs/ bot_data/

# 3. Actualizar imagen
docker-compose pull

# 4. Iniciar con nueva imagen
docker-compose up -d

# 5. Verificar funcionamiento
docker-compose logs -f discord-bot
```

---

## 📞 Soporte

Si tienes problemas:
- 📖 Revisa los logs: `docker-compose logs discord-bot`
- 🐛 Reporta issues en el repositorio
- 💬 Contacta a los administradores

**¡Tu bot Ain'tonio está listo para servir a la comunidad! 🎉**