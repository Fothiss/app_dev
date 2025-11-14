# scripts/update_data.py
import asyncio
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload
from models import User, Product, Order, Address
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv('DB_URL', 'sqlite+aiosqlite:///./lab3.db')

async def update_users_with_descriptions():
    """Добавляет описания существующим пользователям"""
    engine = create_async_engine(DB_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        users = (await session.execute(select(User))).scalars().all()
        
        descriptions = [
            "Любитель путешествий и фотографии",
            "Программист и геймер",
            "Дизайнер интерьеров из Казани", 
            "Студент университета в Новосибирске",
            "Предприниматель из Краснодарского края"
        ]
        
        for user, description in zip(users, descriptions):
            user.description = description
        
        await session.commit()
        print("Описания добавлены!")
    
    await engine.dispose()

async def add_products_and_orders():
    """Добавляет продукты и заказы"""
    engine = create_async_engine(DB_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        products = [
            Product(name="Ноутбук Gaming Pro", description="Игровой ноутбук с RTX 4060", price=Decimal("150000.00")),
            Product(name="Смартфон Galaxy S24", description="Флагманский смартфон", price=Decimal("90000.00")),
            Product(name="Наушники Wireless", description="Беспроводные наушники с шумоподавлением", price=Decimal("15000.00")),
            Product(name="Умные часы Pro", description="Смарт-часы с функцией ECG", price=Decimal("50000.00")),
            Product(name="Планшет для рисования", description="Графический планшет с пером", price=Decimal("30000.00"))
        ]
        
        session.add_all(products)
        await session.flush()

        users = (await session.execute(
            select(User).options(selectinload(User.addresses))
        )).scalars().all()
        
        orders = []
        for i in range(5):
            user = users[i]
            primary_address = next((addr for addr in user.addresses if addr.is_primary), user.addresses[0] if user.addresses else None)
            
            if primary_address:
                order = Order(
                    user_id=user.id,
                    address_id=primary_address.id,
                    product_id=products[i].id,
                    quantity=1,
                    status="completed",
                    total_amount=products[i].price
                )
                orders.append(order)
        
        session.add_all(orders)
        await session.commit()
        print("Продукты и заказы добавлены!")
    
    await engine.dispose()

async def main():
    await update_users_with_descriptions()
    await add_products_and_orders()

if __name__ == "__main__":
    asyncio.run(main())