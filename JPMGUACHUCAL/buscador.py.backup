import os
import pymongo
import pandas as pd
import certifi
import getpass
from datetime import date
import pdfplumber
from dotenv import load_dotenv

load_dotenv()

usuario = os.getenv("USER")
contrasena = os.getenv("PASSWORD")

carpeta_raiz = os.path.dirname(os.path.abspath(__file__))

carpeta_pdf = os.path.join(carpeta_raiz, 'pdf')
carpeta_revision = os.path.join(carpeta_raiz, 'revision')

cadena_conexion = f"mongodb+srv://{usuario}:{contrasena}@clusterestados.iarfl.mongodb.net/?retryWrites=true&w=majority&appName=ClusterEstados"

cliente = pymongo.MongoClient(cadena_conexion, tlsCAFile=certifi.where())

base_datos = cliente.dbestados

nombre_carpeta_raiz = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

coleccion = base_datos[nombre_carpeta_raiz]

datos = coleccion.find()
lista_datos = list(datos)
df = pd.DataFrame(lista_datos)

for indice, fila in df.iterrows():
    numero = fila['numero']
    radicado = fila['radicado'] 
    encontrado = False
    archivos_encontrados = []
    for nombre_archivo in os.listdir(carpeta_pdf):
        if nombre_archivo.endswith(".pdf"):
            with pdfplumber.open(os.path.join(carpeta_pdf, nombre_archivo)) as pdf:
                contenido = ""
                for pagina in pdf.pages:
                    contenido += pagina.extract_text()
                if numero in contenido:
                    encontrado = True
                    archivos_encontrados.append(nombre_archivo)
    
    with open(os.path.join(carpeta_revision, f'{date.today()}_revision.txt'), 'a') as archivo_txt:
        if encontrado:
            archivo_txt.write(f"Se encontró el numero {numero} con radicado {radicado} en los archivos: {', '.join(archivos_encontrados)}\n")
        else:
            archivo_txt.write(f"No se encontro el número {numero} con radicado {radicado} en ningun archivo.\n")
        archivo_txt.write("\n")