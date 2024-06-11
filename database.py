import sqlite3

def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            task TEXT
        )
    ''')
    conn.commit()
    conn.close()

# def add_task(user_id, username, task):
#     conn = sqlite3.connect('tasks.db')
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO tasks (user_id, username, task) VALUES (?, ?, ?)", (user_id, username, task))
#     conn.commit()
#     conn.close()


def add_task(user_id, username, task):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user_id =? AND task =?", (user_id, task))
    existing_task = cursor.fetchone()
    if existing_task:
        conn.close()
        return False  # Task already exists
    else:
        cursor.execute("INSERT INTO tasks (user_id, username, task) VALUES (?,?,?)", (user_id, username, task))
        conn.commit()
        conn.close()
        return True  # Task added successfully
def get_task():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY id ASC")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# def delete_task(task_id):
#     conn = sqlite3.connect('tasks.db')
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
#     conn.commit()
#     conn.close()
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id =?", (task_id,))
    conn.commit()

    # Update IDs of remaining tasks
    cursor.execute("SELECT id FROM tasks WHERE id >?", (task_id,))
    remaining_tasks = cursor.fetchall()
    for task in remaining_tasks:
        new_id = task[0] - 1
        cursor.execute("UPDATE tasks SET id =? WHERE id =?", (new_id, task[0]))
    conn.commit()
    conn.close()