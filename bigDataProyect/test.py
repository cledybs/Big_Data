import os
from collections import defaultdict

def construir_indice(documentos):
    indice = defaultdict(set)
    for doc_id, doc_content in documentos.items():
        palabras = doc_content.split()
        for palabra in palabras:
            indice[palabra].add(doc_id)
    return indice

def buscar(indice, consulta):
    resultados = set()
    palabras = consulta.split()
    for palabra in palabras:
        resultados.update(indice.get(palabra, set()))
    return resultados

# Directorio donde se encuentran los documentos
directorio = "/home/h-user/bigDataProyect/docs"

def leer_documentos(directorio):
    documentos = {}
    for filename in os.listdir(directorio):
        if filename.endswith(".txt"):
            with open(os.path.join(directorio, filename), "r") as file:
                documentos[filename] = file.read()
    return documentos

# Ejemplo de uso
documentos = leer_documentos(directorio)
for i in documentos.values() :
    print(i)
indice = construir_indice(documentos)

consulta = "documento palabras"
resultados = buscar(indice, consulta)

print("Resultados de la consulta '{}':".format(consulta))
for doc_name in resultados:
    print("- Documento", doc_name, ":", documentos[doc_name])
