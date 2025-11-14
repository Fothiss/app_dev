from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from models import User
from schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_filter(self, count: int = 10, page: int = 1, **kwargs) -> List[User]:
        """Получить пользователей с фильтрацией и пагинацией"""
        query = select(User)
        
        # Применяем фильтры
        for key, value in kwargs.items():
            if hasattr(User, key):
                query = query.where(getattr(User, key) == value)
        
        # Пагинация
        query = query.offset((page - 1) * count).limit(count)
        
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, user_data: UserCreate) -> User:
        """Создать нового пользователя"""
        user = User(
            username=user_data.username,
            email=user_data.email,
            description=user_data.description
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:  # МЕНЯЕМ НА int
        """Обновить пользователя"""
        user = await self.get_by_id(user_id)
        if not user:
            return None
            
        # Обновляем только переданные поля
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
            
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: int) -> None:
        """Удалить пользователя"""
        user = await self.get_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()

    async def get_total_count(self, **kwargs) -> int:
        """Получить общее количество пользователей с фильтрацией"""
        query = select(func.count(User.id))
    
        for key, value in kwargs.items():
            if hasattr(User, key):
                query = query.where(getattr(User, key) == value)
    
        result = await self.session.execute(query)
        count = result.scalar()

        return count