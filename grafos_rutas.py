import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

DB_PATH = "smartcoffee.db"

def obtener_rutas_y_ubicaciones():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    ubicaciones = conn.execute("SELECT * FROM ubicaciones").fetchall()
    rutas = conn.execute("SELECT * FROM rutas").fetchall()

    conn.close()
    return ubicaciones, rutas

def construir_grafo(ubicaciones, rutas):
    G = nx.Graph()  # Grafo no dirigido

    id_a_nombre = {u["id"]: u["nombre"] for u in ubicaciones}
    
    for u in ubicaciones:
        G.add_node(u["nombre"])

    for r in rutas:
        origen = id_a_nombre[r["origen_id"]]
        destino = id_a_nombre[r["destino_id"]]
        distancia = r["distancia"]
        G.add_edge(origen, destino, weight=distancia)

    return G

def encontrar_cliente_mas_lejano(G, origen):
    longitudes = nx.single_source_dijkstra_path_length(G, origen, weight='weight')
    destino_mas_lejano = max(longitudes, key=longitudes.get)
    distancia = longitudes[destino_mas_lejano]
    camino = nx.shortest_path(G, origen, destino_mas_lejano, weight='weight')
    return camino, distancia

def dibujar_grafo(G, camino_resaltado=None):
    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if camino_resaltado:
        path_edges = list(zip(camino_resaltado, camino_resaltado[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)

    plt.title("Rutas desde la Cafetería")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    ubicaciones, rutas = obtener_rutas_y_ubicaciones()
    G = construir_grafo(ubicaciones, rutas)

    origen = "Cafetería Central"
    camino, distancia = encontrar_cliente_mas_lejano(G, origen)

    print(f"Camino más largo desde la Cafetería: {' -> '.join(camino)} (Distancia: {distancia} km)")

    dibujar_grafo(G, camino_resaltado=camino)
