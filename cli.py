#!/usr/bin/env python3
"""
Interfaz de línea de comandos para el sistema de búsqueda de estados procesales.
"""

import argparse
import sys
import os

# Agregar el directorio del proyecto al path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from buscador_estados.juzgados.manager import MultiJuzgadoManager, JuzgadoManager
from buscador_estados.utils.logger import setup_logger

logger = setup_logger('cli')


def crear_parser() -> argparse.ArgumentParser:
    """Crea el parser de argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description='Sistema de Búsqueda de Estados Procesales - Rama Judicial',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s                              # Procesar todos los juzgados
  %(prog)s --juzgado JPMCONTADERO       # Procesar solo un juzgado
  %(prog)s --list                       # Listar juzgados disponibles
  %(prog)s --verbose                    # Ejecutar con logs detallados
        """
    )
    
    parser.add_argument(
        '--juzgado', '-j',
        type=str,
        help='Procesar solo el juzgado especificado'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='Listar todos los juzgados disponibles'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar logs detallados'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Buscador Estados Procesales v2.0.0'
    )
    
    return parser


def listar_juzgados():
    """Lista todos los juzgados disponibles."""
    try:
        juzgados = MultiJuzgadoManager.get_juzgados_disponibles()
        
        if not juzgados:
            print("No se encontraron juzgados configurados.")
            return 1
        
        print("Juzgados disponibles:")
        print("=" * 50)
        for i, juzgado in enumerate(juzgados, 1):
            print(f"{i:2d}. {juzgado}")
        
        print(f"\nTotal: {len(juzgados)} juzgados")
        return 0
        
    except Exception as e:
        logger.error(f"Error listando juzgados: {e}")
        return 1


def procesar_juzgado_especifico(nombre_juzgado: str):
    """Procesa un juzgado específico."""
    try:
        juzgados_disponibles = MultiJuzgadoManager.get_juzgados_disponibles()
        
        if nombre_juzgado not in juzgados_disponibles:
            print(f"Error: Juzgado '{nombre_juzgado}' no encontrado.")
            print("\nJuzgados disponibles:")
            for juzgado in juzgados_disponibles:
                print(f"  - {juzgado}")
            return 1
        
        logger.info(f"Procesando juzgado: {nombre_juzgado}")
        MultiJuzgadoManager.procesar_juzgado(nombre_juzgado)
        
        print(f"✓ Juzgado {nombre_juzgado} procesado exitosamente")
        return 0
        
    except Exception as e:
        logger.error(f"Error procesando juzgado {nombre_juzgado}: {e}")
        print(f"✗ Error procesando juzgado {nombre_juzgado}")
        return 1


def procesar_todos_los_juzgados():
    """Procesa todos los juzgados."""
    try:
        juzgados = MultiJuzgadoManager.get_juzgados_disponibles()
        
        if not juzgados:
            print("No se encontraron juzgados para procesar.")
            return 1
        
        print(f"Procesando {len(juzgados)} juzgados...")
        print("=" * 50)
        
        MultiJuzgadoManager.procesar_todos_los_juzgados()
        
        print("✓ Todos los juzgados procesados exitosamente")
        return 0
        
    except Exception as e:
        logger.error(f"Error procesando juzgados: {e}")
        print("✗ Error procesando juzgados")
        return 1


def main():
    """Función principal de la CLI."""
    parser = crear_parser()
    args = parser.parse_args()
    
    # Configurar nivel de logging
    log_level = 'DEBUG' if args.verbose else 'INFO'
    import logging
    setup_logger('cli', getattr(logging, log_level))
    
    try:
        # Ejecutar comando solicitado
        if args.list:
            return listar_juzgados()
        elif args.juzgado:
            return procesar_juzgado_especifico(args.juzgado)
        else:
            return procesar_todos_los_juzgados()
            
    except KeyboardInterrupt:
        print("\n✗ Proceso interrumpido por el usuario")
        return 1
    except Exception as e:
        logger.error(f"Error crítico: {e}")
        print(f"✗ Error crítico: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
