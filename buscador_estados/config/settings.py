import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class Settings:
    """Configuraciones centralizadas del sistema."""
    
    def __init__(self):
        load_dotenv()
        self._validate_environment()
    
    @property
    def mongodb_user(self) -> str:
        """Usuario de MongoDB."""
        return os.getenv("USER", "")
    
    @property
    def mongodb_password(self) -> str:
        """Contraseña de MongoDB."""
        return os.getenv("PASSWORD", "")
    
    @property
    def mongodb_cluster(self) -> str:
        """Cluster de MongoDB."""
        return "clusterestados.iarfl.mongodb.net"
    
    @property
    def mongodb_database(self) -> str:
        """Base de datos de MongoDB."""
        return "dbestados"
    
    @property
    def mongodb_connection_string(self) -> str:
        """Cadena de conexión completa a MongoDB."""
        return (f"mongodb+srv://{self.mongodb_user}:{self.mongodb_password}"
                f"@{self.mongodb_cluster}/?retryWrites=true&w=majority"
                f"&appName=ClusterEstados")
    
    @property
    def proyecto_root(self) -> str:
        """Directorio raíz del proyecto."""
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    @property
    def juzgados_config(self) -> Dict[str, str]:
        """Configuración de carpetas de juzgados."""
        root = self.proyecto_root
        juzgados = {}
        
        # Buscar todas las carpetas que contengan archivos buscador.py
        for item in os.listdir(root):
            item_path = os.path.join(root, item)
            if (os.path.isdir(item_path) and 
                item not in ['buscador_rama', 'buscador_estados', '.git', '__pycache__']):
                buscador_path = os.path.join(item_path, 'buscador.py')
                if os.path.exists(buscador_path):
                    juzgados[item] = item_path
        
        return juzgados
    
    def _validate_environment(self) -> None:
        """Valida que las variables de entorno requeridas estén presentes."""
        required_vars = ['USER', 'PASSWORD']
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(
                f"Variables de entorno faltantes: {', '.join(missing_vars)}"
            )


# Instancia global de configuración
settings = Settings()
