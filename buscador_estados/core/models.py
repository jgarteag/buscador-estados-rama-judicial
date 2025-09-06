from dataclasses import dataclass
from typing import List, Optional
from datetime import date


@dataclass
class EstadoProcesal:
    """Modelo para representar un estado procesal."""
    numero: str
    radicado: str
    id: Optional[str] = None


@dataclass
class ResultadoBusqueda:
    """Modelo para representar el resultado de una búsqueda."""
    estado: EstadoProcesal
    archivos_encontrados: List[str]
    fecha_busqueda: date
    
    @property
    def encontrado(self) -> bool:
        """Indica si se encontró el estado en algún archivo."""
        return len(self.archivos_encontrados) > 0
    
    def __str__(self) -> str:
        """Representación en string del resultado."""
        if self.encontrado:
            archivos = ", ".join(self.archivos_encontrados)
            return (f"Se encontró el numero {self.estado.numero} "
                   f"con radicado {self.estado.radicado} "
                   f"en los archivos: {archivos}")
        else:
            return (f"No se encontró el número {self.estado.numero} "
                   f"con radicado {self.estado.radicado} en ningún archivo.")


@dataclass
class ConfiguracionJuzgado:
    """Configuración específica de un juzgado."""
    nombre: str
    carpeta_base: str
    carpeta_pdf: str
    carpeta_revision: str
    coleccion_db: str
