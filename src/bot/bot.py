"""
Cliente principal del bot
Informatica UAIn'T Community Bot
"""

import logging
import asyncio
from pathlib import Path
from typing import List

from core.client import UaintBot
from core.exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class BotManager:
    """Gestor principal del bot"""

    def __init__(self):
        self.bot: UaintBot = UaintBot()
        self.extensions_loaded: List[str] = []

    async def load_extensions(self) -> None:
        """Carga todas las extensiones (cogs) del bot"""

        # Extensiones principales
        core_extensions = [
            "core.events",  # Eventos globales
        ]

        # Cogs básicos
        basic_cogs = [
            "cogs.utility.basic",  # Comandos básicos
            "cogs.utility.dynamic_voice",  # Canales dinámicos
            "cogs.admin.embeds",  # Sistema de embeds administrativos
        ]

        # Todas las extensiones a cargar
        all_extensions = core_extensions + basic_cogs

        logger.info(f"Cargando {len(all_extensions)} extensiones...")

        for extension in all_extensions:
            try:
                await self.bot.load_extension(extension)
                self.extensions_loaded.append(extension)
                logger.info(f"✅ Cargada extensión: {extension}")

            except Exception as e:
                logger.error(f"❌ Error cargando extensión {extension}: {e}")
                # En desarrollo, podemos continuar sin algunas extensiones
                if not self.bot.settings.IS_DEVELOPMENT:
                    raise

        logger.info(f"🎉 Cargadas {len(self.extensions_loaded)} extensiones correctamente")

    async def unload_extensions(self) -> None:
        """Descarga todas las extensiones"""

        logger.info("Descargando extensiones...")

        for extension in self.extensions_loaded[:]:  # Copia para evitar modificar durante iteración
            try:
                await self.bot.unload_extension(extension)
                self.extensions_loaded.remove(extension)
                logger.info(f"✅ Descargada extensión: {extension}")

            except Exception as e:
                logger.error(f"❌ Error descargando extensión {extension}: {e}")

    async def reload_extension(self, extension: str) -> bool:
        """Recarga una extensión específica"""

        try:
            await self.bot.reload_extension(extension)
            logger.info(f"🔄 Recargada extensión: {extension}")
            return True

        except Exception as e:
            logger.error(f"❌ Error recargando extensión {extension}: {e}")
            return False

    async def start(self) -> None:
        """Inicia el bot"""

        try:
            # Cargar extensiones
            await self.load_extensions()

            # Iniciar bot (la sincronización se hará en on_ready)
            logger.info("🚀 Iniciando bot...")
            await self.bot.start(self.bot.settings.DISCORD_TOKEN)

        except ConfigurationError as e:
            logger.error(f"❌ Error de configuración: {e}")
            raise

        except Exception as e:
            logger.exception(f"❌ Error iniciando bot: {e}")
            raise

        finally:
            # Cleanup
            await self.cleanup()

    async def cleanup(self) -> None:
        """Limpieza al cerrar el bot"""

        logger.info("🧹 Realizando limpieza...")

        try:
            # Descargar extensiones
            await self.unload_extensions()

            # Cerrar bot si no está cerrado
            if not self.bot.is_closed():
                await self.bot.close()

        except Exception as e:
            logger.error(f"Error durante limpieza: {e}")

        logger.info("✅ Limpieza completada")

    async def stop(self) -> None:
        """Detiene el bot de forma segura"""

        logger.info("🛑 Deteniendo bot...")
        await self.bot.close()


# ====================================
# FUNCIONES DE UTILIDAD
# ====================================

def setup_project_path() -> None:
    """Configura el path del proyecto para imports"""
    import sys

    # Obtener directorio del proyecto (2 niveles arriba de este archivo)
    project_root = Path(__file__).parent.parent.parent
    src_path = project_root / "src" / "bot"

    # Agregar al path si no está
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


async def run_bot() -> None:
    """Función principal para ejecutar el bot"""

    # Configurar path del proyecto
    setup_project_path()

    # Crear gestor del bot
    bot_manager = BotManager()

    try:
        # Iniciar bot
        await bot_manager.start()

    except KeyboardInterrupt:
        logger.info("🛑 Interrupción por teclado recibida")

    except Exception as e:
        logger.exception(f"❌ Error fatal: {e}")
        return 1

    return 0


if __name__ == "__main__":
    # Ejecutar bot si se llama directamente
    import sys

    try:
        exit_code = asyncio.run(run_bot())
        sys.exit(exit_code)

    except KeyboardInterrupt:
        logger.info("👋 Bot detenido por el usuario")
        sys.exit(0)