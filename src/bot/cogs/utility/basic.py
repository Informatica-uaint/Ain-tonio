"""
Comandos básicos y de utilidad
Informatica UAIn'T Community Bot
"""

import logging
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

logger = logging.getLogger(__name__)


class BasicCommands(commands.Cog, name="Utilidad"):
    """Comandos básicos y de utilidad"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="latencia", description="Verifica la latencia del bot")
    async def latencia(self, interaction: discord.Interaction) -> None:
        """Comando slash para verificar la latencia del bot"""

        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latencia: **{latency}ms**",
            color=discord.Color.green() if latency < 100 else
            discord.Color.yellow() if latency < 200 else
            discord.Color.red()
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="info", description="Información del bot")
    async def info(self, interaction: discord.Interaction) -> None:
        """Muestra información del bot"""

        embed = discord.Embed(
            title=f"🤖 {self.bot.settings.BOT_NAME}",
            description=self.bot.settings.BOT_DESCRIPTION,
            color=discord.Color.blue()
        )

        # Información básica
        embed.add_field(
            name="📊 Estadísticas",
            value=f"**Servidores:** {len(self.bot.guilds)}\n"
                  f"**Usuarios:** {len(self.bot.users)}\n"
                  f"**Latencia:** {round(self.bot.latency * 1000)}ms",
            inline=True
        )

        # Información técnica
        embed.add_field(
            name="⚙️ Información",
            value=f"**Versión:** {self.bot.settings.BOT_VERSION}\n"
                  f"**Tiempo activo:** {self.bot.get_uptime()}\n"
                  f"**Discord.py:** {discord.__version__}",
            inline=True
        )

        # Autor
        embed.add_field(
            name="👨‍💻 Desarrollado por",
            value=self.bot.settings.BOT_AUTHOR,
            inline=False
        )

        # Avatar del bot
        if self.bot.user and self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        embed.set_footer(text=f"Bot ID: {self.bot.user.id}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="servidor", description="Información del servidor")
    async def servidor(self, interaction: discord.Interaction) -> None:
        """Muestra información del servidor actual"""

        if not interaction.guild:
            await interaction.response.send_message(
                "❌ Este comando solo funciona en servidores.",
                ephemeral=True
            )
            return

        guild = interaction.guild

        embed = discord.Embed(
            title=f"🏠 {guild.name}",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )

        # Información básica
        embed.add_field(
            name="📊 Estadísticas",
            value=f"**Miembros:** {guild.member_count}\n"
                  f"**Canales:** {len(guild.channels)}\n"
                  f"**Roles:** {len(guild.roles)}",
            inline=True
        )

        # Información del servidor
        embed.add_field(
            name="ℹ️ Información",
            value=f"**Creado:** <t:{int(guild.created_at.timestamp())}:D>\n"
                  f"**Owner:** {guild.owner.mention if guild.owner else 'Desconocido'}\n"
                  f"**Nivel de verificación:** {guild.verification_level.name.title()}",
            inline=True
        )

        # Contadores detallados
        text_channels = len([c for c in guild.channels if isinstance(c, discord.TextChannel)])
        voice_channels = len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)])
        categories = len([c for c in guild.channels if isinstance(c, discord.CategoryChannel)])

        embed.add_field(
            name="📁 Canales",
            value=f"**Texto:** {text_channels}\n"
                  f"**Voz:** {voice_channels}\n"
                  f"**Categorías:** {categories}",
            inline=True
        )

        # Icon del servidor
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.set_footer(text=f"ID: {guild.id}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="usuario", description="Información de un usuario")
    @app_commands.describe(usuario="Usuario del que quieres ver la información")
    async def usuario(
            self,
            interaction: discord.Interaction,
            usuario: Optional[discord.Member] = None
    ) -> None:
        """Muestra información de un usuario"""

        # Si no se especifica usuario, usar el que ejecuta el comando
        target = usuario or interaction.user

        if not isinstance(target, discord.Member):
            await interaction.response.send_message(
                "❌ Este comando solo funciona en servidores.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=f"👤 {target.display_name}",
            color=target.color if target.color != discord.Color.default() else discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )

        # Información básica
        embed.add_field(
            name="ℹ️ Información",
            value=f"**Nombre:** {target.name}\n"
                  f"**Tag:** {target.discriminator}\n"
                  f"**ID:** {target.id}",
            inline=True
        )

        # Fechas importantes
        embed.add_field(
            name="📅 Fechas",
            value=f"**Cuenta creada:** <t:{int(target.created_at.timestamp())}:D>\n"
                  f"**Se unió:** <t:{int(target.joined_at.timestamp())}:D>",
            inline=True
        )

        # Estado y actividad
        status_emoji = {
            discord.Status.online: "🟢",
            discord.Status.idle: "🟡",
            discord.Status.dnd: "🔴",
            discord.Status.offline: "⚫"
        }

        embed.add_field(
            name="🎭 Estado",
            value=f"**Estado:** {status_emoji.get(target.status, '❓')} {target.status.name.title()}\n"
                  f"**Roles:** {len(target.roles) - 1}\n"  # -1 para excluir @everyone
                  f"**Permisos:** {'👑 Admin' if target.guild_permissions.administrator else '👤 Miembro'}",
            inline=True
        )

        # Avatar
        if target.avatar:
            embed.set_thumbnail(url=target.avatar.url)

        # Rol más alto (con color)
        if len(target.roles) > 1:  # Más que solo @everyone
            highest_role = target.roles[-1]  # El último rol es el más alto
            embed.set_footer(text=f"Rol más alto: @{highest_role.name}")

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Función para cargar el cog"""
    await bot.add_cog(BasicCommands(bot))
    logger.info("✅ Comandos básicos cargados")