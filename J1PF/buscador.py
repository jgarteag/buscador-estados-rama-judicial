import os
import pandas as pd
from pymongo import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv
from datetime import date
import pdfplumber

load_dotenv()

username = quote_plus(os.getenv("MONGO_USERNAME"))
password = quote_plus(os.getenv("MONGO_PASSWORD"))

pdf_folder = os.getenv("J1PF_PATH_PDF")
check_folder = os.getenv("J1PF_CHECK_PATH")

MONGODB_URI = f"mongodb+srv://{username}:{password}@clusterestados.iarfl.mongodb.net/?retryWrites=true&w=majority&appName=ClusterEstados"

client = MongoClient(MONGODB_URI)

db = client["dbestados"]
# COLLECTION FOR 'JUZGADO 1 PROMISCUO DE FAMILIA'
collection = db["J1PF"]

data = collection.find()
data_list = list(data)
df = pd.DataFrame(data_list)

for index, row in df.iterrows():
    numero = row['numero']
    radicado = row['radicado'] 
    found = False
    found_files = []
    # Iterar sobre cada archivo PDF en la carpeta especificada
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            # Abrir el archivo y leer su contenido
            with pdfplumber.open(os.path.join(pdf_folder, filename)) as pdf:
                content = ""
                for page in pdf.pages:
                    content += page.extract_text()
                # Buscar el número en el contenido del archivo PDF
                if numero in content:
                    found = True
                    found_files.append(filename)
    
    # Escribir la información relevante en un archivo .txt
    with open(os.path.join(check_folder, f'{date.today()}_revision.txt'), 'a') as txt_file:
        if found:
            txt_file.write(f"Se encontró el numero {numero} con radicado {radicado} en los archivos: {', '.join(found_files)}\n")
        else:
            txt_file.write(f"No se encontro el número {numero} con radicado {radicado} en ningún archivo.\n")
        txt_file.write("\n")

