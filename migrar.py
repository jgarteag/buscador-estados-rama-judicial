#!/usr/bin/env python3
"""
Script de migración para actualizar todos los archivos buscador.py
a la nueva arquitectura POO.
"""

import os
import sys
from pathlib import Path

# Template del nuevo buscador.py
NUEVO_BUSCADOR_TEMPLATE = '''#!/usr/bin/env python3
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
'''


def es_archivo_antiguo(ruta_archivo):
    """Verifica si un archivo buscador.py es del formato antiguo."""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar si contiene imports del sistema antiguo
        indicadores_antiguos = [
            'import pymongo',
            'import pdfplumber',
            'load_dotenv()',
            'cadena_conexion = f"mongodb+srv',
            'from buscador_rama.search import main'
        ]
        
        return any(indicador in contenido for indicador in indicadores_antiguos)
    
    except Exception as e:
        print(f"Error leyendo {ruta_archivo}: {e}")
        return False


def migrar_archivo(ruta_archivo):
    """Migra un archivo buscador.py al nuevo formato."""
    try:
        # Crear backup
        backup_path = f"{ruta_archivo}.backup"
        if not os.path.exists(backup_path):
            os.rename(ruta_archivo, backup_path)
            print(f"  📋 Backup creado: {backup_path}")
        
        # Escribir nuevo contenido
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(NUEVO_BUSCADOR_TEMPLATE)
        
        print(f"  ✅ Migrado: {ruta_archivo}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error migrando {ruta_archivo}: {e}")
        return False


def main():
    """Función principal del script de migración."""
    print("🚀 Iniciando migración de archivos buscador.py")
    print("=" * 50)
    
    # Obtener directorio raíz del proyecto
    script_dir = Path(__file__).parent
    project_root = script_dir
    
    # Buscar todos los archivos buscador.py
    archivos_buscador = list(project_root.glob("*/buscador.py"))
    
    if not archivos_buscador:
        print("❌ No se encontraron archivos buscador.py")
        return 1
    
    print(f"🔍 Encontrados {len(archivos_buscador)} archivos buscador.py")
    
    migrados = 0
    ya_actualizados = 0
    errores = 0
    
    for archivo in archivos_buscador:
        juzgado = archivo.parent.name
        print(f"\n🏛️  Procesando {juzgado}:")
        
        if es_archivo_antiguo(archivo):
            if migrar_archivo(archivo):
                migrados += 1
            else:
                errores += 1
        else:
            print(f"  ⏭️  Ya está actualizado")
            ya_actualizados += 1
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE MIGRACIÓN:")
    print(f"  ✅ Migrados exitosamente: {migrados}")
    print(f"  ⏭️  Ya actualizados: {ya_actualizados}")
    print(f"  ❌ Errores: {errores}")
    print(f"  📊 Total procesados: {len(archivos_buscador)}")
    
    if errores == 0:
        print("\n🎉 ¡Migración completada exitosamente!")
        return 0
    else:
        print(f"\n⚠️  Migración completada con {errores} errores")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
