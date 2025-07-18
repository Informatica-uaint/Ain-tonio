"""
Configuración central del bot de Discord
Informatica UAIn'T Community Bot
"""

import os
import logging
from typing import List, Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Settings:
    """Configuración principal del bot"""

    # ====================================
    # CONFIGURACIÓN DISCORD
    # ====================================

    # Token del bot (OBLIGATORIO)
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")

    # Guild principal
    GUILD_ID: Optional[int] = None
    if os.getenv("GUILD_ID"):
        GUILD_ID = int(os.getenv("GUILD_ID"))

    # ====================================
    # CONFIGURACIÓN GENERAL
    # ====================================

    # Entorno de ejecución
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Prefijo de comandos tradicionales
    COMMAND_PREFIX: str = os.getenv("COMMAND_PREFIX", "!")

    # ====================================
    # CONFIGURACIÓN DE CANALES
    # ====================================

    # Canal de logs de moderación
    MOD_LOG_CHANNEL_ID: Optional[int] = None
    if os.getenv("MOD_LOG_CHANNEL_ID"):
        MOD_LOG_CHANNEL_ID = int(os.getenv("MOD_LOG_CHANNEL_ID"))

    # Canal de bienvenida
    WELCOME_CHANNEL_ID: Optional[int] = None
    if os.getenv("WELCOME_CHANNEL_ID"):
        WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))

    # ====================================
    # CONFIGURACIÓN DE ROLES
    # ====================================

    @property
    def ADMIN_ROLE_IDS(self) -> List[int]:
        """Lista de IDs de roles de administrador"""
        ids_str = os.getenv("ADMIN_ROLE_IDS", "")
        if not ids_str:
            return []
        return [int(id.strip()) for id in ids_str.split(",") if id.strip()]

    @property
    def MOD_ROLE_IDS(self) -> List[int]:
        """Lista de IDs de roles de moderador"""
        ids_str = os.getenv("MOD_ROLE_IDS", "")
        if not ids_str:
            return []
        return [int(id.strip()) for id in ids_str.split(",") if id.strip()]

    # Rol de miembro
    MEMBER_ROLE_ID: Optional[int] = None
    if os.getenv("MEMBER_ROLE_ID"):
        MEMBER_ROLE_ID = int(os.getenv("MEMBER_ROLE_ID"))

    # ====================================
    # CONFIGURACIÓN DE DESARROLLO
    # ====================================

    @property
    def IS_DEVELOPMENT(self) -> bool:
        """Verifica si estamos en modo desarrollo"""
        return self.ENVIRONMENT.lower() == "development"

    @property
    def IS_PRODUCTION(self) -> bool:
        """Verifica si estamos en modo producción"""
        return self.ENVIRONMENT.lower() == "production"

    # ====================================
    # VALIDACIÓN
    # ====================================

    def validate(self) -> None:
        """Valida que la configuración sea correcta"""
        errors = []

        if not self.DISCORD_TOKEN:
            errors.append("DISCORD_TOKEN es obligatorio")

        if self.DISCORD_TOKEN == "your_discord_bot_token_here":
            errors.append("Debes configurar un DISCORD_TOKEN válido")

        if errors:
            raise ValueError(
                f"Errores de configuración:\n" +
                "\n".join(f"- {error}" for error in errors)
            )

    # ====================================
    # INFORMACIÓN DEL BOT
    # ====================================

    BOT_NAME: str = "Ain'tonio"
    BOT_VERSION: str = "1.0.0"
    BOT_DESCRIPTION: str = "Bot multifuncional para la comunidad de Informática UAIn'T"
    BOT_AUTHOR: str = "Informatica UAIn'T Community"

    # ====================================
    # CONFIGURACIÓN DE LOGGING
    # ====================================

    def setup_logging(self) -> None:
        """Configura el sistema de logging"""
        import colorlog

        # Configurar el nivel de logging
        log_level = getattr(logging, self.LOG_LEVEL.upper(), logging.INFO)

        # Formato para desarrollo (con colores)
        if self.IS_DEVELOPMENT:
            formatter = colorlog.ColoredFormatter(
                "%(log_color)s%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                }
            )
        else:
            # Formato para producción (sin colores)
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

        # Configurar handler
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        # Configurar logger raíz
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        root_logger.handlers.clear()
        root_logger.addHandler(handler)

        # Silenciar logs muy verbosos de discord.py en producción
        if not self.IS_DEVELOPMENT:
            logging.getLogger('discord').setLevel(logging.WARNING)
            logging.getLogger('discord.http').setLevel(logging.WARNING)


# Instancia global de configuración
settings = Settings()


def get_settings() -> Settings:
    """Obtiene la instancia de configuración"""
    return settings