import sqlite3

import openpyxl

DB_PATH = 'users.db'


def setup_database():
    """ Create table if not exists """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                class_name TEXT NOT NULL,
                full_name TEXT NOT NULL,
                completed_tasks TEXT DEFAULT '',
                UNIQUE(user_id, class_name, full_name)
            )
        ''')
        conn.commit()


async def save_user_data(
        user_id: int,
        class_name: str,
        full_name: str) -> bool:
    """ Save user data to database """
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


async def update_completed_tasks(user_id: int, task_number: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT completed_tasks
            FROM users
            WHERE user_id = ?
        ''', (user_id,))
        result = cursor.fetchone()

        if result:
            current_tasks = result[0] or ""
            tasks_list = current_tasks.split(',') if current_tasks else []
            try:
                task_number = int(task_number)
            except ValueError:
                raise ValueError('Номер задания должен быть целым числом')

            if str(task_number) not in tasks_list:
                tasks_list.append(str(task_number))
                tasks_list = sorted(tasks_list, key=int)
                updated_tasks = ','.join(tasks_list)
                cursor.execute('''
                    UPDATE users
                    SET completed_tasks = ?
                    WHERE user_id = ?
                ''', (updated_tasks, user_id))
                conn.commit()


async def get_users():
    """ Get users from database """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_id, class_name, full_name, completed_tasks
            FROM users
        ''',)
        return cursor.fetchall()


async def export_users_to_excel():
    """ Export users data to Excel file """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_id, class_name, full_name, completed_tasks
            FROM users
        ''')
        users = cursor.fetchall()

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Пользователи'

    sheet.append(['ID', 'Класс', 'Имя', 'Выполненные задания'])

    for user in users:
        user_id, class_name, full_name, completed_tasks = user
        sheet.append([user_id, class_name, full_name, completed_tasks])

    file_path = 'users_export.xlsx'
    workbook.save(file_path)
    return file_path


async def get_user_full_name(user_id: int) -> str:
    """ Get user full name from database """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT full_name FROM users WHERE user_id = ?
        ''', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None


async def get_user_ids():
    """ Get user IDs from database """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_id FROM users
        ''')
        return [row[0] for row in cursor.fetchall()]
