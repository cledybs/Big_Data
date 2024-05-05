import matplotlib.pyplot as plt
import networkx as nx
import random
import psycopg2
import os

try:
    connection = psycopg2.connect(
        user="postgres",

        password="hadoop",
        host="localhost",
        port="5432",
        database="postgres"
    )
except (Exception, psycopg2.Error) as error:
    print("Error al conectar a la base de datos:", error)


cursor = connection.cursor()

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index_principal.html')

def graficar_page_rank(final_results):
    G = nx.DiGraph()
    
    #global final_results
    print(final_results)

    # Agregar nodos al grafo
    for doc, rank, _ in final_results:
        G.add_node(doc, pagerank=rank)  # Añadir el atributo 'pagerank' al nodo

    # Agregar aristas entre los nodos relacionados
    for doc, _, related_docs in final_results:
        related_docs = related_docs.split(',')
        for related_doc in related_docs:
            if related_doc.strip() != '' and G.has_node(related_doc):
                G.add_edge(doc, related_doc.strip())

    # Verificar nodos y atributos
    for node, data in G.nodes(data=True):
        print("Node:", node)
        print("Attributes:", data)

    # Calcular tamaños de los nodos basados en el PageRank
    node_sizes = [G.nodes[node].get('pagerank', 0) * 5000 for node in G.nodes()]
    print(node_sizes)
    
    # Generar colores aleatorios para los nodos
    node_colors = [generar_color_aleatorio() for _ in G.nodes()]
    print(node_colors)

    # Dibujar el grafo
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, font_size=10, font_weight='bold', arrowsize=20)
    plt.title("Grafo de Page Rank")
    #plt.show()
    # Get the path to the static directory
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    # Save the plot as a PNG file in the static directory
    plt.savefig(os.path.join(static_dir, 'page_rank_graph.png'))
    plt.close()

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('query')
    
    valores = query.split()
    placeholders = ','.join(['%s'] * len(valores))
    cursor.execute("""
	    SELECT documento, pagerank, refdocument 
	    FROM pagerank 
	    WHERE documento IN (
		SELECT DISTINCT unnest(string_to_array(concatenated_string, ',')) AS distinct_names 
		FROM (
		    SELECT string_agg(indexdocument, ',') AS concatenated_string 
		    FROM indexinvert 
		    WHERE word IN ({}) 
		) AS subquery 
	    ) 
	    ORDER BY pagerank DESC 
	    LIMIT 10;""".format(placeholders), valores)
    
    results = cursor.fetchall()
    #print(results)
    
    #cursor.close()
    #connection.close()
    # Aquí puedes procesar la consulta como lo necesites
    # Por ejemplo, podrías realizar una búsqueda en una base de datos
    # y luego renderizar la plantilla 'resultados.html' con los resultados.
    with open('query.txt', 'a') as f:
        f.write(query + '\n')

    graficar_page_rank(results.copy())

    return render_template('resultados.html', query=results)

@app.route('/index_principal')
def index_principal():
    return render_template('index_principal.html')

@app.route('/resultados')
def resultados():
    return render_template('resultados.html')
    
@app.route('/mostrar_texto/<nombre_archivo>')
def mostrar_texto(nombre_archivo):
    # Construye la ruta del archivo de texto
    ruta_archivo = f"static/files/{nombre_archivo}"

    # Lee el contenido del archivo de texto
    with open(ruta_archivo, 'r') as archivo:
        contenido = archivo.read()

    # Renderiza la plantilla y pasa el contenido del archivo como contexto
    return render_template('mostar_texto.html', contenido=contenido)
    
def generar_color_aleatorio():
    # Generar valores RGB aleatorios entre 0 y 255
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    # Devolver el color en formato hexadecimal
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


    
if __name__ == '__main__':
    # Ejemplo de datos de Page Rank
    page_rank_data = [
        ('d1', 0.6000000043, "d2,d3,d4"),
        ('d2', 1.4000000043, "d3,d5,d1, d16"),
        ('d5', 5.20000043, "d4,d87"),
        ('d3', 3.9000000043, "d35,d4,d5"),
        ('d4', 0.1043, "d1,d2")
    ]

    # Graficar el grafo
    app.run(debug=True)
    #print(final_results)
    #print(page_rank_data)
    global final_results
    graficar_page_rank(final_results)
    print(final_results)

