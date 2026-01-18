import pymongo
import pandas as pd
import certifi
from typing import List, Optional
from ..core.models import EstadoProcesal
from ..config.settings import settings


class DatabaseManager:
    """Gestor de conexiones y operaciones con MongoDB."""
    
    def __init__(self):
        self._client: Optional[pymongo.MongoClient] = None
        self._db = None
    
    def connect(self) -> None:
        """Establece conexión con MongoDB."""
        try:
            self._client = pymongo.MongoClient(
                settings.mongodb_connection_string,
                tlsCAFile=certifi.where()
            )
            self._db = self._client[settings.mongodb_database]
            # Verificar conexión
            self._client.admin.command('ping')
        except Exception as e:
            raise ConnectionError(f"Error conectando a MongoDB: {e}")
    
    def disconnect(self) -> None:
        """Cierra la conexión con MongoDB."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
    
    def get_estados_procesales(self, coleccion_nombre: str) -> List[EstadoProcesal]:
        """
        Obtiene los estados procesales de una colección específica.
        
        Args:
            coleccion_nombre: Nombre de la colección en MongoDB
            
        Returns:
            Lista de estados procesales
        """
        if self._db is None:
            raise ConnectionError("No hay conexión a la base de datos")
        
        try:
            coleccion = self._db[coleccion_nombre]
            datos = coleccion.find()
            lista_datos = list(datos)
            
            if not lista_datos:
                return []
            
            df = pd.DataFrame(lista_datos)
            estados = []
            
            for _, fila in df.iterrows():
                estado = EstadoProcesal(
                    numero=str(fila.get('numero', '')),
                    radicado=str(fila.get('radicado', '')),
                    id=str(fila.get('_id', '')) if '_id' in fila else None
                )
                estados.append(estado)
            
            return estados
            
        except Exception as e:
            raise RuntimeError(f"Error obteniendo estados de {coleccion_nombre}: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
