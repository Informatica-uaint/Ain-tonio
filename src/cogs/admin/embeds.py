"""
Sistema de Embeds Administrativos
Informatica UAIn'T Community Bot
"""

import logging
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional, Dict, Any, Literal
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class AdminEmbeds(commands.Cog, name="Admin Embeds"):
    """Sistema de embeds administrativos para anuncios y comunicados"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Plantillas predefinidas
        self.templates = {
            "anuncio": {
                "color": discord.Color.blue(),
                "emoji": "📢",
                "footer": "Anuncio oficial del servidor"
            },
            "reglas": {
                "color": discord.Color.red(),
                "emoji": "📋",
                "footer": "Reglas del servidor - Cumplimiento obligatorio"
            },
            "informacion": {
                "color": discord.Color.green(),
                "emoji": "ℹ️",
                "footer": "Información del servidor"
            },
            "aviso": {
                "color": discord.Color.orange(),
                "emoji": "⚠️",
                "footer": "Aviso importante"
            },
            "evento": {
                "color": discord.Color.purple(),
                "emoji": "🎉",
                "footer": "Evento del servidor"
            },
            "bienvenida": {
                "color": discord.Color.gold(),
                "emoji": "👋",
                "footer": "¡Te damos la bienvenida!"
            }
        }

        # Colores predefinidos
        self.colors = {
            "rojo": discord.Color.red(),
            "verde": discord.Color.green(),
            "azul": discord.Color.blue(),
            "naranja": discord.Color.orange(),
            "morado": discord.Color.purple(),
            "rosa": discord.Color.magenta(),
            "dorado": discord.Color.gold(),
            "gris": discord.Color.light_grey(),
            "gris_oscuro": discord.Color.dark_grey(),
            "amarillo": discord.Color.from_rgb(255, 255, 0),
            "cyan": discord.Color.from_rgb(0, 255, 255),
            "negro": discord.Color.from_rgb(0, 0, 0),
            "blanco": discord.Color.from_rgb(255, 255, 255)
        }

    async def check_admin_permissions(self, interaction: discord.Interaction) -> bool:
        """Verifica si el usuario tiene permisos de administrador"""

        # Verificar que sea en un servidor
        if not interaction.guild:
            await interaction.response.send_message(
                "❌ Este comando solo puede usarse en servidores.",
                ephemeral=True
            )
            return False

        # Verificar que sea un miembro
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(
                "❌ Error: No se pudo verificar tus permisos.",
                ephemeral=True
            )
            return False

        member = interaction.user

        # Owner del bot siempre puede
        if await self.bot.is_owner(member):
            return True

        # Administradores del servidor pueden
        if member.guild_permissions.administrator:
            return True

        # Verificar si tiene permiso de gestionar mensajes
        if member.guild_permissions.manage_messages:
            return True

        # Verificar roles de admin configurados
        admin_roles = self.bot.settings.ADMIN_ROLE_IDS
        if admin_roles and any(role.id in admin_roles for role in member.roles):
            return True

        # Verificar roles de moderador configurados
        mod_roles = self.bot.settings.MOD_ROLE_IDS
        if mod_roles and any(role.id in mod_roles for role in member.roles):
            return True

        # Si no tiene permisos, enviar mensaje de error
        await interaction.response.send_message(
            "❌ **Sin permisos suficientes**\n\n"
            "Necesitas uno de los siguientes permisos:\n"
            "• **Administrador** del servidor\n"
            "• **Gestionar Mensajes** de Discord\n"
            "• Rol de **Admin/Moderador** configurado en el bot",
            ephemeral=True
        )
        return False

    def parse_color(self, color_input: str) -> discord.Color:
        """Convierte input de color a objeto Color de Discord"""

        # Limpiar input
        color_input = color_input.lower().strip()

        # Verificar si es un color predefinido
        if color_input in self.colors:
            return self.colors[color_input]

        # Verificar si es hex válido
        hex_pattern = re.compile(r'^#?([A-Fa-f0-9]{6})$')
        match = hex_pattern.match(color_input)
        if match:
            hex_code = match.group(1)
            return discord.Color(int(hex_code, 16))

        # Color por defecto si no se reconoce
        return discord.Color.blue()

    def create_embed(
            self,
            title: str,
            description: str,
            color: discord.Color = discord.Color.blue(),
            footer: Optional[str] = None,
            thumbnail_url: Optional[str] = None,
            timestamp: bool = True,
            author_name: Optional[str] = None,
            fields: Optional[list] = None
    ) -> discord.Embed:
        """Crea un embed con los parámetros especificados"""

        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

        if timestamp:
            embed.timestamp = discord.utils.utcnow()

        if footer:
            embed.set_footer(text=footer)

        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)

        if author_name:
            embed.set_author(name=author_name)

        if fields:
            for field in fields:
                embed.add_field(
                    name=field.get("name", "Campo"),
                    value=field.get("value", "Valor"),
                    inline=field.get("inline", False)
                )

        return embed

    async def log_embed_action(
            self,
            interaction: discord.Interaction,
            embed_title: str,
            target_channel: discord.TextChannel,
            command_type: str
    ):
        """Registra el envío de embeds en los logs"""

        logger.info(
            f"📨 Embed enviado por {interaction.user.name} ({interaction.user.id}) "
            f"en #{target_channel.name}: '{embed_title}' (Tipo: {command_type})"
        )

    # ====================================
    # GRUPO DE COMANDOS ADMINISTRATIVOS
    # ====================================

    admin_group = app_commands.Group(
        name="admin",
        description="Comandos administrativos del servidor",
        default_permissions=discord.Permissions(manage_messages=True)
    )

    @admin_group.command(
        name="embed-simple",
        description="Envía un embed básico con título y descripción"
    )
    @app_commands.describe(
        titulo="Título del embed",
        descripcion="Contenido principal del embed",
        canal="Canal donde enviar el embed (opcional, por defecto el actual)"
    )
    async def embed_simple(
            self,
            interaction: discord.Interaction,
            titulo: str,
            descripcion: str,
            canal: Optional[discord.TextChannel] = None
    ):
        """Comando para enviar embeds simples"""

        # Verificar permisos
        if not await self.check_admin_permissions(interaction):
            return

        # Canal de destino
        target_channel = canal or interaction.channel

        # Verificar permisos del bot en el canal de destino
        if not target_channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.response.send_message(
                f"❌ No tengo permisos para enviar mensajes en {target_channel.mention}",
                ephemeral=True
            )
            return

        # Crear embed básico
        embed = self.create_embed(
            title=titulo,
            description=descripcion,
            color=discord.Color.blue(),
            footer=f"Enviado por {interaction.user.display_name}",
            thumbnail_url=interaction.guild.icon.url if interaction.guild.icon else None
        )

        try:
            # Enviar embed
            await target_channel.send(embed=embed)

            # Confirmar envío
            confirm_embed = discord.Embed(
                title="✅ Embed Enviado",
                description=f"Embed enviado exitosamente en {target_channel.mention}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=confirm_embed, ephemeral=True)

            # Log de la acción
            await self.log_embed_action(interaction, titulo, target_channel, "simple")

        except discord.Forbidden:
            await interaction.response.send_message(
                f"❌ No tengo permisos para enviar embeds en {target_channel.mention}",
                ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error enviando embed simple: {e}")
            await interaction.response.send_message(
                "❌ Error inesperado al enviar el embed.",
                ephemeral=True
            )

    @admin_group.command(
        name="embed-avanzado",
        description="Envía un embed completamente personalizable"
    )
    @app_commands.describe(
        titulo="Título del embed",
        descripcion="Contenido principal del embed",
        color="Color del embed (nombre o código hex)",
        footer="Texto del footer (opcional)",
        canal="Canal donde enviar el embed (opcional)",
        autor="Nombre del autor del embed (opcional)",
        thumbnail="Mostrar thumbnail del servidor"
    )
    async def embed_avanzado(
            self,
            interaction: discord.Interaction,
            titulo: str,
            descripcion: str,
            color: str = "azul",
            footer: Optional[str] = None,
            canal: Optional[discord.TextChannel] = None,
            autor: Optional[str] = None,
            thumbnail: bool = True
    ):
        """Comando para enviar embeds avanzados con todas las opciones"""

        # Verificar permisos
        if not await self.check_admin_permissions(interaction):
            return

        # Canal de destino
        target_channel = canal or interaction.channel

        # Verificar permisos del bot
        if not target_channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.response.send_message(
                f"❌ No tengo permisos para enviar mensajes en {target_channel.mention}",
                ephemeral=True
            )
            return

        # Procesar color
        embed_color = self.parse_color(color)

        # Footer por defecto
        if not footer:
            footer = f"Enviado por {interaction.user.display_name}"

        # Thumbnail
        thumbnail_url = None
        if thumbnail and interaction.guild.icon:
            thumbnail_url = interaction.guild.icon.url

        # Crear embed avanzado
        embed = self.create_embed(
            title=titulo,
            description=descripcion,
            color=embed_color,
            footer=footer,
            thumbnail_url=thumbnail_url,
            author_name=autor
        )

        try:
            # Enviar embed
            await target_channel.send(embed=embed)

            # Confirmar envío con detalles
            confirm_embed = discord.Embed(
                title="✅ Embed Avanzado Enviado",
                color=discord.Color.green()
            )
            confirm_embed.add_field(
                name="📍 Destino",
                value=target_channel.mention,
                inline=True
            )
            confirm_embed.add_field(
                name="🎨 Color",
                value=color,
                inline=True
            )
            confirm_embed.add_field(
                name="📝 Título",
                value=titulo[:50] + "..." if len(titulo) > 50 else titulo,
                inline=False
            )

            await interaction.response.send_message(embed=confirm_embed, ephemeral=True)

            # Log de la acción
            await self.log_embed_action(interaction, titulo, target_channel, "avanzado")

        except discord.Forbidden:
            await interaction.response.send_message(
                f"❌ No tengo permisos para enviar embeds en {target_channel.mention}",
                ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error enviando embed avanzado: {e}")
            await interaction.response.send_message(
                "❌ Error inesperado al enviar el embed.",
                ephemeral=True
            )

    @admin_group.command(
        name="embed-plantilla",
        description="Envía un embed usando una plantilla predefinida"
    )
    @app_commands.describe(
        tipo="Tipo de plantilla a usar",
        titulo="Título del embed",
        contenido="Contenido principal del embed",
        canal="Canal donde enviar el embed (opcional)"
    )
    async def embed_plantilla(
            self,
            interaction: discord.Interaction,
            tipo: Literal["anuncio", "reglas", "informacion", "aviso", "evento", "bienvenida"],
            titulo: str,
            contenido: str,
            canal: Optional[discord.TextChannel] = None
    ):
        """Comando para enviar embeds usando plantillas predefinidas"""

        # Verificar permisos
        if not await self.check_admin_permissions(interaction):
            return

        # Canal de destino
        target_channel = canal or interaction.channel

        # Verificar permisos del bot
        if not target_channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.response.send_message(
                f"❌ No tengo permisos para enviar mensajes en {target_channel.mention}",
                ephemeral=True
            )
            return

        # Obtener plantilla
        template = self.templates[tipo]

        # Crear título con emoji
        full_title = f"{template['emoji']} {titulo}"

        # Crear embed con plantilla
        embed = self.create_embed(
            title=full_title,
            description=contenido,
            color=template["color"],
            footer=template["footer"],
            thumbnail_url=interaction.guild.icon.url if interaction.guild.icon else None
        )

        try:
            # Enviar embed
            await target_channel.send(embed=embed)

            # Confirmar envío con info de plantilla
            confirm_embed = discord.Embed(
                title="✅ Embed con Plantilla Enviado",
                color=discord.Color.green()
            )
            confirm_embed.add_field(
                name="📋 Plantilla",
                value=f"{template['emoji']} {tipo.title()}",
                inline=True
            )
            confirm_embed.add_field(
                name="📍 Destino",
                value=target_channel.mention,
                inline=True
            )
            confirm_embed.add_field(
                name="📝 Título",
                value=titulo[:50] + "..." if len(titulo) > 50 else titulo,
                inline=False
            )

            await interaction.response.send_message(embed=confirm_embed, ephemeral=True)

            # Log de la acción
            await self.log_embed_action(interaction, titulo, target_channel, f"plantilla-{tipo}")

        except discord.Forbidden:
            await interaction.response.send_message(
                f"❌ No tengo permisos para enviar embeds en {target_channel.mention}",
                ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error enviando embed con plantilla: {e}")
            await interaction.response.send_message(
                "❌ Error inesperado al enviar el embed.",
                ephemeral=True
            )

    @admin_group.command(
        name="embed-preview",
        description="Muestra una vista previa del embed sin enviarlo"
    )
    @app_commands.describe(
        titulo="Título del embed",
        descripcion="Contenido del embed",
        color="Color del embed (opcional)",
        tipo_plantilla="Usar plantilla predefinida (opcional)"
    )
    async def embed_preview(
            self,
            interaction: discord.Interaction,
            titulo: str,
            descripcion: str,
            color: Optional[str] = None,
            tipo_plantilla: Optional[
                Literal["anuncio", "reglas", "informacion", "aviso", "evento", "bienvenida"]] = None
    ):
        """Comando para previsualizar embeds antes de enviarlos"""

        # Verificar permisos
        if not await self.check_admin_permissions(interaction):
            return

        # Determinar configuración del embed
        if tipo_plantilla:
            template = self.templates[tipo_plantilla]
            embed_color = template["color"]
            full_title = f"{template['emoji']} {titulo}"
            footer_text = template["footer"]
        else:
            embed_color = self.parse_color(color) if color else discord.Color.blue()
            full_title = titulo
            footer_text = f"Vista previa - por {interaction.user.display_name}"

        # Crear embed de preview
        preview_embed = self.create_embed(
            title=full_title,
            description=descripcion,
            color=embed_color,
            footer=footer_text,
            thumbnail_url=interaction.guild.icon.url if interaction.guild.icon else None
        )

        # Embed de información sobre el preview
        info_embed = discord.Embed(
            title="👁️ Vista Previa del Embed",
            description="Así se vería tu embed. Usa los otros comandos para enviarlo realmente.",
            color=discord.Color.yellow()
        )

        if tipo_plantilla:
            info_embed.add_field(
                name="📋 Plantilla",
                value=f"{self.templates[tipo_plantilla]['emoji']} {tipo_plantilla.title()}",
                inline=True
            )

        if color:
            info_embed.add_field(
                name="🎨 Color",
                value=color,
                inline=True
            )

        await interaction.response.send_message(
            embeds=[info_embed, preview_embed],
            ephemeral=True
        )

    @admin_group.command(
        name="embed-ayuda",
        description="Guía completa para usar los comandos de embeds"
    )
    async def embed_ayuda(self, interaction: discord.Interaction):
        """Comando de ayuda para el sistema de embeds"""

        # Verificar permisos
        if not await self.check_admin_permissions(interaction):
            return

        # Embed principal de ayuda
        help_embed = discord.Embed(
            title="📚 Guía de Comandos de Embeds",
            description="Sistema completo para enviar mensajes oficiales del servidor",
            color=discord.Color.blue()
        )

        # Comandos disponibles
        help_embed.add_field(
            name="📝 Comandos Disponibles",
            value="`/admin embed-simple` - Embed básico\n"
                  "`/admin embed-avanzado` - Embed personalizable\n"
                  "`/admin embed-plantilla` - Usando plantillas\n"
                  "`/admin embed-preview` - Vista previa\n"
                  "`/admin embed-ayuda` - Esta ayuda",
            inline=False
        )

        # Plantillas disponibles
        templates_text = ""
        for name, template in self.templates.items():
            templates_text += f"{template['emoji']} **{name.title()}** - {template['footer']}\n"

        help_embed.add_field(
            name="📋 Plantillas Disponibles",
            value=templates_text,
            inline=False
        )

        # Colores disponibles
        colors_text = ", ".join([f"`{name}`" for name in list(self.colors.keys())[:10]])
        colors_text += "\n💡 También puedes usar códigos hex: `#ff0000`"

        help_embed.add_field(
            name="🎨 Colores Disponibles",
            value=colors_text,
            inline=False
        )

        # Ejemplos
        help_embed.add_field(
            name="💡 Ejemplos de Uso",
            value="`/admin embed-simple titulo:\"Mantenimiento\" descripcion:\"El servidor estará en mantenimiento\"`\n\n"
                  "`/admin embed-plantilla tipo:anuncio titulo:\"Nuevo evento\" contenido:\"Inscripciones abiertas\"`\n\n"
                  "`/admin embed-avanzado titulo:\"Reglas\" descripcion:\"Normas del servidor\" color:rojo`",
            inline=False
        )

        help_embed.set_footer(text="Solo administradores y moderadores pueden usar estos comandos")

        await interaction.response.send_message(embed=help_embed, ephemeral=True)

    @admin_group.command(
        name="plantillas-info",
        description="Ver información detallada de todas las plantillas disponibles"
    )
    async def plantillas_info(self, interaction: discord.Interaction):
        """Muestra información detallada sobre las plantillas"""

        # Verificar permisos
        if not await self.check_admin_permissions(interaction):
            return

        embeds = []

        # Embed principal
        main_embed = discord.Embed(
            title="📋 Plantillas de Embeds Disponibles",
            description="Plantillas prediseñadas para diferentes tipos de mensajes",
            color=discord.Color.blue()
        )
        main_embed.set_footer(text="Usa /admin embed-plantilla tipo:[nombre] para usar una plantilla")
        embeds.append(main_embed)

        # Crear un embed de ejemplo para cada plantilla
        for name, template in self.templates.items():
            example_embed = self.create_embed(
                title=f"{template['emoji']} Ejemplo de {name.title()}",
                description=f"Este es un ejemplo de cómo se ve la plantilla '{name}'. "
                            f"Úsala para {name.replace('_', ' ')} del servidor.",
                color=template["color"],
                footer=template["footer"]
            )
            embeds.append(example_embed)

        await interaction.response.send_message(embeds=embeds[:10], ephemeral=True)  # Discord limit


async def setup(bot: commands.Bot) -> None:
    """Función para cargar el cog"""
    await bot.add_cog(AdminEmbeds(bot))
    logger.info("✅ Sistema de embeds administrativos cargado")