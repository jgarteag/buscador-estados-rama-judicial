import pandas as pd
import os
from datetime import date
import pdfplumber

RUTA_CARPETA_J1PF = r"C:\Users\juanmgart\Documents\BUSCADOR\J2CMIPIALES"
RUTA_EXCEL = r"C:\Users\juanmgart\OneDrive - Tecnologico de Antioquia Institucion Universitaria\Estados_Mami\estados_mami.xlsx"
SHEET_NAME = "J2CMIPIALES"
CARPETA_PDF = r"C:\Users\juanmgart\Documents\BUSCADOR\J2CMIPIALES\pdf"
CARPETA_REVISION = r"C:\Users\juanmgart\Documents\BUSCADOR\J2CMIPIALES\revision"

# Leer el archivo Excel
df = pd.read_excel(RUTA_EXCEL, sheet_name=SHEET_NAME, dtype={'numero': str, 'radicado': str})

# Iterar sobre cada fila del DataFrame
for index, row in df.iterrows():
    numero = row['numero']
    radicado = row['radicado']  # Obtener el valor de 'radicado'
    found = False
    found_files = []
    # Iterar sobre cada archivo PDF en la carpeta especificada
    for filename in os.listdir(CARPETA_PDF):
        if filename.endswith(".pdf"):
            # Abrir el archivo y leer su contenido
            with pdfplumber.open(os.path.join(CARPETA_PDF, filename)) as pdf:
                content = ""
                for page in pdf.pages:
                    content += page.extract_text()
                # Buscar el número en el contenido del archivo PDF
                if numero in content:
                    found = True
                    found_files.append(filename)
    # Mover los archivos después de cerrar el archivo PDF
    """ if found:
        for found_file in found_files:
            shutil.move(os.path.join(CARPETA_PDF, found_file), os.path.join(CARPETA_RELACION, found_file)) """
    # Escribir la información relevante en un archivo .txt
    with open(os.path.join(CARPETA_REVISION, f'{date.today()}_revision_J2CMIPIALES.txt'), 'a') as txt_file:
        if found:
            txt_file.write(f"Se encontró el número {numero} con radicado {radicado} en los archivos: {', '.join(found_files)}\n")
        else:
            txt_file.write(f"No se encontró el número {numero} con radicado {radicado} en ningún archivo.\n")
        txt_file.write("\n")

# Eliminar los archivos PDF que no contienen el número buscado
""" for filename in os.listdir(CARPETA_PDF):
    if filename.endswith(".pdf"):
        os.remove(os.path.join(CARPETA_PDF, filename)) """