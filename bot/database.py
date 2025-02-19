import sqlite3

DB_PATH = 'users.db'


def setup_database():
    """Создание таблицы, если её нет"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                class_name TEXT NOT NULL,
                full_name TEXT NOT NULL,
                UNIQUE(user_id, class_name, full_name)
            )
        ''')
        conn.commit()


async def save_user_data(
        user_id: int,
        class_name: str,
        full_name: str) -> bool:
    """Сохранение данных в БД с проверкой дублей"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 1
            FROM users
            WHERE user_id = ?
              AND class_name = ?
              AND full_name = ?
        ''', (user_id, class_name, full_name))

        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO users (user_id, class_name, full_name)
                VALUES (?, ?, ?)
            ''', (user_id, class_name, full_name))
            conn.commit()
            return True
        return False
