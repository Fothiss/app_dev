from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session
from load_data import engine
from models import User, Address

def get_users_addresses():
    """Получить всех пользователей с адресами"""
    stmt=select(User).options(selectinload(User.addresses))

    with Session(engine) as session:
        users = session.execute(stmt).scalars().all()
        
        for user in users:
            print(f"👤 {user.username} ({user.email})")
            for address in user.addresses:
                print(f"   {address.city}, {address.street}")
            print()
        
        return users

if __name__ == "__main__":
    get_users_addresses()
