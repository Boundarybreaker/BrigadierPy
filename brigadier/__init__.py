from abc import ABC, abstractmethod
from typing import TypeVar, Collection, Generic

from brigadier.context import CommandContext

S = TypeVar('S')


class Message(ABC):
    @abstractmethod
    def get_string(self) -> str:
        return ""


class ImmutableStringReader(ABC):
    @abstractmethod
    def get_string(self) -> str:
        return ""

    @abstractmethod
    def get_remaining_length(self) -> int:
        return 0

    @abstractmethod
    def get_total_length(self) -> int:
        return 0

    @abstractmethod
    def get_cursor(self) -> int:
        return 0

    @abstractmethod
    def get_read(self) -> str:
        return ""

    @abstractmethod
    def get_remaining(self) -> str:
        return ""

    @abstractmethod
    def can_read(self, length: int) -> bool:
        return False

    @abstractmethod
    def peek(self) -> str:
        return ""

    @abstractmethod
    def peek(self, offset: int) -> str:
        return ""


class Command(ABC, Generic[S]):
    @abstractmethod
    def run(self, ctx: CommandContext[S]) -> int:
        return 0


class RedirectModifier(ABC, Generic[S]):
    @abstractmethod
    def apply(self, ctx: CommandContext[S]) -> Collection[S]:
        return []
