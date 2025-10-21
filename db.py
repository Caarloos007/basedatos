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

    CREATE TABLE IF NOT EXISTS ubicaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS rutas (
        origen_id INTEGER,
        destino_id INTEGER,
        distancia REAL NOT NULL,
        FOREIGN KEY (origen_id) REFERENCES ubicaciones(id),
        FOREIGN KEY (destino_id) REFERENCES ubicaciones(id),
        PRIMARY KEY (origen_id, destino_id)
    );
    """)

    # Insertar clientes
    conn.executemany(
        "INSERT INTO clientes (nombre, email, puntos) VALUES (?, ?, ?);",
        [
            ("Fulano García", "fulano@correo.com", 10),
        ],
    )

    # Insertar productos
    conn.executemany(
        "INSERT INTO productos (nombre, tipo, precio) VALUES (?, ?, ?);",
        [
            ("Espresso", "bebida", 1.8),
            ("Capuccino", "bebida", 2.5),
            ("Croissant", "comida", 1.6),
        ],
    )

    # Insertar ubicaciones (1 cafetería + 4 clientes)
    conn.executemany(
        "INSERT INTO ubicaciones (nombre) VALUES (?)",
        [
            ("Cafetería Central",),
            ("Cliente A",),
            ("Cliente B",),
            ("Cliente C",),
            ("Cliente D",),
        ],
    )

    # Insertar rutas entre ubicaciones (grafo no dirigido: agregamos ida y vuelta)
    conn.executemany(
        "INSERT INTO rutas (origen_id, destino_id, distancia) VALUES (?, ?, ?)",
        [
            (1, 2, 3.2), (2, 1, 3.2),
            (1, 3, 5.1), (3, 1, 5.1),
            (1, 4, 2.7), (4, 1, 2.7),
            (1, 5, 7.4), (5, 1, 7.4),
            (2, 3, 1.8), (3, 2, 1.8),
            (3, 4, 2.0), (4, 3, 2.0),
            (4, 5, 4.5), (5, 4, 4.5),
            (2, 5, 6.0), (5, 2, 6.0),
        ],
    )

    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada con éxito.")

if __name__ == "__main__":
    init_db()
