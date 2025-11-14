import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import User, Address, Base  # относительный импорт
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv('DB_URL', 'sqlite+aiosqlite:///./lab3.db')

async def load_data():
    """Создает таблицы и загружает данные"""
    engine = create_async_engine(DB_URL, echo=True)
    
    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Загружаем данные
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        
        user1 = User(
            username="ivanov",
            email="ivanov@example.com"
        )
        address1_1 = Address(
            street="ул. Ленина, 15",
            city="Москва",
            state="Московская область",
            zip_code="101000",
            country="Russia",
            is_primary=True,
            user=user1  
        )
        address1_2 = Address(
            street="пр. Победы, 42",
            city="Москва", 
            state="Московская область",
            zip_code="101001",
            country="Russia",
            is_primary=False,
            user=user1  
        )
    
        user2 = User(
            username="petrov",
            email="petrov@example.com"
        )
        address2_1 = Address(
            street="Невский пр., 25",
            city="Санкт-Петербург",
            state="Ленинградская область",
            zip_code="190000",
            country="Russia", 
            is_primary=True,
            user=user2 
        )
        
        user3 = User(
            username="sidorova", 
            email="sidorova@example.com"
        )
        address3_1 = Address(
            street="ул. Баумана, 8",
            city="Казань",
            state="Татарстан",
            zip_code="420000",
            country="Russia",
            is_primary=True,
            user=user3 
        )
        address3_2 = Address(
            street="ул. Кремлевская, 35",
            city="Казань",
            state="Татарстан", 
            zip_code="420001",
            country="Russia",
            is_primary=False,
            user=user3 
        )
        
        user4 = User(
            username="kozlov",
            email="kozlov@example.com"
        )
        address4_1 = Address(
            street="ул. Советская, 77",
            city="Новосибирск",
            state="Новосибирская область", 
            zip_code="630000",
            country="Russia",
            is_primary=True,
            user=user4  
        )
        
        user5 = User(
            username="novikova",
            email="novikova@example.com"
        )
        address5_1 = Address(
            street="ул. Красная, 12",
            city="Краснодар",
            state="Краснодарский край",
            zip_code="350000", 
            country="Russia",
            is_primary=True,
            user=user5  
        )
        address5_2 = Address(
            street="ул. Мира, 33",
            city="Сочи",
            state="Краснодарский край",
            zip_code="354000",
            country="Russia", 
            is_primary=False,
            user=user5
        )
        address5_3 = Address(
            street="ул. Курортная, 5",
            city="Анапа", 
            state="Краснодарский край",
            zip_code="353440",
            country="Russia",
            is_primary=False,
            user=user5  
        )
        
        users = [user1, user2, user3, user4, user5]
        addresses = [
            address1_1, address1_2, address2_1, address3_1, address3_2,
            address4_1, address5_1, address5_2, address5_3
        ]
        
        session.add_all(users + addresses)
        await session.commit()
        print("Данные успешно добавлены!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(load_data())