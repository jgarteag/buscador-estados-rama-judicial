#!/usr/bin/env python3
"""
Script para actualizar todos los archivos buscador.py con el nuevo template.
"""

import os
import shutil

# Contenido del nuevo template
template_content = '''#!/usr/bin/env python3
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

def main():
    """Actualiza todos los archivos buscador.py."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Buscar todas las carpetas de juzgados
    juzgados_actualizados = 0
    
    for item in os.listdir(project_root):
        item_path = os.path.join(project_root, item)
        
        # Verificar si es una carpeta de juzgado
        if (os.path.isdir(item_path) and 
            item not in ['buscador_rama', 'buscador_estados', '.git', '__pycache__']):
            
            buscador_path = os.path.join(item_path, 'buscador.py')
            
            if os.path.exists(buscador_path):
                # Crear backup del archivo original
                backup_path = buscador_path + '.backup'
                if not os.path.exists(backup_path):
                    shutil.copy2(buscador_path, backup_path)
                    print(f"Backup creado: {backup_path}")
                
                # Escribir el nuevo contenido
                with open(buscador_path, 'w', encoding='utf-8') as f:
                    f.write(template_content)
                
                print(f"✓ Actualizado: {buscador_path}")
                juzgados_actualizados += 1
    
    print(f"\nActualizados {juzgados_actualizados} archivos buscador.py")
    print("Los archivos originales se guardaron como .backup")

if __name__ == "__main__":
    main()
