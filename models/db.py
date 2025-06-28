import sqlite3

def get_db_connection():
    return sqlite3.connect('tasks.db')  # Conectar a la base de datos SQLite

def init_db():
    conn = get_db_connection()
    c = conn.cursor() # Crear un cursor para ejecutar comandos SQL
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            priority TEXT NOT NULL,
            date TEXT NOT NULL DEFAULT (datetime('now')),
            done BOOLEAN NOT NULL DEFAULT 0
        )''')
    conn.commit() # Confirmar los cambios
    conn.close() # Cerrar la conexión a la base de datos