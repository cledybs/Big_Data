import matplotlib.pyplot as plt
import networkx as nx
import random

def generar_color_aleatorio():
    # Generar valores RGB aleatorios entre 0 y 255
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    # Devolver el color en formato hexadecimal
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def graficar_page_rank(page_rank_data):
    G = nx.DiGraph()

    # Agregar nodos al grafo
    for doc, rank, _ in page_rank_data:
        G.add_node(doc, pagerank=rank)  # Añadir el atributo 'pagerank' al nodo

    # Agregar aristas entre los nodos relacionados
    for doc, _, related_docs in page_rank_data:
        related_docs = related_docs.split(',')
        for related_doc in related_docs:
            if related_doc.strip() != '':
                G.add_edge(doc, related_doc.strip())

    # Verificar nodos y atributos
    for node, data in G.nodes(data=True):
        print("Node:", node)
        print("Attributes:", data)

    # Calcular tamaños de los nodos basados en el PageRank
    node_sizes = [G.nodes[node].get('pagerank', 0) * 5000 for node in G.nodes()]

    # Generar colores aleatorios para los nodos
    node_colors = [generar_color_aleatorio() for _ in G.nodes()]

    # Dibujar el grafo
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, font_size=10, font_weight='bold', arrowsize=20)
    plt.title("Grafo de Page Rank")
    plt.show()

# Ejemplo de datos de Page Rank
page_rank_data = [
    ('d1', 0.6, "d2,d3,d4"),
    ('d2', 0.4, "d3,d5,d1"),
    ('d5', 0.2, "d4"),
    ('d3', 0.9, "d4,d5"),
    ('d4', 0.1, "d1,d2")
]

# Graficar el grafo
graficar_page_rank(page_rank_data)
