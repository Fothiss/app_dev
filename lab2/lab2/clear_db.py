# clear_db.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv('DB_URL')
engine = create_engine(DB_URL)
session_factory = sessionmaker(bind=engine)

def clear_database():
    """Полностью очищает базу данных"""
    with session_factory() as session:
        try:
            # Для SQLite
            if 'sqlite' in DB_URL:
                session.execute(text("PRAGMA foreign_keys=OFF"))
                session.execute(text("DELETE FROM addresses"))
                session.execute(text("DELETE FROM users"))
                session.execute(text("PRAGMA foreign_keys=ON"))
            # Для PostgreSQL
            elif 'postgresql' in DB_URL:
                session.execute(text("TRUNCATE TABLE addresses, users CASCADE"))
            
            session.commit()
            print("✅ База данных очищена!")
            
        except Exception as e:
            session.rollback()
            print(f"❌ Ошибка при очистке: {e}")

if __name__ == "__main__":
    clear_database()