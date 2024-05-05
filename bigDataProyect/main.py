import psycopg2
import re

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


'''nombre_tabla = "pagerank"

# Insertar el diccionario en la tabla
nombre_tabla2="indexinvert"
for clave,valor in dic.items():
    sql = f"INSERT INTO {nombre_tabla2} (word,indexdocument) VALUES (%s, %s)"
    cursor.execute(sql,(clave,valor) )'''

'''
for clave,valor in dicdoc.items():
    sql = f"INSERT INTO {nombre_tabla} (documento,refdocument) VALUES (%s, %s)"
    cursor.execute(sql,(clave,valor) )
'''
# Confirmar la transacción
connection.commit()



cursor.execute("")
# Ejecutar una consulta SELECT
cursor.execute("SELECT * FROM pagerank;")

# Recuperar los resultados de la consulta
rows = cursor.fetchall()

docs = [list(row) for row in rows]
#print(arreglo_resultados)
def sumatoria(d,i):
    nodo = d[i][0]
    sum=0
    for j in range(len(d)):
        if(j==i):
            continue
        tmp=d[j][2]
        tmp=tmp.split(',')
        if(nodo in tmp):
            sum = sum + (d[j][1]/len(tmp))
    return sum
def pageRank(docs,d):
    pR={}
    for i in range(len(docs)):
        docs[i][1]=(1-d)+d*sumatoria(docs,i)
        print(docs[i][1])
        pR[docs[i][0]]=docs[i][1]
    return pR
#docs=[["A",1,"B,C,D"],["B",1,"C,D"],["C",1,"A"],["D",1,"A,C"]]
valores = pageRank(docs, 0.85)

nombre_tabla = "pagerank"

# Iterar sobre el arreglo y actualizar la tabla
for clave, valor in valores.items():
    # Sentencia SQL para actualizar el valor en la tabla
    sql = f"UPDATE {nombre_tabla} SET pagerank = %s WHERE documento = %s"
    cursor.execute(sql, (valor,clave ))

# Confirmar la transacción
connection.commit()



if connection:
    cursor.close()
    connection.close()
    print("Conexión cerrada.")