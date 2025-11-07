from litestar import Controller, get, post, put, delete
from litestar.params import Parameter, Body
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from typing import List, Optional
import uuid

from services.user_service import UserService
from models import User
from schemas import UserCreate, UserUpdate, UserResponse, UsersListResponse

class UserController(Controller):
    path = "/users"
#    dependencies = {"user_service": Provide("user_service")}

    @get("/{user_id:uuid}")
    async def get_user_by_id(
        self, 
        user_service: UserService, 
        user_id: uuid.UUID = Parameter()
        ) -> UserResponse:
        """Получить пользователя по ID"""
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(
        self,
        user_service: UserService,
        count: int = Parameter(gt=0, le=100, default=10),
        page: int = Parameter(ge=1, default=1),
        username: Optional[str] = Parameter(default=None),
    ) -> UsersListResponse:
        """Получить всех пользователей"""       
        # Собираем фильтры
        filters = {}
        if username:
            filters["username"] = username
        
        users = await user_service.get_by_filter(count=count, page=page, **filters)
        total_count = await user_service.get_total_count(**filters)
        
        user_responses = [UserResponse.model_validate(user, from_attributes=True) for user in users]
        response = UsersListResponse(
            users=user_responses,
            total_count=total_count 
        )
        
        return response

    @post()
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate = Body(),
    ) -> UserResponse:
        """Создать нового пользователя"""
        user = await user_service.create(data)
        response = UserResponse.model_validate(user, from_attributes=True)
        
        return response

    @delete("/{user_id:uuid}")
    async def delete_user(
        self,
        user_service: UserService,
        user_id: uuid.UUID = Parameter(),
    ) -> None:
        """Удалить пользователя"""
        await user_service.delete(user_id)

    @put("/{user_id:uuid}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: uuid.UUID = Parameter(),
        data: UserUpdate = Body(),
    ) -> UserResponse:
        """Обновить пользователя"""
        user = await user_service.update(user_id, data)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)
