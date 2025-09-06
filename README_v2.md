# Buscador de Estados Procesales - Rama Judicial

Sistema automatizado para la búsqueda de estados procesales en documentos PDF usando programación orientada a objetos y buenas prácticas de desarrollo.

## 🏗️ Arquitectura

El proyecto ha sido completamente reestructurado usando **Programación Orientada a Objetos** con las siguientes mejoras:

### Estructura del Proyecto

```
buscador-estados-rama-judicial/
├── buscador_estados/           # Módulo principal del sistema
│   ├── core/                   # Funcionalidades centrales
│   │   ├── models.py          # Modelos de datos (EstadoProcesal, ResultadoBusqueda)
│   │   ├── database.py        # Gestión de conexiones MongoDB
│   │   ├── pdf_processor.py   # Procesamiento de archivos PDF
│   │   └── file_manager.py    # Gestión de archivos y resultados
│   ├── config/                # Configuraciones
│   │   └── settings.py        # Configuraciones centralizadas
│   ├── juzgados/             # Gestión de juzgados
│   │   └── manager.py        # Lógica de negocio principal
│   └── utils/                # Utilidades
│       └── logger.py         # Sistema de logging
├── main.py                   # Punto de entrada principal
├── cli.py                    # Interfaz de línea de comandos
└── [JUZGADO]/               # Carpetas de juzgados
    ├── buscador.py          # Script simplificado para cada juzgado
    ├── pdf/                 # Archivos PDF a procesar
    └── revision/            # Resultados de las búsquedas
```

### Principios Aplicados

- **Single Responsibility Principle**: Cada clase tiene una responsabilidad específica
- **Open/Closed Principle**: Fácil extensión sin modificar código existente
- **Dependency Injection**: Configuraciones centralizadas y flexibles
- **Error Handling**: Manejo robusto de errores con logging detallado
- **Type Hints**: Código más legible y mantenible

## 🚀 Instalación

```bash
git clone https://github.com/jgarteag/buscador-estados-rama-judicial
cd buscador-estados-rama-judicial
pip install -r requirements.txt
```

## ⚙️ Configuración

1. **Variables de Entorno**: Crear archivo `.env` con credenciales de MongoDB:
```env
USER=tu_usuario_mongodb
PASSWORD=tu_password_mongodb
```

2. **Estructura de Juzgados**: Cada juzgado debe tener:
   - Carpeta `pdf/` con los archivos PDF a procesar
   - Carpeta `revision/` para resultados (se crea automáticamente)
   - Archivo `buscador.py` (ya actualizado automáticamente)

## 📖 Uso

### Opción 1: Procesar Todos los Juzgados

```bash
python main.py
```

### Opción 2: Interfaz de Línea de Comandos

```bash
# Listar juzgados disponibles
python cli.py --list

# Procesar un juzgado específico
python cli.py --juzgado JPMCONTADERO

# Procesar todos con logs detallados
python cli.py --verbose
```

### Opción 3: Juzgado Individual

```bash
cd JPMCONTADERO
python buscador.py
```

## 🔧 Principales Mejoras

### 1. **Eliminación de Código Duplicado**
- **Antes**: Cada juzgado tenía su propio código completo
- **Ahora**: Código centralizado con configuración automática

### 2. **Programación Orientada a Objetos**
```python
# Clases principales:
- EstadoProcesal: Modelo de datos
- ResultadoBusqueda: Resultado de búsquedas
- DatabaseManager: Gestión de MongoDB
- PDFProcessor: Procesamiento de PDFs
- JuzgadoManager: Lógica de negocio
```

### 3. **Configuración Centralizada**
```python
# settings.py maneja toda la configuración
- Conexiones a MongoDB
- Rutas de archivos
- Variables de entorno
- Detección automática de juzgados
```

### 4. **Sistema de Logging**
```python
# Logs estructurados con diferentes niveles
logger.info("Información general")
logger.debug("Detalles de depuración")
logger.error("Errores con stack trace")
```

### 5. **Manejo de Errores Robusto**
```python
# Context managers para recursos
with DatabaseManager() as db:
    estados = db.get_estados_procesales(juzgado)

# Validaciones y recuperación de errores
try:
    manager.ejecutar_revision_completa()
except Exception as e:
    logger.error(f"Error: {e}")
    # Continúa con siguiente juzgado
```

## 🎯 Funcionalidades

### Búsqueda Inteligente
- Extracción de texto optimizada de PDFs
- Búsqueda precisa por número de estado
- Soporte para múltiples archivos PDF

### Resultados Estructurados
- Archivos de revisión con formato mejorado
- Timestamps y estadísticas
- Backup automático de configuraciones

### Escalabilidad
- Fácil adición de nuevos juzgados
- Configuración automática
- Procesamiento paralelo futuro

## 📊 Ejemplo de Salida

```
=== REVISIÓN DEL 2025-09-06 ===

Se encontró el numero 12345 con radicado ABC123 en los archivos: estados_mayo.pdf
No se encontró el número 67890 con radicado XYZ456 en ningún archivo.

=== FIN DE REVISIÓN - 2 estados procesados ===
```

## 🔄 Migración desde la Versión Anterior

La migración es **automática**:

1. ✅ Archivos originales respaldados como `.backup`
2. ✅ Nuevos archivos `buscador.py` generados automáticamente
3. ✅ Configuración detectada automáticamente
4. ✅ Misma funcionalidad, mejor estructura

## 🛠️ Mantenimiento

### Agregar Nuevo Juzgado
1. Crear carpeta con nombre del juzgado
2. Crear subcarpetas `pdf/` y `revision/`
3. Copiar `buscador_template.py` como `buscador.py`
4. El sistema lo detectará automáticamente

### Debugging
```bash
python cli.py --verbose  # Logs detallados
```

### Extensibilidad
- Nuevos formatos: Extender `PDFProcessor`
- Nuevas bases de datos: Extender `DatabaseManager`  
- Nuevos reportes: Extender `FileManager`

## 🔐 Seguridad

- Variables de entorno para credenciales
- Validación de rutas y archivos
- Manejo seguro de conexiones
- Logs sin información sensible

---

**Autor**: Juan Gart  
**Versión**: 2.0.0  
**Licencia**: Ver LICENSE
