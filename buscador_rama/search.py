import os
import pymongo
import pandas as pd
import certifi
from datetime import date
import pdfplumber
from dotenv import load_dotenv

def cargar_credenciales():
    load_dotenv()
    usuario = os.getenv("USER")
    contrasena = os.getenv("PASSWORD")
    return usuario, contrasena

def conectar_mongodb(usuario, contrasena, db_name, collection_name):
    cadena_conexion = f"mongodb+srv://{usuario}:{contrasena}@clusterestados.iarfl.mongodb.net/?retryWrites=true&w=majority&appName=ClusterEstados"
    cliente = pymongo.MongoClient(cadena_conexion, tlsCAFile=certifi.where())
    base_datos = cliente[db_name]
    coleccion = base_datos[collection_name]
    return coleccion

def obtener_dataframe(coleccion):
    datos = coleccion.find()
    lista_datos = list(datos)
    df = pd.DataFrame(lista_datos)
    return df

def buscar_numero_en_pdfs(numero, carpeta_pdf):
    archivos_encontrados = []
    for nombre_archivo in os.listdir(carpeta_pdf):
        if nombre_archivo.endswith(".pdf"):
            with pdfplumber.open(os.path.join(carpeta_pdf, nombre_archivo)) as pdf:
                contenido = ""
                for pagina in pdf.pages:
                    contenido += pagina.extract_text()
                if numero in contenido:
                    archivos_encontrados.append(nombre_archivo)
    return archivos_encontrados

def escribir_resultado(carpeta_revision, numero, radicado, archivos_encontrados):
    ruta_archivo = os.path.join(carpeta_revision, f'{date.today()}_revision.txt')
    with open(ruta_archivo, 'a') as archivo_txt:
        if archivos_encontrados:
            archivo_txt.write(f"Se encontró el numero {numero} con radicado {radicado} en los archivos: {', '.join(archivos_encontrados)}\n")
        else:
            archivo_txt.write(f"No se encontro el número {numero} con radicado {radicado} en ningun archivo.\n")
        archivo_txt.write("\n")

def main():
    usuario, contrasena = cargar_credenciales()
    carpeta_raiz = os.path.dirname(os.path.abspath(__file__))
    carpeta_pdf = os.path.join(carpeta_raiz, 'pdf')
    carpeta_revision = os.path.join(carpeta_raiz, 'revision')
    nombre_carpeta_raiz = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    coleccion = conectar_mongodb(usuario, contrasena, "dbestados", nombre_carpeta_raiz)
    df = obtener_dataframe(coleccion)
    for _, fila in df.iterrows():
        numero = fila['numero']
        radicado = fila['radicado']
        archivos_encontrados = buscar_numero_en_pdfs(numero, carpeta_pdf)
        escribir_resultado(carpeta_revision, numero, radicado, archivos_encontrados)
