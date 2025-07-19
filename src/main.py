#!/usr/bin/env python3
"""
Punto de entrada principal del bot de Discord
Informatica UAIn'T Community Bot

Autor: Raztor
Versión: 1.0.0
"""

import sys
import asyncio
import logging
from pathlib import Path

# Configurar path del proyecto
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src" / "bot"))

# Ahora podemos importar nuestros módulos
from bot import run_bot
from config.settings import get_settings


def print_banner() -> None:
    """Muestra el banner del bot"""

    settings = get_settings()

    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🤖 {settings.BOT_NAME} v{settings.BOT_VERSION}            ║
║    {settings.BOT_DESCRIPTION}                                ║
║                                                              ║
║    📋 Información:                                           ║
║    • Entorno: {settings.ENVIRONMENT.upper()}                 ║
║    • Log Level: {settings.LOG_LEVEL}                         ║
║    • Guild ID: {settings.GUILD_ID or 'No configurado'}       ║
║                                                              ║
║    🚀 Iniciando bot...                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """

    print(banner)


def validate_python_version() -> None:
    """Valida que la versión de Python sea compatible"""

    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        sys.exit(1)


def validate_environment() -> None:
    """Valida el entorno antes de iniciar"""

    try:
        settings = get_settings()
        settings.validate()

    except Exception as e:
        print(f"❌ Error de configuración: {e}")
        print("\n💡 Asegúrate de:")
        print("   1. Copiar .env.example a .env")
        print("   2. Configurar DISCORD_TOKEN en el archivo .env")
        print("   3. Configurar GUILD_ID si quieres funcionalidades específicas del servidor")
        sys.exit(1)


def setup_exception_handler() -> None:
    """Configura el manejador de excepciones global"""

    def handle_exception(exc_type, exc_value, exc_traceback):
        """Maneja excepciones no capturadas"""

        if issubclass(exc_type, KeyboardInterrupt):
            # Manejar Ctrl+C de forma elegante
            print("\n🛑 Bot detenido por el usuario")
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        # Loggear otras excepciones
        logger = logging.getLogger(__name__)
        logger.critical(
            "Excepción no capturada",
            exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = handle_exception


async def main() -> int:
    """Función principal del programa"""

    try:
        # Ejecutar bot
        return await run_bot()

    except KeyboardInterrupt:
        print("\n👋 Bot detenido por el usuario")
        return 0

    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception(f"❌ Error fatal en main: {e}")
        return 1


if __name__ == "__main__":
    # Validaciones previas
    validate_python_version()
    validate_environment()

    # Configurar manejador de excepciones
    setup_exception_handler()

    # Mostrar banner
    print_banner()

    # Ejecutar programa principal
    try:
        exit_code = asyncio.run(main())

        print(f"\n{'=' * 60}")
        print(f"🏁 Bot finalizado con código: {exit_code}")
        print(f"{'=' * 60}")

        sys.exit(exit_code)

    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        sys.exit(1)