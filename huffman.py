# Autor: Alejandro Flores Jacobo 
# Fecha: 11-05-2023
# Descripcion: 
# Script aplicar el algoritmo de compresion Huffman a un archivo.

import time
inicio = time.time()
# -----------------------------------------[Arbol binario]-----------------------------------------

# La clase NodoABB define los nodos del árbol y contiene tres atributos: info, que almacena la información del nodo, 
# y izq y der, que son punteros a los hijos izquierdo y derecho del nodo, respectivamente.
class NodoABB:
    def __init__(self, info):
        self.info = info
        self.izq = None
        self.der = None

# La función insertar_nodo inserta un nuevo nodo con la información dato en el árbol ABB raiz. Si el árbol está vacío, 
# se crea un nuevo nodo en la raíz. Si el dato es menor que la información en la raíz, se inserta en el subárbol izquierdo. 
# De lo contrario, se inserta en el subárbol derecho.
def insertar_nodo(raiz, dato):
    if raiz is None:
        raiz = NodoABB(dato)
    elif dato < raiz.info:
        raiz.izq = insertar_nodo(raiz.izq, dato)
    else:
        raiz.der = insertar_nodo(raiz.der,dato)
    return raiz

# La función buscar busca un nodo con información clave en el árbol ABB raiz. Si la clave se encuentra en la raíz, 
# se devuelve el nodo de la raíz. De lo contrario, se busca en el subárbol izquierdo 
# si la clave es menor que la información en la raíz, o en el subárbol derecho si la clave es mayor.
def buscar(raiz,clave):
    pos = None
    if raiz is not None:
        if raiz.info == clave:
            pos = raiz
        elif clave < raiz.info:
            pos = buscar(raiz.izq, clave)
        else:
            pos = buscar(raiz.der, clave)
    return pos

# La función crear_Arbol crea un árbol ABB a partir de una lista de nodos de frecuencia (los nodos son tuplas que contienen 
# información y frecuencia). El algoritmo funciona combinando los dos nodos de frecuencia más bajos en un nuevo nodo y 
# agregando este nuevo nodo a la lista. Este proceso se repite hasta que se crea un solo nodo, que se convierte en la raíz del árbol.
def crear_Arbol(list_frecuencias):
    nodo_Aux = NodoABB(None)
    nodo_Aux.info = (None, list_frecuencias[0].info[1] + list_frecuencias[1].info[1])
    nodo_Aux.izq = list_frecuencias[0]
    nodo_Aux.der = list_frecuencias [1]

    list_frecuencias.append(nodo_Aux)   # se anade el nodo formado al final de la lista
    del list_frecuencias[0:2]   # Se eliminar los primeros nodos que ya forma un solo nodos
    
    return list_frecuencias

# La función preorden_binario realiza un recorrido preorden del árbol y asigna un código binario único a cada información del nodo. 
# El código binario se almacena en un diccionario, donde la clave es la información del nodo y el valor es el código binario correspondiente.
def preorden_binario(raiz, diccionario, binario):
    if raiz is not None:
        diccionario[raiz.info[0]] = binario
        preorden_binario(raiz.izq, diccionario, (binario + '0') )
        preorden_binario(raiz.der,diccionario, (binario + '1'))
        
    return diccionario

# -----------------------------------------[Probabildades de los simbolos]-----------------------------------------

# Nombre del archivo a leer
archivo = 'h.jpg'
# archivo = 'archivo.py'
# archivo = 'archivo.bin'

with open(archivo, 'rb') as f:  # Leer el contenido del archivo
    cadena = f.read()
    f.close()

if (len(cadena)) % 2 != 0:    # Verificar si hay simbolos suficientes de 2 bytes
    cadena += b'\x00'         # Agregar un byte de padding

# Funcion para determinar el tamano apropiado para los simbolos siendo 16 caracteres o 2 bytes como maximo 
tope = 1     # Se establece una variable tope en 1, que será utilizada para determinar el tamaño apropiado para los símbolos.
while True:
    if len(cadena) == 2:    # Si la longitud es 2 concluye el bucle ya el tamano de los simbolos es el apropiado
        break
    if len(cadena)//tope <= tope:break   # Mientras el cocienente  sea menor al tope y concluye el bucle
    if tope == 32: break                 # El maximo tamano apropiado para un simbolo y concluye el bucle 
    else: tope *= 2                      # Mientras el cocienente  sea mayor al tope, duplicamos el tope.
           
dic_frecuencias = {}     # Diccionario para guardar la frecuencia de cada símbolo
for i in range(0, len(cadena), tope):   # Recorrer el contenido del archivo
    simbolo = cadena[i:i+tope]          # Obtener el símbolo como una cadena de bytes de 2 bytes
    if simbolo in dic_frecuencias:           # Actualizar la frecuencia del símbolo en el diccionario
        dic_frecuencias[simbolo] += 1
    else:
        dic_frecuencias[simbolo] = 1
if len(dic_frecuencias)==1:
    print("Solo hay un simbolo en el archivo, se interrumpe el script.")
    exit()

# -----------------------------------------[Diccionario de Codigos]-----------------------------------------
def ordenar_Frecuencias(frecuencia):   # Funcion para ordenar los simbolos de acuerdo a sus frecuencias
    diccionario_ordenado = dict(sorted(frecuencia.items(), key = lambda x: x[1])) # Ordena las frecuencias de menor a mayor
    return diccionario_ordenado

dic_frecuencias = ordenar_Frecuencias(dic_frecuencias)  # Diccionario de simbolos/frecuencias

list_frecuencias = list(dic_frecuencias.items())        # Lista de tuplas simbolos/frecuencias


for i in range(len(list_frecuencias)):                  # Crea un BOSQUE DE ARBOLES BINARIOS, los arboles comienzan por nodos
    list_frecuencias[i] = NodoABB(list_frecuencias[i])  # Modifica la lista de tuplas por una de nodos de la clase NodoABB 

while len(list_frecuencias)>=2:      # Crea el arbol a partir de los simbolos de menor frecuencia
    list_frecuencias = crear_Arbol(list_frecuencias) # Cuando solo quedan 2 nodos realiza el arbol completa el arbol  Huffman

dic_frecuencias = preorden_binario(list_frecuencias[0], dic_frecuencias, '') # Recorremos la lista de tuplas, donde el nodo raiz es el [0]


# -----------------------------------------[CODIFICADOR]-----------------------------------------
# Se creaa una lista con las claves del diccionario y  # se accede al último elemento de la lista utilizando el índice -1.
del dic_frecuencias[list(dic_frecuencias.keys())[-1]]   # Se utiliza la instrucción del para eliminar el elemento del diccionario con esa clave

cadena_binaria = ''
for i in range(0, len(cadena), tope):   # Recorrer el contenido del archivo
    llave = cadena[i:i+tope]          # Se concatenan los simbolos codificados en binario
    cadena_binaria +=  dic_frecuencias[llave] # Busca en el diccionario la llave de acuerdo al simbolo

# Rellenar la cadena de bits con ceros a la derecha hasta que tenga una longitud múltiplo de 8 utilizamos '1' como bandera
resto = len(cadena_binaria)%8
if resto != 0:
    cadena_binaria += '1'+('0'*(7-resto))

# A partir de la cadena binaria forma enteros en bloques de 8 simbolos
lista_de_Bytes = [int(cadena_binaria[i:i+8],2) for i in range(0, len(cadena_binaria),8)] 

# Escribir los bytes en el archivo
with open("codificado.huff", "wb") as f:    # Crea el archivo .huff  
    for b in lista_de_Bytes:
        f.write(bytes([b]))  # Lo enteros se escriben en el archivo de forma binaria
    f.close()

fin = time.time()
tiempo_total = fin - inicio
print(f"El programa tardó {tiempo_total} segundos en crear el archivo .huff")


# # -----------------------------------------[DECODIFICADOR]-----------------------------------------
# Abrir el archivo en modo lectura de bytes
with open("codificado.huff", "rb") as f:
    # Leer el contenido del archivo en un objeto bytes
    contenido = f.read()
    f.close()

# Convertir el objeto bytes a una cadena binaria y añadir ceros iniciales
cadena_codificada = ''.join([bin(b)[2:].zfill(8) for b in contenido])

# Quitar el zeroo pading de la cadena
while True:
    if cadena_codificada[-1] == '1': # Se utiliza el primer '1' mas significativo como bandera
        cadena_codificada = cadena_codificada[:-1]
        break
    else:
        cadena_codificada = cadena_codificada[:-1] # Borra todos los '0' de derecha a izquierda 'zero padding'

# Decodificar la cadena de bits utilizando la tabla de códigos Huffman
codigo_temporal = ''
cadena_decodificada = bytes()

# invertir elementos y claves
diccionario_invertido = {valor: clave for clave, valor in dic_frecuencias.items()}

# # Recorre cada bit de la cadena codificada
for bit in cadena_codificada:
    codigo_temporal += bit  # Se crea una cadena temporal para verificar la se enciuentra como llave en el diccionario

    # Si el código temporal está en el diccionario de códigos invertido (es decir, si corresponde a un símbolo decodificado)
    if codigo_temporal in diccionario_invertido.keys():  
        # Obtiene el símbolo correspondiente y lo añade a la cadena decodificada   
        simbolo = diccionario_invertido[codigo_temporal]
        cadena_decodificada += simbolo
        codigo_temporal = ''


# Funcion para verificar si la cadena decodifcada es igual a la cadena antes de codificar para crear el archivo
print(cadena_decodificada == cadena)

# Crea el archivo copia.
with open ("decodificado.bin", 'wb') as f:
    f.write(cadena_decodificada)
    f.close

fin = time.time()
tiempo_total = fin - inicio
print(f"El programa tardó {tiempo_total} segundos.")