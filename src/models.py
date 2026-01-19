"""Shared data models"""

from enum import StrEnum, auto
from pydantic import BaseModel


class Keys(StrEnum):
    """State keys"""

    ACTIVE_USER_PROGRESS = auto()
    CURRENT_USER_DETAILS = auto()
    IMPERSONATED_USER_DETAILS = auto()
    IMPERSONATING_USER_EMAIL = auto()
    LANGUAGE = auto()
    SHOW_COMPLETED = auto()


class Group(StrEnum):
    """User groups in the system."""

    CHA = auto()  # Cha fam
    CNB = auto()  # Chestnutberry
    EXT = auto()  # Extended fam
    JUN = auto()  # Jung elders
    SIB = auto()  # Siblings


class Language(StrEnum):
    """Supported languages."""

    EN = auto()
    KO = auto()


class Role(StrEnum):
    """User roles in the system."""

    ADMIN = auto()
    GUEST = auto()
    USER = auto()


class UserDetails(BaseModel):
    """Details about a user."""

    username: str
    email: str
    role: Role
    group: Group
    language: Language
    viewables: list[Group]
