import re


dic = {}
dicdoc ={}
dococument =[]
for i in range(60):
    dococument.append("doc"+str(i))


with open('/home/h-user/Downloads/part-r-00000(3)', 'r') as archivo:
    # Itera sobre cada línea en el archivo
    for linea in archivo:
        partes = linea.split('\t')

        palabra = partes[0]
        cadena = partes[1]
        if(palabra in dococument):
            cadena_modificada = re.sub(r':\d+', '', cadena)
            cadena_modificada = cadena_modificada.replace("  ", ",")
            cadena_modificada= cadena_modificada[:-2]
            dicdoc[palabra]=cadena_modificada 
            continue

        cadena_modificada = re.sub(r':\d+', '', cadena)
        cadena_modificada = cadena_modificada.replace("  ", ",")
        cadena_modificada= cadena_modificada[:-2]
        dic[palabra]=cadena_modificada

ruta_archivo = "indexInverted.txt"

# Guardar el diccionario en el archivo
with open(ruta_archivo, "w") as archivo:
    for clave, valor in dic.items():
        archivo.write(f"{clave}:{valor}\n")

ruta_archivo = "dicdoc.txt"

# Guardar el diccionario en el archivo
with open(ruta_archivo, "w") as archivo:
    for clave, valor in dicdoc.items():
        archivo.write(f"{clave}:{valor}\n")

#print("Diccionario guardado exitosamente en", ruta_archivo)