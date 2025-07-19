# src/bot/__init__.py
"""
Bot de Discord para la comunidad de Informática UAIn'T
"""

__version__ = "1.0.0"
__author__ = "Raztor"

# src/bot/core/__init__.py
"""
Núcleo del bot - Funcionalidades centrales
"""

from .client import UaintBot
from .exceptions import BotException, ConfigurationError

__all__ = ["UaintBot", "BotException", "ConfigurationError"]

# src/bot/cogs/__init__.py
"""
Módulos de comandos (Cogs) del bot
"""

# src/bot/cogs/utility/__init__.py
"""
Comandos de utilidad
"""