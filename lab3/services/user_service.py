from typing import List, Optional
import uuid

from repositories.user_repository import UserRepository
from models import User
from schemas import UserCreate, UserUpdate

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Получить пользователя по ID"""
        return await self.user_repository.get_by_id(user_id)

    async def get_by_filter(self, count: int, page: int, **kwargs) -> list[User]:
        """Получить пользователей с фильтрацией и пагинацией"""
        return await self.user_repository.get_by_filter(count=count, page=page, **kwargs)

    async def create(self, user_data: UserCreate) -> User:
        """Создать нового пользователя"""
        return await self.user_repository.create(user_data)

    async def update(self, user_id: uuid.UUID, user_data: UserUpdate) -> User:
        """Обновить пользователя"""
        return await self.user_repository.update(user_id, user_data)

    async def delete(self, user_id: int) -> None:
        """Удалить пользователя"""
        return await self.user_repository.delete(user_id)
    async def get_total_count(self, **kwargs) -> int:
        """Получить общее количество пользователей"""
        return await self.user_repository.get_total_count(**kwargs)
