from typing import Optional
from app.domain.entities import HomeProfile
from app.domain.repositories import HomeRepository
from app.application.home_dtos import CreateHomeRequest, HomeResponse


class HomeService:
    def __init__(self, repository: HomeRepository):
        self.repository = repository

    async def create_home(self, request: CreateHomeRequest) -> HomeResponse:
        home_profile = HomeProfile(**request.model_dump())
        created_home = await self.repository.create(home_profile)
        return HomeResponse(**created_home.model_dump())

    async def get_home(self, home_id: str) -> Optional[HomeResponse]:
        home = await self.repository.get_by_id(home_id)
        if home:
            return HomeResponse(**home.model_dump())
        return None
