"""
Cliente personalizado del bot de Discord
Informatica UAIn'T Community Bot
"""

import logging
from typing import Optional, List
import discord
from discord.ext import commands

from config import get_settings
from .exceptions import ConfigurationError, format_discord_error, should_log_error

logger = logging.getLogger(__name__)


class UaintBot(commands.Bot):
    """Cliente personalizado del bot con funcionalidades específicas"""

    def __init__(self):
        # Obtener configuración
        self.settings = get_settings()

        # Configurar intents
        intents = discord.Intents.default()
        intents.message_content = True  # Necesario para comandos de texto
        intents.members = True  # Para eventos de miembros
        intents.guilds = True  # Para información de servidores
        intents.guild_messages = True  # Para mensajes en servidores
        intents.guild_reactions = True  # Para reacciones

        # Inicializar bot
        super().__init__(
            command_prefix=self._get_prefix,
            intents=intents,
            description=self.settings.BOT_DESCRIPTION,
            help_command=None,  # Usaremos comando personalizado
            case_insensitive=True,
            strip_after_prefix=True
        )

        # Estado del bot
        self.is_ready = False
        self.start_time = discord.utils.utcnow()

        # Guild principal
        self.main_guild: Optional[discord.Guild] = None

        logger.info(f"Inicializando {self.settings.BOT_NAME} v{self.settings.BOT_VERSION}")

    async def _get_prefix(self, bot, message: discord.Message) -> List[str]:
        """Determina el prefijo de comandos"""
        # Prefijo por defecto
        prefixes = [self.settings.COMMAND_PREFIX]

        # En DMs, también aceptar sin prefijo
        if message.guild is None:
            prefixes.append("")

        # Siempre aceptar menciones
        return commands.when_mentioned_or(*prefixes)(bot, message)

    async def setup_hook(self) -> None:
        """Se ejecuta durante la configuración inicial del bot"""
        logger.info("Configurando bot...")

        # Validar configuración
        try:
            self.settings.validate()
        except ValueError as e:
            raise ConfigurationError(str(e))

        # Configurar logging
        self.settings.setup_logging()

        logger.info("Bot configurado correctamente")

    async def sync_commands(self) -> None:
        """Sincroniza los comandos slash con Discord"""
        try:
            logger.info("🔄 Sincronizando comandos...")

            # Ver comandos disponibles
            tree_commands = self.tree.get_commands()
            logger.info(f"📋 Comandos disponibles: {[cmd.name for cmd in tree_commands]}")

            # En desarrollo: sync para guild específico para rapidez
            # En producción: sync global para alcance completo
            if self.settings.IS_DEVELOPMENT and self.settings.GUILD_ID:
                # Copiar comandos globales al guild específico
                guild = discord.Object(id=self.settings.GUILD_ID)

                # Limpiar comandos del guild primero
                self.tree.clear_commands(guild=guild)

                # Copiar cada comando global al guild
                for cmd in tree_commands:
                    self.tree.add_command(cmd, guild=guild)
                    logger.debug(f"📋 Comando {cmd.name} copiado al guild")

                # Sincronizar el guild
                synced = await self.tree.sync(guild=guild)
                logger.info(f"✅ Sincronizados {len(synced)} comandos en guild {self.settings.GUILD_ID} (desarrollo)")
                logger.info("⚡ Comandos disponibles inmediatamente en el servidor de desarrollo")

            else:
                # Sincronización global para producción
                synced = await self.tree.sync()
                logger.info(f"✅ Sincronizados {len(synced)} comandos globalmente")
                logger.info("⏰ Los comandos pueden tardar hasta 1 hora en aparecer")

            # Mostrar comandos sincronizados
            if synced:
                names = []
                for cmd in synced:
                    if isinstance(cmd, dict):
                        names.append(cmd.get('name', 'unknown'))
                    else:
                        names.append(getattr(cmd, 'name', str(cmd)))
                logger.info(f"🎯 Comandos sincronizados: {names}")
            else:
                logger.warning("⚠️ No se sincronizaron comandos")

        except Exception as e:
            logger.error(f"❌ Error sincronizando comandos: {e}")
            import traceback
            logger.error(traceback.format_exc())


    async def on_ready(self) -> None:
        """Se ejecuta cuando el bot está listo"""
        if self.is_ready:
            return  # Evitar múltiples ejecuciones

        self.is_ready = True

        # Obtener guild principal
        if self.settings.GUILD_ID:
            self.main_guild = self.get_guild(self.settings.GUILD_ID)
            if not self.main_guild:
                logger.warning(f"No se pudo encontrar el guild {self.settings.GUILD_ID}")

        # Información del bot
        logger.info(f"🤖 {self.user.name} está listo!")
        logger.info(f"📊 Conectado a {len(self.guilds)} servidor(es)")
        logger.info(f"👥 Sirviendo a {len(self.users)} usuario(s)")

        if self.main_guild:
            logger.info(f"🏠 Guild principal: {self.main_guild.name} ({self.main_guild.member_count} miembros)")

        # SINCRONIZAR COMANDOS AQUÍ (cuando el bot ya está listo)
        if self.settings.IS_DEVELOPMENT:
            logger.info("🔄 Sincronizando comandos slash...")

            # Cambiar temporalmente a DEBUG para ver más detalles
            original_level = logging.getLogger().level
            logging.getLogger().setLevel(logging.DEBUG)

            await self.sync_commands()

            # Restaurar nivel original
            logging.getLogger().setLevel(original_level)

        # Establecer estado del bot
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="la comunidad de Informática UAIn'T"
            ),
            status=discord.Status.online
        )

        logger.info("✅ Bot inicializado completamente")

    async def on_error(self, event_method: str, *args, **kwargs) -> None:
        """Maneja errores globales del bot"""
        logger.exception(f"Error en evento {event_method}")

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """Maneja errores de comandos"""

        # Ignorar comandos no encontrados
        if isinstance(error, commands.CommandNotFound):
            return

        # Errores de permisos
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(
                "❌ No tienes permisos suficientes para usar este comando.",
                delete_after=10
            )
            return

        # Errores de argumentos
        if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            await ctx.reply(
                f"❌ Uso incorrecto del comando. Usa `{ctx.prefix}help {ctx.command}` para más información.",
                delete_after=10
            )
            return

        # Comando en cooldown
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(
                f"⏰ Comando en cooldown. Inténtalo en {error.retry_after:.1f} segundos.",
                delete_after=5
            )
            return

        # Errores de Discord
        if isinstance(error, commands.CommandInvokeError):
            original = error.original

            if isinstance(original, discord.DiscordException):
                message = format_discord_error(original)
                await ctx.reply(message, delete_after=10)

                if should_log_error(original):
                    logger.error(f"Error de Discord en comando {ctx.command}: {original}")
                return

        # Error genérico
        logger.exception(f"Error no manejado en comando {ctx.command}")
        await ctx.reply(
            "❌ Ocurrió un error inesperado. Por favor, inténtalo más tarde.",
            delete_after=10
        )

    async def on_guild_join(self, guild: discord.Guild) -> None:
        """Se ejecuta cuando el bot se une a un servidor"""
        logger.info(f"🎉 Unido al servidor: {guild.name} ({guild.id}) - {guild.member_count} miembros")

    async def on_guild_remove(self, guild: discord.Guild) -> None:
        """Se ejecuta cuando el bot es removido de un servidor"""
        logger.info(f"👋 Removido del servidor: {guild.name} ({guild.id})")

    async def on_member_join(self, member: discord.Member) -> None:
        """Se ejecuta cuando un miembro se une al servidor"""
        if member.guild == self.main_guild:
            logger.info(f"👋 Nuevo miembro en {member.guild.name}: {member.name}")

    async def close(self) -> None:
        """Cierra el bot de forma limpia"""
        logger.info("🔄 Cerrando bot...")
        await super().close()
        logger.info("✅ Bot cerrado correctamente")

    # ====================================
    # MÉTODOS AUXILIARES
    # ====================================

    def get_uptime(self) -> str:
        """Obtiene el tiempo de actividad del bot"""
        if not self.is_ready:
            return "No disponible"

        delta = discord.utils.utcnow() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def is_owner_or_admin(self, user: discord.Member) -> bool:
        """Verifica si el usuario es owner o administrador"""
        if user.id in self.owner_ids:
            return True

        if user.guild_permissions.administrator:
            return True

        # Verificar roles de admin configurados
        admin_roles = self.settings.ADMIN_ROLE_IDS
        return any(role.id in admin_roles for role in user.roles)

    def is_moderator(self, user: discord.Member) -> bool:
        """Verifica si el usuario es moderador"""
        if self.is_owner_or_admin(user):
            return True

        # Verificar roles de moderador configurados
        mod_roles = self.settings.MOD_ROLE_IDS
        return any(role.id in mod_roles for role in user.roles)