from abc import ABC, abstractmethod
from typing import Sequence

from aiogram import Bot

from asgi_aiogram.types import ScopeType


class BaseStrategy(ABC):

    @abstractmethod
    async def resolve_bot(self, scope: ScopeType) -> Bot | None:
        pass

    @abstractmethod
    async def verify_path(self, path: str) -> bool:
        pass

    async def startup(self):
        pass

    async def shutdown(self):
        pass

    @property
    def bots(self) -> Sequence[Bot]:
        return []

    @property
    def bot(self) -> Bot | None:
        return
