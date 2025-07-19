"""
Eventos globales del bot
Informatica UAIn'T Community Bot
"""

import logging
import discord
from discord.ext import commands
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import UaintBot

logger = logging.getLogger(__name__)


class BotEvents(commands.Cog):
    """Cog para manejar eventos globales del bot"""

    def __init__(self, bot: "UaintBot"):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Se ejecuta cuando se envía un mensaje"""

        # Ignorar mensajes del bot
        if message.author.bot:
            return

        # Log de mensajes en el guild principal (solo en desarrollo)
        if (self.bot.settings.IS_DEVELOPMENT and
                message.guild == self.bot.main_guild):
            logger.debug(
                f"Mensaje en #{message.channel.name}: "
                f"{message.author.name}: {message.content[:50]}..."
            )

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        """Se ejecuta cuando se edita un mensaje"""

        # Ignorar mensajes del bot
        if before.author.bot:
            return

        # Re-procesar comandos si el mensaje editado ahora es un comando
        if before.content != after.content:
            await self.bot.process_commands(after)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        """Se ejecuta cuando se elimina un mensaje"""

        # Solo loggear en el guild principal
        if message.guild != self.bot.main_guild:
            return

        # Ignorar mensajes del bot
        if message.author.bot:
            return

        # Log básico (en el futuro esto irá a un sistema de moderación)
        if len(message.content) > 0:
            logger.info(
                f"Mensaje eliminado en #{message.channel.name} por {message.author.name}: "
                f"{message.content[:100]}..."
            )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """Se ejecuta cuando un miembro se une al servidor"""

        # Solo procesar el guild principal
        if member.guild != self.bot.main_guild:
            return

        logger.info(f"👋 {member.name} se unió a {member.guild.name}")

        # TODO: En futuras fases aquí se implementará:
        # - Mensaje de bienvenida
        # - Asignación de roles automáticos
        # - Log en canal de moderación

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        """Se ejecuta cuando un miembro deja el servidor"""

        # Solo procesar el guild principal
        if member.guild != self.bot.main_guild:
            return

        logger.info(f"👋 {member.name} dejó {member.guild.name}")

        # TODO: En futuras fases aquí se implementará:
        # - Mensaje de despedida
        # - Log en canal de moderación

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel) -> None:
        """Se ejecuta cuando se crea un canal"""
        if channel.guild == self.bot.main_guild:
            logger.info(f"📝 Canal creado: #{channel.name} en {channel.guild.name}")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel) -> None:
        """Se ejecuta cuando se elimina un canal"""
        if channel.guild == self.bot.main_guild:
            logger.info(f"🗑️ Canal eliminado: #{channel.name} en {channel.guild.name}")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role) -> None:
        """Se ejecuta cuando se crea un rol"""
        if role.guild == self.bot.main_guild:
            logger.info(f"🎭 Rol creado: @{role.name} en {role.guild.name}")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role) -> None:
        """Se ejecuta cuando se elimina un rol"""
        if role.guild == self.bot.main_guild:
            logger.info(f"🗑️ Rol eliminado: @{role.name} en {role.guild.name}")

    @commands.Cog.listener()
    async def on_voice_state_update(
            self,
            member: discord.Member,
            before: discord.VoiceState,
            after: discord.VoiceState
    ) -> None:
        """Se ejecuta cuando cambia el estado de voz de un miembro"""

        # Solo procesar el guild principal
        if member.guild != self.bot.main_guild:
            return

        # Entró a un canal de voz
        if before.channel is None and after.channel is not None:
            logger.debug(f"🔊 {member.name} se conectó a {after.channel.name}")

        # Salió de un canal de voz
        elif before.channel is not None and after.channel is None:
            logger.debug(f"🔇 {member.name} se desconectó de {before.channel.name}")

        # Cambió de canal
        elif before.channel != after.channel and after.channel is not None:
            logger.debug(f"🔄 {member.name} se movió de {before.channel.name} a {after.channel.name}")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User) -> None:
        """Se ejecuta cuando se agrega una reacción"""

        # Ignorar reacciones del bot
        if user.bot:
            return

        # Solo procesar en el guild principal
        if not reaction.message.guild or reaction.message.guild != self.bot.main_guild:
            return

        # TODO: En futuras fases aquí se implementará:
        # - Sistema de roles por reacciones
        # - Votaciones
        # - Sistemas de aprobación

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User) -> None:
        """Se ejecuta cuando se quita una reacción"""

        # Ignorar reacciones del bot
        if user.bot:
            return

        # Solo procesar en el guild principal
        if not reaction.message.guild or reaction.message.guild != self.bot.main_guild:
            return

        # TODO: Complemento del sistema de roles por reacciones

    @commands.Cog.listener()
    async def on_slash_command_error(self, interaction: discord.Interaction, error: Exception) -> None:
        """Maneja errores de comandos slash"""

        logger.exception(f"Error en comando slash: {error}")

        # Responder al usuario si la interacción aún no ha sido respondida
        if not interaction.response.is_done():
            await interaction.response.send_message(
                "❌ Ocurrió un error al ejecutar el comando. Por favor, inténtalo más tarde.",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                "❌ Ocurrió un error inesperado.",
                ephemeral=True
            )


async def setup(bot: "UaintBot") -> None:
    """Función para cargar el cog"""
    await bot.add_cog(BotEvents(bot))