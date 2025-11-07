from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime


class UserBase(BaseModel):
    """Базовые поля, общие для создания и обновления"""
    username: str
    email: str
    description: Optional[str] = None

class UserCreate(UserBase):
    """Для создания пользователя - наследует все от UserBase"""
    pass

class UserUpdate(BaseModel):
    """Для обновления пользователя - все поля опциональны"""
    username: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None

class UserResponse(UserBase):
    """Для ответа API - добавляем системные поля"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    
class UsersListResponse(BaseModel):
    """Для вывода всех пользователей с общим количеством"""
    users: List[UserResponse]
    total_count: int

    class Config:
        from_attributes = True