"""
Sistema de Canales de Voz Dinámicos
Informatica UAIn'T Community Bot
"""

import logging
import asyncio
import discord
from discord.ext import commands, tasks
from discord import app_commands
from typing import Dict, Set, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DynamicVoiceChannels(commands.Cog, name="Canales Dinámicos"):
    """Sistema de canales de voz dinámicos"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Configuración
        self.trigger_channel_names = ["🔧 Crear Canal", "Crear Canal", "➕ Crear Canal"]
        self.temp_channel_prefix = "💬 Canal de"
        self.cleanup_delay = 10  # segundos para verificar canales vacíos

        # Estado interno
        self.temp_channels: Dict[int, Dict] = {}  # channel_id -> info
        self.trigger_channels: Set[int] = set()  # IDs de canales trigger
        self.user_channels: Dict[int, int] = {}  # user_id -> channel_id que creó

        # Iniciar tarea de limpieza
        self.cleanup_empty_channels.start()

    def cog_unload(self):
        """Limpieza al descargar el cog"""
        self.cleanup_empty_channels.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        """Configurar canales trigger cuando el bot esté listo"""
        await self.setup_trigger_channels()

    async def setup_trigger_channels(self):
        """Identifica y configura los canales trigger existentes"""

        if not self.bot.main_guild:
            return

        trigger_count = 0

        for channel in self.bot.main_guild.voice_channels:
            if any(name.lower() in channel.name.lower() for name in self.trigger_channel_names):
                self.trigger_channels.add(channel.id)
                trigger_count += 1
                logger.info(f"📢 Canal trigger configurado: #{channel.name}")

        logger.info(f"✅ Configurados {trigger_count} canales trigger para canales dinámicos")

    @commands.Cog.listener()
    async def on_voice_state_update(
            self,
            member: discord.Member,
            before: discord.VoiceState,
            after: discord.VoiceState
    ):
        """Maneja cambios en el estado de voz"""

        # Solo procesar en el guild principal
        if member.guild != self.bot.main_guild:
            return

        # Ignorar bots
        if member.bot:
            return

        # Manejar entrada a canal trigger
        if after.channel and after.channel.id in self.trigger_channels:
            await self.handle_trigger_join(member, after.channel)

        # Manejar salida de canales temporales
        if before.channel and before.channel.id in self.temp_channels:
            await self.handle_temp_channel_leave(before.channel)

    async def handle_trigger_join(self, member: discord.Member, trigger_channel: discord.VoiceChannel):
        """Maneja cuando un usuario se une a un canal trigger"""

        try:
            # Verificar si el usuario ya tiene un canal
            if member.id in self.user_channels:
                existing_channel = self.bot.get_channel(self.user_channels[member.id])
                if existing_channel and len(existing_channel.members) == 0:
                    # Si su canal anterior está vacío, usarlo
                    await member.move_to(existing_channel)
                    logger.info(f"👤 {member.name} movido a su canal existente: {existing_channel.name}")
                    return

            # Crear nuevo canal temporal
            temp_channel = await self.create_temp_channel(member, trigger_channel)
            if temp_channel:
                await member.move_to(temp_channel)
                logger.info(f"✅ {member.name} movido a su nuevo canal: {temp_channel.name}")

        except discord.Forbidden:
            logger.error(f"❌ Sin permisos para mover a {member.name}")
        except discord.HTTPException as e:
            logger.error(f"❌ Error moviendo a {member.name}: {e}")
        except Exception as e:
            logger.exception(f"❌ Error inesperado manejando trigger join: {e}")

    async def create_temp_channel(
            self,
            member: discord.Member,
            trigger_channel: discord.VoiceChannel
    ) -> Optional[discord.VoiceChannel]:
        """Crea un canal temporal para el usuario"""

        try:
            # Nombre del canal
            channel_name = f"{self.temp_channel_prefix} {member.display_name}"

            # Configurar permisos
            overwrites = {
                member.guild.default_role: discord.PermissionOverwrite(
                    view_channel=True,
                    connect=True,
                    speak=True
                ),
                member: discord.PermissionOverwrite(
                    view_channel=True,
                    connect=True,
                    speak=True,
                    move_members=True,
                    manage_channels=True,
                    mute_members=True,
                    deafen_members=True
                ),
                self.bot.user: discord.PermissionOverwrite(
                    view_channel=True,
                    connect=True,
                    manage_channels=True,
                    move_members=True
                )
            }

            # Crear canal en la misma categoría
            temp_channel = await trigger_channel.category.create_voice_channel(
                name=channel_name,
                overwrites=overwrites,
                reason=f"Canal dinámico creado para {member.name}"
            )

            # Registrar canal temporal
            self.temp_channels[temp_channel.id] = {
                'owner_id': member.id,
                'created_at': datetime.utcnow(),
                'trigger_channel_id': trigger_channel.id,
                'category_id': trigger_channel.category.id if trigger_channel.category else None
            }

            # Asociar canal con usuario
            self.user_channels[member.id] = temp_channel.id

            logger.info(f"🎉 Canal temporal creado: {temp_channel.name} para {member.name}")
            return temp_channel

        except discord.Forbidden:
            logger.error("❌ Sin permisos para crear canales de voz")
        except discord.HTTPException as e:
            logger.error(f"❌ Error creando canal temporal: {e}")
        except Exception as e:
            logger.exception(f"❌ Error inesperado creando canal: {e}")

        return None

    async def handle_temp_channel_leave(self, channel: discord.VoiceChannel):
        """Maneja cuando alguien deja un canal temporal"""

        # Verificar si el canal está vacío después de un pequeño delay
        await asyncio.sleep(1)  # Dar tiempo para que Discord actualice

        if len(channel.members) == 0:
            await self.schedule_channel_deletion(channel)

    async def schedule_channel_deletion(self, channel: discord.VoiceChannel):
        """Programa la eliminación de un canal vacío"""

        # Esperar un poco más para confirmar que está vacío
        await asyncio.sleep(self.cleanup_delay)

        # Verificar nuevamente si sigue vacío
        fresh_channel = self.bot.get_channel(channel.id)
        if fresh_channel and len(fresh_channel.members) == 0:
            await self.delete_temp_channel(fresh_channel)

    async def delete_temp_channel(self, channel: discord.VoiceChannel):
        """Elimina un canal temporal"""

        try:
            # Obtener información del canal
            channel_info = self.temp_channels.get(channel.id, {})
            owner_id = channel_info.get('owner_id')

            # Eliminar canal
            await channel.delete(reason="Canal dinámico vacío - eliminación automática")

            # Limpiar registros
            if channel.id in self.temp_channels:
                del self.temp_channels[channel.id]

            if owner_id and owner_id in self.user_channels:
                if self.user_channels[owner_id] == channel.id:
                    del self.user_channels[owner_id]

            logger.info(f"🗑️ Canal temporal eliminado: {channel.name}")

        except discord.NotFound:
            # Canal ya fue eliminado
            self.cleanup_channel_records(channel.id)
        except discord.Forbidden:
            logger.error(f"❌ Sin permisos para eliminar canal: {channel.name}")
        except Exception as e:
            logger.exception(f"❌ Error eliminando canal {channel.name}: {e}")

    def cleanup_channel_records(self, channel_id: int):
        """Limpia registros de un canal que ya no existe"""

        if channel_id in self.temp_channels:
            owner_id = self.temp_channels[channel_id].get('owner_id')
            del self.temp_channels[channel_id]

            if owner_id and owner_id in self.user_channels:
                if self.user_channels[owner_id] == channel_id:
                    del self.user_channels[owner_id]

    @tasks.loop(minutes=5)
    async def cleanup_empty_channels(self):
        """Tarea periódica para limpiar canales olvidados"""

        if not self.bot.is_ready:
            return

        channels_to_delete = []

        for channel_id, info in self.temp_channels.items():
            channel = self.bot.get_channel(channel_id)

            if not channel:
                # Canal no existe, limpiar registros
                channels_to_delete.append(channel_id)
                continue

            # Verificar si está vacío por mucho tiempo
            if len(channel.members) == 0:
                created_at = info.get('created_at', datetime.utcnow())
                if datetime.utcnow() - created_at > timedelta(minutes=2):
                    await self.delete_temp_channel(channel)

        # Limpiar registros de canales que no existen
        for channel_id in channels_to_delete:
            self.cleanup_channel_records(channel_id)

    @cleanup_empty_channels.before_loop
    async def before_cleanup(self):
        """Esperar a que el bot esté listo antes de iniciar limpieza"""
        await self.bot.wait_until_ready()

    # ====================================
    # COMANDOS SLASH DE ADMINISTRACIÓN
    # ====================================

    # Grupo principal de comandos
    dynamic_group = app_commands.Group(
        name="canales-dinamicos",
        description="Gestión de canales de voz dinámicos"
    )

    @dynamic_group.command(
        name="estado",
        description="Ver el estado actual del sistema de canales dinámicos"
    )
    @app_commands.default_permissions(manage_channels=True)
    async def estado(self, interaction: discord.Interaction):
        """Muestra el estado del sistema de canales dinámicos"""

        embed = discord.Embed(
            title="🔧 Canales de Voz Dinámicos",
            description="Sistema de canales temporales automáticos",
            color=discord.Color.blue()
        )

        # Información básica
        embed.add_field(
            name="📊 Estado Actual",
            value=f"**Canales trigger:** {len(self.trigger_channels)}\n"
                  f"**Canales temporales activos:** {len(self.temp_channels)}\n"
                  f"**Usuarios con canales:** {len(self.user_channels)}",
            inline=True
        )

        # Información técnica
        embed.add_field(
            name="⚙️ Configuración",
            value=f"**Prefijo:** {self.temp_channel_prefix}\n"
                  f"**Delay de limpieza:** {self.cleanup_delay}s\n"
                  f"**Limpieza automática:** ✅ Activa",
            inline=True
        )

        # Comandos disponibles
        embed.add_field(
            name="📋 Comandos disponibles",
            value="`/canales-dinamicos listar` - Listar canales activos\n"
                  "`/canales-dinamicos reconfigurar` - Reconfigurar triggers\n"
                  "`/canales-dinamicos limpiar` - Limpiar canales vacíos\n"
                  "`/canales-dinamicos eliminar` - Eliminar canal de usuario",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @dynamic_group.command(
        name="listar",
        description="Lista todos los canales dinámicos activos"
    )
    @app_commands.default_permissions(manage_channels=True)
    async def listar(self, interaction: discord.Interaction):
        """Lista todos los canales dinámicos activos"""

        if not self.temp_channels:
            await interaction.response.send_message("📭 No hay canales temporales activos.")
            return

        embed = discord.Embed(
            title="📋 Canales Dinámicos Activos",
            color=discord.Color.green()
        )

        for channel_id, info in self.temp_channels.items():
            channel = self.bot.get_channel(channel_id)
            if channel:
                owner = self.bot.get_user(info['owner_id'])
                created_time = info['created_at'].strftime("%H:%M:%S")

                embed.add_field(
                    name=f"🎙️ {channel.name}",
                    value=f"**Owner:** {owner.mention if owner else 'Usuario desconocido'}\n"
                          f"**Miembros:** {len(channel.members)}\n"
                          f"**Creado:** {created_time}",
                    inline=True
                )

        await interaction.response.send_message(embed=embed)

    @dynamic_group.command(
        name="reconfigurar",
        description="Reconfigura los canales trigger del sistema"
    )
    @app_commands.default_permissions(manage_channels=True)
    async def reconfigurar(self, interaction: discord.Interaction):
        """Reconfigura los canales trigger"""

        self.trigger_channels.clear()
        await self.setup_trigger_channels()

        embed = discord.Embed(
            title="✅ Reconfiguración Completada",
            description=f"Canales trigger encontrados: **{len(self.trigger_channels)}**",
            color=discord.Color.green()
        )

        if self.trigger_channels:
            trigger_list = []
            for channel_id in self.trigger_channels:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    trigger_list.append(f"• {channel.mention}")

            if trigger_list:
                embed.add_field(
                    name="📢 Canales Trigger Configurados",
                    value="\n".join(trigger_list),
                    inline=False
                )

        await interaction.response.send_message(embed=embed)

    @dynamic_group.command(
        name="limpiar",
        description="Ejecuta limpieza manual de canales vacíos"
    )
    @app_commands.default_permissions(manage_channels=True)
    async def limpiar(self, interaction: discord.Interaction):
        """Ejecuta limpieza manual de canales vacíos"""

        await interaction.response.defer()  # El proceso puede tomar tiempo

        cleaned = 0

        for channel_id in list(self.temp_channels.keys()):
            channel = self.bot.get_channel(channel_id)
            if not channel:
                self.cleanup_channel_records(channel_id)
                cleaned += 1
            elif len(channel.members) == 0:
                await self.delete_temp_channel(channel)
                cleaned += 1

        embed = discord.Embed(
            title="🧹 Limpieza Completada",
            description=f"Canales procesados: **{cleaned}**",
            color=discord.Color.green()
        )

        embed.add_field(
            name="📊 Estado Actualizado",
            value=f"**Canales activos restantes:** {len(self.temp_channels)}",
            inline=False
        )

        await interaction.followup.send(embed=embed)

    @dynamic_group.command(
        name="eliminar",
        description="Elimina el canal dinámico de un usuario específico"
    )
    @app_commands.describe(usuario="Usuario cuyo canal dinámico quieres eliminar")
    @app_commands.default_permissions(manage_channels=True)
    async def eliminar(self, interaction: discord.Interaction, usuario: discord.Member):
        """Elimina el canal de un usuario específico"""

        if usuario.id not in self.user_channels:
            embed = discord.Embed(
                title="❌ Canal No Encontrado",
                description=f"{usuario.mention} no tiene un canal dinámico activo.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        channel_id = self.user_channels[usuario.id]
        channel = self.bot.get_channel(channel_id)

        if channel:
            channel_name = channel.name
            await self.delete_temp_channel(channel)

            embed = discord.Embed(
                title="✅ Canal Eliminado",
                description=f"Canal de {usuario.mention} eliminado: **{channel_name}**",
                color=discord.Color.green()
            )
        else:
            self.cleanup_channel_records(channel_id)
            embed = discord.Embed(
                title="✅ Registros Limpiados",
                description=f"Registros de canal de {usuario.mention} limpiados.",
                color=discord.Color.green()
            )

        await interaction.response.send_message(embed=embed)

    @dynamic_group.command(
        name="info",
        description="Información detallada sobre un canal dinámico específico"
    )
    @app_commands.describe(canal="Canal de voz del que quieres ver información")
    @app_commands.default_permissions(manage_channels=True)
    async def info_canal(self, interaction: discord.Interaction, canal: discord.VoiceChannel):
        """Muestra información detallada de un canal específico"""

        if canal.id not in self.temp_channels:
            embed = discord.Embed(
                title="❌ No es un Canal Dinámico",
                description=f"{canal.mention} no es un canal dinámico o no está registrado.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        info = self.temp_channels[canal.id]
        owner = self.bot.get_user(info['owner_id'])
        created_at = info['created_at']

        embed = discord.Embed(
            title=f"🎙️ {canal.name}",
            description="Información del canal dinámico",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="👤 Propietario",
            value=owner.mention if owner else "Usuario desconocido",
            inline=True
        )

        embed.add_field(
            name="👥 Miembros Actuales",
            value=f"**{len(canal.members)}** conectados",
            inline=True
        )

        embed.add_field(
            name="⏰ Tiempo Activo",
            value=f"<t:{int(created_at.timestamp())}:R>",
            inline=True
        )

        embed.add_field(
            name="📊 Detalles Técnicos",
            value=f"**ID Canal:** {canal.id}\n"
                  f"**ID Owner:** {info['owner_id']}\n"
                  f"**Categoría:** {canal.category.name if canal.category else 'Sin categoría'}",
            inline=False
        )

        if canal.members:
            members_list = [member.mention for member in canal.members[:10]]  # Máximo 10 para no saturar
            members_text = "\n".join(members_list)
            if len(canal.members) > 10:
                members_text += f"\n... y {len(canal.members) - 10} más"

            embed.add_field(
                name="🎧 Miembros Conectados",
                value=members_text,
                inline=False
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Función para cargar el cog"""
    await bot.add_cog(DynamicVoiceChannels(bot))
    logger.info("✅ Sistema de canales dinámicos cargado")