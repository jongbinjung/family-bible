"""Shared data models"""

from enum import StrEnum, auto
from pydantic import BaseModel, computed_field


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


class UserProgressMetrics(BaseModel):
    """Progress metrics for a single user."""

    ytd_completed: int
    ytd_planned: int
    total_completed: int
    total_planned: int

    @computed_field
    @property
    def ytd_completion_rate(self) -> float:
        """Year-to-date completion percentage."""
        if self.ytd_planned == 0:
            return 0.0
        return self.ytd_completed / self.ytd_planned

    @computed_field
    @property
    def total_completion_rate(self) -> float:
        """Total completion percentage."""
        if self.total_planned == 0:
            return 0.0
        return self.total_completed / self.total_planned

    @computed_field
    @property
    def past_unread(self) -> int:
        """Past plans that are unread"""
        return max(0, self.ytd_planned - self.ytd_completed)

    @computed_field
    @property
    def up_to_date(self) -> bool:
        """Whether progress is up-to-date"""
        return self.past_unread == 0
