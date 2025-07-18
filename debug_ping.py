#!/usr/bin/env python3
"""
Debug específico del error en comando ping
"""

import sys
from pathlib import Path

# Configurar path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src" / "bot"))

print("🔍 Debugging error de comando ping...")
print("=" * 50)

# Verificar bot y settings
try:
    from core.client import UaintBot

    print("✅ UaintBot importado")

    bot = UaintBot()
    print(f"✅ Bot creado: {bot}")
    print(f"✅ Bot tiene settings: {hasattr(bot, 'settings')}")

    if hasattr(bot, 'settings'):
        print(f"✅ Settings: {bot.settings}")
        print(f"✅ BOT_NAME: {getattr(bot.settings, 'BOT_NAME', 'NO ENCONTRADO')}")
        print(f"✅ BOT_VERSION: {getattr(bot.settings, 'BOT_VERSION', 'NO ENCONTRADO')}")
    else:
        print("❌ Bot NO tiene atributo settings")

except Exception as e:
    print(f"❌ Error creando bot: {e}")
    import traceback

    traceback.print_exc()

# Verificar cog
try:
    from cogs.utility.basic import BasicCommands

    print("\n✅ BasicCommands importado")

    # Crear cog con bot
    if 'bot' in locals():
        cog = BasicCommands(bot)
        print(f"✅ Cog creado: {cog}")
        print(f"✅ Cog.bot: {cog.bot}")
        print(f"✅ Cog.bot tiene settings: {hasattr(cog.bot, 'settings')}")

        if hasattr(cog.bot, 'settings'):
            print(f"✅ Cog.bot.settings: {cog.bot.settings}")

        # Simular acceso a latencia
        print(f"✅ Bot latency: {bot.latency}")
        print(f"✅ Latency en ms: {round(bot.latency * 1000)}")

except Exception as e:
    print(f"❌ Error con cog: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 50)
print("🏁 Debugging completado")