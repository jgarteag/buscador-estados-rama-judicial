#!/usr/bin/env python3
"""
Buscador para juzgado específico usando el nuevo sistema.
"""

import sys
import os

# Agregar el directorio del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from buscador_estados.juzgados.manager import JuzgadoManager
from buscador_estados.utils.logger import setup_logger

# Obtener el nombre del juzgado desde el nombre de la carpeta
nombre_juzgado = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

logger = setup_logger(f'buscador_{nombre_juzgado}')


def main():
    """Función principal del buscador."""
    try:
        logger.info(f"Iniciando búsqueda para {nombre_juzgado}")
        
        manager = JuzgadoManager(nombre_juzgado)
        manager.ejecutar_revision_completa()
        
        logger.info(f"Búsqueda completada para {nombre_juzgado}")
        print(f"✓ Revisión completada para {nombre_juzgado}")
        print(f"  Resultados guardados en: {manager.config.carpeta_revision}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error en búsqueda para {nombre_juzgado}: {e}")
        print(f"✗ Error en la búsqueda: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
