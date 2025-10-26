"""VC Scout Agent - AI-powered founder intelligence for venture capital firms."""

from .workflows import FounderScoutCrew, FounderProfile
from .agents import ScoutAgents
from .config import settings

__version__ = "0.1.0"

__all__ = [
    "FounderScoutCrew",
    "FounderProfile",
    "ScoutAgents",
    "settings",
]
