import sqlite3

def init_db():
    conn = sqlite3.connect("smartcoffee.db")
    conn.execute("PRAGMA foreign_keys = ON")

    conn.executescript("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        puntos INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        tipo TEXT NOT NULL,
        precio REAL NOT NULL
    );
    """)

    conn.executemany(
        "INSERT INTO clientes (nombre, email, puntos) VALUES (?, ?, ?);",
        [
            ("Fulano García", "fulano@correo.com", 10),
        ],
    )

    conn.executemany(
        "INSERT INTO productos (nombre, tipo, precio) VALUES (?, ?, ?);",
        [
            ("Espresso", "bebida", 1.8),
            ("Capuccino", "bebida", 2.5),
            ("Croissant", "comida", 1.6),
        ],
    )

    conn.commit()
    conn.close()
    print("Todo ok, Bro")

if __name__ == "__main__":
    init_db()

import sqlite3
from contextlib import closing

DB_PATH = "smartcoffee.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    conn.execute("PRAGMA foreign_keys = ON")  # Habilita claves foráneas
    return conn


def exec_script(sql: str):
    """Ejecuta un script SQL completo (por ejemplo, para crear tablas)."""
    with closing(get_conn()) as conn:  # Asegura cierre de conexión
        with conn:  # Asegura commit/rollback automático
            conn.executescript(sql)

