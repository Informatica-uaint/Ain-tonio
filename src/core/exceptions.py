"""
Excepciones personalizadas para el bot de Discord
Informatica UAIn'T Community Bot
"""

import discord
from typing import Optional


class BotException(Exception):
    """Excepción base para el bot"""

    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(message)
        self.user_message = user_message or message


class ConfigurationError(BotException):
    """Error de configuración del bot"""
    pass


class PermissionError(BotException):
    """Error de permisos insuficientes"""

    def __init__(self, message: str, required_permission: Optional[str] = None):
        super().__init__(message)
        self.required_permission = required_permission


class UserNotFoundError(BotException):
    """Usuario no encontrado"""
    pass


class ChannelNotFoundError(BotException):
    """Canal no encontrado"""
    pass


class RoleNotFoundError(BotException):
    """Rol no encontrado"""
    pass


class CommandError(BotException):
    """Error genérico de comando"""
    pass


class ModerationError(BotException):
    """Error relacionado con moderación"""
    pass


class DatabaseError(BotException):
    """Error de base de datos"""
    pass


class APIError(BotException):
    """Error de API externa"""
    pass


class RateLimitError(BotException):
    """Error de límite de tasa"""

    def __init__(self, message: str, retry_after: Optional[float] = None):
        super().__init__(message)
        self.retry_after = retry_after


# ====================================
# HELPERS PARA MANEJO DE ERRORES
# ====================================

def format_discord_error(error: discord.DiscordException) -> str:
    """Formatea errores de Discord para mostrar al usuario"""

    if isinstance(error, discord.Forbidden):
        return "❌ No tengo permisos suficientes para realizar esta acción."

    elif isinstance(error, discord.NotFound):
        return "❌ El recurso solicitado no fue encontrado."

    elif isinstance(error, discord.HTTPException):
        if error.status == 429:  # Rate limit
            return "⏰ Demasiadas peticiones. Espera un momento e inténtalo de nuevo."
        return f"❌ Error de conexión con Discord: {error.text}"

    elif isinstance(error, discord.LoginFailure):
        return "❌ Error de autenticación con Discord. Verifica el token del bot."

    elif isinstance(error, discord.ConnectionClosed):
        return "❌ Conexión con Discord perdida. Intentando reconectar..."

    else:
        return f"❌ Error inesperado: {str(error)}"


def is_user_error(error: Exception) -> bool:
    """Determina si el error es causado por el usuario"""

    user_errors = (
        PermissionError,
        UserNotFoundError,
        ChannelNotFoundError,
        RoleNotFoundError,
        CommandError,
        discord.Forbidden,
        discord.NotFound
    )

    return isinstance(error, user_errors)


def should_log_error(error: Exception) -> bool:
    """Determina si el error debe ser loggeado"""

    # No loggear errores de usuario comunes
    if is_user_error(error):
        return False

    # No loggear rate limits (son esperados)
    if isinstance(error, (RateLimitError, discord.HTTPException)):
        if hasattr(error, 'status') and error.status == 429:
            return False

    return True


def get_error_embed(error: Exception, title: str = "Error") -> discord.Embed:
    """Crea un embed para mostrar errores al usuario"""

    embed = discord.Embed(
        title=f"❌ {title}",
        color=discord.Color.red(),
        timestamp=discord.utils.utcnow()
    )

    if isinstance(error, BotException) and error.user_message:
        embed.description = error.user_message
    else:
        embed.description = format_discord_error(error)

    return embed