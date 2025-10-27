# update_data.py
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from load_data import session_factory
from models import User, Product, Order, Address
from decimal import Decimal

def update_users_with_descriptions():
    """Добавляет описания существующим пользователям"""
    with session_factory() as session:
        users = session.execute(select(User)).scalars().all()
        
        descriptions = [
            "Любитель путешествий и фотографии",
            "Программист и геймер",
            "Дизайнер интерьеров из Казани", 
            "Студент университета в Новосибирске",
            "Предприниматель из Краснодарского края"
        ]
        
        for user, description in zip(users, descriptions):
            user.description = description
        
        session.commit()
        print("Описания добавлены!")

def add_products_and_orders():
    """Добавляет продукты и заказы"""
    with session_factory() as session:

        products = [
            Product(name="Ноутбук Gaming Pro", description="Игровой ноутбук с RTX 4060", price=Decimal("150000.00")),
            Product(name="Смартфон Galaxy S24", description="Флагманский смартфон", price=Decimal("90000.00")),
            Product(name="Наушники Wireless", description="Беспроводные наушники с шумоподавлением", price=Decimal("15000.00")),
            Product(name="Умные часы Pro", description="Смарт-часы с функцией ECG", price=Decimal("50000.00")),
            Product(name="Планшет для рисования", description="Графический планшет с пером", price=Decimal("30000.00"))
        ]
        
        session.add_all(products)
        session.flush()
        print("Продукты созданы!")

        users = session.execute(
            select(User).options(selectinload(User.addresses))
        ).scalars().all()
        
        orders = []
        for i in range(5):
            user = users[i]
            
            primary_address = next((addr for addr in user.addresses if addr.is_primary), None)
            
            if not primary_address and user.addresses: 
                primary_address = user.addresses[0]   
                print(f"У пользователя {user.username} нет основного адреса, взят первый")
            
            if not primary_address:
                print(f"У пользователя {user.username} нет адресов, пропускаем заказ")
                continue
            
            order = Order(
                user_id=user.id,
                address_id=primary_address.id,
                product_id=products[i].id,
                quantity=1,
                status="completed",
                total_amount=products[i].price
            )
            orders.append(order)
        
        session.add_all(products + orders)
        session.commit()
        print("Продукты и заказы добавлены!")

if __name__ == "__main__":
    update_users_with_descriptions()
    add_products_and_orders()
    