import os
from datetime import date
from typing import List, Optional
from ..core.models import ConfiguracionJuzgado, EstadoProcesal, ResultadoBusqueda
from ..core.database import DatabaseManager
from ..core.pdf_processor import PDFProcessor
from ..core.file_manager import FileManager
from ..config.settings import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class JuzgadoManager:
    """Gestor principal para operaciones de un juzgado específico."""
    
    def __init__(self, nombre_juzgado: str):
        """
        Inicializa el gestor para un juzgado específico.
        
        Args:
            nombre_juzgado: Nombre del juzgado
        """
        self.nombre_juzgado = nombre_juzgado
        self.config = self._crear_configuracion()
        self.pdf_processor = PDFProcessor(self.config.carpeta_pdf)
        self.file_manager = FileManager(self.config.carpeta_revision)
        
    def _crear_configuracion(self) -> ConfiguracionJuzgado:
        """Crea la configuración del juzgado."""
        juzgados_config = settings.juzgados_config
        
        if self.nombre_juzgado not in juzgados_config:
            raise ValueError(f"Juzgado no encontrado: {self.nombre_juzgado}")
        
        carpeta_base = juzgados_config[self.nombre_juzgado]
        
        return ConfiguracionJuzgado(
            nombre=self.nombre_juzgado,
            carpeta_base=carpeta_base,
            carpeta_pdf=os.path.join(carpeta_base, 'pdf'),
            carpeta_revision=os.path.join(carpeta_base, 'revision'),
            coleccion_db=self.nombre_juzgado
        )
    
    def validar_estructura(self) -> bool:
        """
        Valida que la estructura de carpetas del juzgado sea correcta.
        
        Returns:
            True si la estructura es válida
        """
        carpetas_requeridas = [
            self.config.carpeta_base,
            self.config.carpeta_pdf,
            self.config.carpeta_revision
        ]
        
        for carpeta in carpetas_requeridas:
            if not os.path.exists(carpeta):
                logger.error(f"Carpeta faltante: {carpeta}")
                return False
        
        # Verificar que exista al menos un PDF
        archivos_pdf = self.pdf_processor.get_pdf_files()
        if not archivos_pdf:
            logger.warning(f"No se encontraron archivos PDF en {self.config.carpeta_pdf}")
            return False
        
        logger.info(f"Estructura válida para {self.nombre_juzgado}")
        return True
    
    def obtener_estados_procesales(self) -> List[EstadoProcesal]:
        """
        Obtiene los estados procesales desde la base de datos.
        
        Returns:
            Lista de estados procesales
        """
        with DatabaseManager() as db:
            estados = db.get_estados_procesales(self.config.coleccion_db)
            logger.info(f"Obtenidos {len(estados)} estados para {self.nombre_juzgado}")
            return estados
    
    def procesar_estado(self, estado: EstadoProcesal) -> ResultadoBusqueda:
        """
        Procesa un estado procesal específico.
        
        Args:
            estado: Estado procesal a procesar
            
        Returns:
            Resultado de la búsqueda
        """
        archivos_encontrados = self.pdf_processor.search_text_in_all_pdfs(estado.numero)
        
        resultado = ResultadoBusqueda(
            estado=estado,
            archivos_encontrados=archivos_encontrados,
            fecha_busqueda=date.today()
        )
        
        logger.debug(f"Procesado estado {estado.numero}: {len(archivos_encontrados)} archivos")
        return resultado
    
    def procesar_todos_los_estados(self) -> List[ResultadoBusqueda]:
        """
        Procesa todos los estados procesales del juzgado.
        
        Returns:
            Lista de resultados de búsqueda
        """
        logger.info(f"Iniciando procesamiento para {self.nombre_juzgado}")
        
        if not self.validar_estructura():
            raise RuntimeError(f"Estructura inválida para {self.nombre_juzgado}")
        
        estados = self.obtener_estados_procesales()
        if not estados:
            logger.warning(f"No se encontraron estados para procesar en {self.nombre_juzgado}")
            return []
        
        resultados = []
        for estado in estados:
            try:
                resultado = self.procesar_estado(estado)
                resultados.append(resultado)
            except Exception as e:
                logger.error(f"Error procesando estado {estado.numero}: {e}")
                # Crear resultado con error
                resultado = ResultadoBusqueda(
                    estado=estado,
                    archivos_encontrados=[],
                    fecha_busqueda=date.today()
                )
                resultados.append(resultado)
        
        logger.info(f"Procesamiento completo para {self.nombre_juzgado}: {len(resultados)} resultados")
        return resultados
    
    def ejecutar_revision_completa(self) -> None:
        """Ejecuta una revisión completa y guarda los resultados."""
        try:
            resultados = self.procesar_todos_los_estados()
            
            if resultados:
                self.file_manager.escribir_resultados(resultados)
                
                # Estadísticas detalladas
                encontrados = sum(1 for r in resultados if r.encontrado)
                total = len(resultados)
                porcentaje = (encontrados / total * 100) if total > 0 else 0
                
                logger.info(f"Revisión completa para {self.nombre_juzgado}: "
                          f"{encontrados}/{total} estados encontrados ({porcentaje:.1f}%)")
                
                # Mostrar resumen de estados encontrados
                if encontrados > 0:
                    logger.info(f"✅ Estados encontrados en PDFs:")
                    for resultado in resultados:
                        if resultado.encontrado:
                            archivos = ", ".join(resultado.archivos_encontrados)
                            logger.info(f"   • {resultado.estado.numero} ({resultado.estado.radicado}) → {archivos}")
                else:
                    logger.info("❌ No se encontraron estados en los archivos PDF")
                    
            else:
                logger.warning(f"No se generaron resultados para {self.nombre_juzgado}")
                
        except Exception as e:
            logger.error(f"Error en revisión completa para {self.nombre_juzgado}: {e}")
            raise


class MultiJuzgadoManager:
    """Gestor para operaciones con múltiples juzgados."""
    
    @staticmethod
    def get_juzgados_disponibles() -> List[str]:
        """
        Obtiene la lista de juzgados disponibles.
        
        Returns:
            Lista de nombres de juzgados
        """
        return list(settings.juzgados_config.keys())
    
    @staticmethod
    def procesar_juzgado(nombre_juzgado: str) -> None:
        """
        Procesa un juzgado específico.
        
        Args:
            nombre_juzgado: Nombre del juzgado a procesar
        """
        manager = JuzgadoManager(nombre_juzgado)
        manager.ejecutar_revision_completa()
    
    @staticmethod
    def procesar_todos_los_juzgados() -> None:
        """Procesa todos los juzgados disponibles."""
        juzgados = MultiJuzgadoManager.get_juzgados_disponibles()
        logger.info(f"Procesando {len(juzgados)} juzgados")
        
        exitosos = 0
        fallidos = 0
        
        for juzgado in juzgados:
            try:
                logger.info(f"Procesando juzgado: {juzgado}")
                MultiJuzgadoManager.procesar_juzgado(juzgado)
                exitosos += 1
            except Exception as e:
                logger.error(f"Error procesando {juzgado}: {e}")
                fallidos += 1
        
        logger.info(f"Procesamiento completo: {exitosos} exitosos, {fallidos} fallidos")
