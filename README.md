# 🤖 Ain'tonio Discord Community Bot

Bot multifuncional de Discord desarrollado en Python para gestión completa de una comunidad.

## 📁 Estructura del Proyecto

```
discord_bot/
├── 📄 README.md                   # Documentación principal
├── 📄 requirements.txt            # Dependencias Python
├── 🐳 docker-compose.yml          # Contenedores
├── ⚙️ .env.example                # Variables de entorno
│
├── 📚 docs/                       # Documentación
├── 🔧 scripts/                    # Scripts de automatización
├── ⚙️ config/                     # Configuraciones
├── 🧪 tests/                      # Tests unitarios
├── 🚀 deployment/                 # Archivos de despliegue
├── 📦 migrations/                 # Migraciones de BD
│
├── 🌐 dashboard/                  # Dashboard web (opcional)
│   ├── frontend/                  # React/Vue app
│   └── backend/                   # API separada
│
└── 📂 src/                        # 🎯 CÓDIGO PRINCIPAL
    └── bot/
        ├── 🚀 main.py             # Punto de entrada
        ├── 🤖 bot.py              # Cliente principal
        │
        ├── ⚡ core/               # Núcleo del bot
        │   ├── client.py          # Cliente personalizado
        │   ├── events.py          # Eventos globales
        │   └── exceptions.py      # Excepciones custom
        │
        ├── 🎮 cogs/               # Módulos de comandos
        │   ├── admin/             # 👑 Administración
        │   ├── moderation/        # 🛡️ Moderación & AutoMod
        │   ├── community/         # 🌟 Bienvenida, Niveles, Roles
        │   ├── entertainment/     # 🎵 Música, Juegos, Diversión
        │   ├── economy/           # 💰 Sistema económico
        │   ├── utility/           # 🔧 Herramientas útiles
        │   └── support/           # 🎫 Tickets & Soporte
        │
        ├── 🗄️ database/           # Capa de datos
        │   ├── models/            # Modelos de BD
        │   └── repositories/      # Acceso a datos
        │
        ├── 🔧 services/           # Lógica de negocio
        ├── 🛠️ utils/              # Utilidades y helpers
        │
        ├── 🌐 api/                # API para dashboard
        │   ├── routes/            # Endpoints REST
        │   ├── schemas/           # Validación de datos
        │   └── middleware/        # Auth, CORS, Rate limit
        │
        └── 📦 resources/          # Recursos estáticos
            ├── images/            # Avatars, banners, memes
            ├── sounds/            # Audio para música
            ├── data/              # JSONs de configuración
            └── locales/           # Idiomas (es, en, pt)
```

## 🎯 Módulos Principales

| Módulo | Descripción | Estado |
|--------|-------------|--------|
| **🛡️ Moderation** | Ban, kick, mute, warns, automod | 🚧 Planificado |
| **🌟 Community** | Bienvenida, niveles XP, auto-roles | 🚧 Planificado |
| **💰 Economy** | Dinero virtual, tienda, apuestas | 🚧 Planificado |
| **🎵 Music** | Reproducción de música, playlists | 🚧 Planificado |
| **🎫 Support** | Sistema de tickets, reportes | 🚧 Planificado |
| **🔧 Utility** | Info servidor/usuario, herramientas | 🚧 Planificado |
| **🌐 Dashboard** | Panel web de administración | 🚧 Planificado |

## 🚀 Inicio Rápido

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd discord_bot

# 2. Configurar entorno
cp .env.example .env
# Editar .env con tu token de Discord

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar bot
python src/bot/main.py
```

## 🛠️ Stack Tecnológico

- **🐍 Python 3.10+** - Lenguaje principal
- **🤖 discord.py 2.3+** - Librería de Discord
- **🗄️ PostgreSQL** - Base de datos
- **⚡ FastAPI** - API REST para dashboard
- **🐳 Docker** - Contenedorización
- **🧪 pytest** - Testing

## 📋 Características Planificadas

### 🛡️ Sistema de Moderación
- ✅ Comandos básicos (ban, kick, mute)
- ✅ Sistema de advertencias
- ✅ Auto-moderación inteligente
- ✅ Logs de moderación

### 🌟 Gestión de Comunidad
- ✅ Mensajes de bienvenida personalizables
- ✅ Sistema de niveles y experiencia
- ✅ Auto-roles por reacciones
- ✅ Eventos y sorteos

### 💰 Sistema Económico
- ✅ Moneda virtual del servidor
- ✅ Tienda personalizable
- ✅ Minijuegos y apuestas
- ✅ Recompensas por actividad

### 🌐 Dashboard Web
- ✅ Panel de administración
- ✅ Estadísticas en tiempo real
- ✅ Configuración visual
- ✅ Gestión de moderación

## 📞 Soporte

- **📖 Documentación**: `docs/`
- **🐛 Issues**: GitHub Issues

---

## Licencia

Este bot está licenciado bajo la [GNU AGPLv3](LICENSE).  
Puedes modificarlo y compartirlo, siempre que mantengas los créditos y distribuyas el código bajo la misma licencia.  
No se permite el uso comercial sin autorización previa.

*Bot desarrollado con ❤️ para la comunidad*


