import sqlite3
from contextlib import closing

DB_PATH = "smartcoffee.db"

def exec_script(sql: str):
    with closing(get_conn()) as conn:
        with conn:
            conn.executescript(sql)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

class Cliente:
    def __init__(self, id, email, puntos_fidelidad):
        self.id = id
        self.email = email
        self.puntos_fidelidad = puntos_fidelidad

    def __str__(self):
        return f"Cliente {self.id} con email {self.email} y puntos de fidelidad {self.puntos_fidelidad}"

    def crear_cliente(nombre, email, puntos=0):
        with closing(get_conn()) as conn:
            conn.execute(
                "INSERT INTO clientes (nombre, email, puntos) VALUES (?, ?, ?)",
                (nombre, email, puntos),
            )

    def obtener_clientes():
        with closing(get_conn()) as conn:
            return conn.execute("SELECT * FROM clientes ORDER BY id").fetchall()

class Producto:
    def __init__(self, id, nombre, precio, tipo):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.tipo = tipo

    def __str__(self):
        return f"Producto {self.id} con nombre {self.nombre} precio {self.precio} y tipo {self.tipo}"

class Pedido:
    pedidos_registrados = []

    def __init__(self, id, cliente, producto, empleado, total):
        self.id = id
        self.cliente = cliente
        self.producto = producto
        self.empleado = empleado
        self.total = total

    def registrar_pedido(self):
        Pedido.pedidos_registrados.append(self)
        print(f"Pedido registrado: ID {self.id}, Cliente {self.cliente}, Producto {self.producto}, Empleado {self.empleado}, Total {self.total}")

class Empleado:
    def __init__(self, id, nombre, rol, turno):
        self.id = id
        self.nombre = nombre
        self.rol = rol
        self.turno = turno

class Contiene:
    def __init__(self, pedido_id, producto_id):
        self.pedido_id = pedido_id
        self.producto_id = producto_id
