import os
from datetime import date
from typing import List
from ..core.models import ResultadoBusqueda
from ..utils.logger import get_logger

logger = get_logger(__name__)


class FileManager:
    """Gestor de archivos y resultados."""
    
    def __init__(self, carpeta_revision: str):
        """
        Inicializa el gestor con la carpeta de revisión.
        
        Args:
            carpeta_revision: Ruta a la carpeta donde guardar los resultados
        """
        self.carpeta_revision = carpeta_revision
        self._crear_carpeta_si_no_existe()
    
    def _crear_carpeta_si_no_existe(self) -> None:
        """Crea la carpeta de revisión si no existe."""
        if not os.path.exists(self.carpeta_revision):
            os.makedirs(self.carpeta_revision, exist_ok=True)
            logger.info(f"Carpeta de revisión creada: {self.carpeta_revision}")
    
    def get_archivo_revision(self, fecha: date = None) -> str:
        """
        Obtiene la ruta del archivo de revisión para una fecha.
        
        Args:
            fecha: Fecha para el archivo. Si es None, usa la fecha actual.
            
        Returns:
            Ruta completa del archivo de revisión
        """
        if fecha is None:
            fecha = date.today()
        
        nombre_archivo = f'{fecha}_revision.txt'
        return os.path.join(self.carpeta_revision, nombre_archivo)
    
    def escribir_resultado(self, resultado: ResultadoBusqueda) -> None:
        """
        Escribe un resultado de búsqueda al archivo de revisión.
        
        Args:
            resultado: Resultado de la búsqueda a escribir
        """
        archivo_revision = self.get_archivo_revision(resultado.fecha_busqueda)
        
        try:
            with open(archivo_revision, 'a', encoding='utf-8') as archivo:
                archivo.write(str(resultado) + '\n')
                archivo.write('\n')  # Línea en blanco para separar resultados
            
            logger.debug(f"Resultado escrito para {resultado.estado.numero}")
            
        except Exception as e:
            logger.error(f"Error escribiendo resultado: {e}")
            raise
    
    def escribir_resultados(self, resultados: List[ResultadoBusqueda]) -> None:
        """
        Escribe múltiples resultados de búsqueda al archivo.
        
        Args:
            resultados: Lista de resultados a escribir
        """
        if not resultados:
            logger.warning("No hay resultados para escribir")
            return
        
        fecha = resultados[0].fecha_busqueda
        archivo_revision = self.get_archivo_revision(fecha)
        
        try:
            with open(archivo_revision, 'w', encoding='utf-8') as archivo:
                archivo.write(f"=== REVISIÓN DEL {fecha} ===\n\n")
                
                for resultado in resultados:
                    archivo.write(str(resultado) + '\n')
                    archivo.write('\n')
                
                archivo.write(f"\n=== FIN DE REVISIÓN - {len(resultados)} estados procesados ===\n")
            
            logger.info(f"Escritos {len(resultados)} resultados en {archivo_revision}")
            
        except Exception as e:
            logger.error(f"Error escribiendo resultados: {e}")
            raise
    
    def leer_revision(self, fecha: date = None) -> str:
        """
        Lee el contenido de un archivo de revisión.
        
        Args:
            fecha: Fecha del archivo a leer. Si es None, usa la fecha actual.
            
        Returns:
            Contenido del archivo o cadena vacía si no existe
        """
        archivo_revision = self.get_archivo_revision(fecha)
        
        if not os.path.exists(archivo_revision):
            logger.warning(f"Archivo de revisión no encontrado: {archivo_revision}")
            return ""
        
        try:
            with open(archivo_revision, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
            
            logger.debug(f"Archivo de revisión leído: {archivo_revision}")
            return contenido
            
        except Exception as e:
            logger.error(f"Error leyendo archivo de revisión: {e}")
            return ""
    
    def get_archivos_revision(self) -> List[str]:
        """
        Obtiene la lista de archivos de revisión existentes.
        
        Returns:
            Lista de nombres de archivos de revisión
        """
        try:
            archivos = [
                archivo for archivo in os.listdir(self.carpeta_revision)
                if archivo.endswith('_revision.txt')
            ]
            archivos.sort()  # Ordenar por fecha
            return archivos
        
        except Exception as e:
            logger.error(f"Error listando archivos de revisión: {e}")
            return []
