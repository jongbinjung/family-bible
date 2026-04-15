"""Poor man's configs"""

from src.models import Language

DEBUG: bool = False
DEFAULT_LANGUAGE: Language = Language.KO

MAX_FUTURE_WEEKS: int = 1

CATCH_UP_THRESHOLD: int = 3
