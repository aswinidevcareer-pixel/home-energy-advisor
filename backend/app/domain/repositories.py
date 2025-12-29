from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities import HomeProfile


class HomeRepository(ABC):
    @abstractmethod
    async def create(self, home: HomeProfile) -> HomeProfile:
        pass

    @abstractmethod
    async def get_by_id(self, home_id: str) -> Optional[HomeProfile]:
        pass

    @abstractmethod
    async def update(self, home: HomeProfile) -> HomeProfile:
        pass

    @abstractmethod
    async def delete(self, home_id: str) -> bool:
        pass
