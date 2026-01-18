#!/usr/bin/env python3
"""
Punto de entrada principal para el sistema de búsqueda de estados procesales.
"""

import sys
import os

# Agregar el directorio del proyecto al path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from buscador_estados.juzgados.manager import MultiJuzgadoManager
from buscador_estados.utils.logger import setup_logger
from buscador_estados.config.settings import settings

# Configurar logging principal
logger = setup_logger('main')


def main():
    """Función principal del sistema."""
    try:
        logger.info("=== Iniciando Sistema de Búsqueda de Estados Procesales ===")
        
        # Validar configuración
        juzgados = MultiJuzgadoManager.get_juzgados_disponibles()
        if not juzgados:
            logger.error("No se encontraron juzgados configurados")
            return 1
        
        logger.info(f"Juzgados encontrados: {', '.join(juzgados)}")
        
        # Procesar todos los juzgados
        MultiJuzgadoManager.procesar_todos_los_juzgados()
        
        logger.info("=== Procesamiento completado exitosamente ===")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Proceso interrumpido por el usuario")
        return 1
    except Exception as e:
        logger.error(f"Error crítico: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
