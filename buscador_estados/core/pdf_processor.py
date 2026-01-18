import os
import pdfplumber
from typing import List, Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)


class PDFProcessor:
    """Procesador de archivos PDF para búsqueda de texto."""
    
    def __init__(self, carpeta_pdf: str):
        """
        Inicializa el procesador con la carpeta de PDFs.
        
        Args:
            carpeta_pdf: Ruta a la carpeta que contiene los PDFs
        """
        self.carpeta_pdf = carpeta_pdf
        self._validar_carpeta()
    
    def _validar_carpeta(self) -> None:
        """Valida que la carpeta de PDFs exista."""
        if not os.path.exists(self.carpeta_pdf):
            raise FileNotFoundError(f"Carpeta PDF no encontrada: {self.carpeta_pdf}")
        
        if not os.path.isdir(self.carpeta_pdf):
            raise NotADirectoryError(f"La ruta no es una carpeta: {self.carpeta_pdf}")
    
    def get_pdf_files(self) -> List[str]:
        """
        Obtiene la lista de archivos PDF en la carpeta.
        
        Returns:
            Lista de nombres de archivos PDF
        """
        try:
            archivos = [
                archivo for archivo in os.listdir(self.carpeta_pdf)
                if archivo.lower().endswith('.pdf')
            ]
            logger.info(f"Encontrados {len(archivos)} archivos PDF en {self.carpeta_pdf}")
            return archivos
        except Exception as e:
            logger.error(f"Error listando archivos PDF: {e}")
            return []
    
    def extract_text_from_pdf(self, nombre_archivo: str) -> Optional[str]:
        """
        Extrae todo el texto de un archivo PDF.
        
        Args:
            nombre_archivo: Nombre del archivo PDF
            
        Returns:
            Texto extraído del PDF o None si hay error
        """
        ruta_archivo = os.path.join(self.carpeta_pdf, nombre_archivo)
        
        try:
            with pdfplumber.open(ruta_archivo) as pdf:
                contenido = ""
                for pagina in pdf.pages:
                    texto_pagina = pagina.extract_text()
                    if texto_pagina:
                        contenido += texto_pagina + "\n"
                
                logger.debug(f"Texto extraído de {nombre_archivo}: {len(contenido)} caracteres")
                return contenido
                
        except Exception as e:
            logger.error(f"Error extrayendo texto de {nombre_archivo}: {e}")
            return None
    
    def search_text_in_pdf(self, nombre_archivo: str, texto_busqueda: str) -> bool:
        """
        Busca un texto específico en un archivo PDF.
        
        Args:
            nombre_archivo: Nombre del archivo PDF
            texto_busqueda: Texto a buscar
            
        Returns:
            True si se encuentra el texto, False en caso contrario
        """
        contenido = self.extract_text_from_pdf(nombre_archivo)
        
        if contenido is None:
            return False
        
        encontrado = texto_busqueda in contenido
        logger.debug(f"Búsqueda de '{texto_busqueda}' en {nombre_archivo}: {'encontrado' if encontrado else 'no encontrado'}")
        
        return encontrado
    
    def search_text_in_all_pdfs(self, texto_busqueda: str) -> List[str]:
        """
        Busca un texto en todos los archivos PDF de la carpeta.
        
        Args:
            texto_busqueda: Texto a buscar
            
        Returns:
            Lista de nombres de archivos donde se encontró el texto
        """
        archivos_pdf = self.get_pdf_files()
        archivos_encontrados = []
        
        logger.info(f"Buscando '{texto_busqueda}' en {len(archivos_pdf)} archivos PDF")
        
        for archivo in archivos_pdf:
            if self.search_text_in_pdf(archivo, texto_busqueda):
                archivos_encontrados.append(archivo)
        
        logger.info(f"Texto encontrado en {len(archivos_encontrados)} archivos")
        return archivos_encontrados
