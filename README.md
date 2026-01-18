
# Sistema de Búsqueda de Estados Procesales - Rama Judicial v2.0

## 🎯 Descripción

Sistema modernizado para automatizar la búsqueda de estados procesales emitidos por la rama judicial. Implementado con **Programación Orientada a Objetos (POO)** y **buenas prácticas de desarrollo**.

## 🏗️ Arquitectura

```
buscador-estados-rama-judicial/
├── buscador_estados/          # 📦 Paquete principal
│   ├── core/                  # 🧠 Lógica de negocio
│   │   ├── models.py          # 📊 Modelos de datos
│   │   ├── database.py        # 🗃️ Gestión de MongoDB
│   │   ├── pdf_processor.py   # 📄 Procesamiento de PDFs
│   │   └── file_manager.py    # 📁 Gestión de archivos
│   ├── config/                # ⚙️ Configuraciones
│   │   └── settings.py        # 🔧 Configuración centralizada
│   ├── juzgados/              # 🏛️ Gestión de juzgados
│   │   └── manager.py         # 👨‍💼 Gestor de juzgados
│   └── utils/                 # 🛠️ Utilidades
│       └── logger.py          # 📝 Sistema de logging
├── JUZGADO_NOMBRE/            # 📂 Carpetas de juzgados
│   ├── buscador.py            # 🔍 Script individual
│   ├── pdf/                   # 📄 Archivos PDF
│   └── revision/              # 📋 Resultados
├── main.py                    # 🚀 Punto de entrada principal
├── cli.py                     # 💻 Interfaz de línea de comandos
└── requirements.txt           # 📋 Dependencias
```

## 🚀 Características Principales

### ✨ Mejoras de la v2.0

- **🎯 Programación Orientada a Objetos**: Código organizado en clases especializadas
- **🔧 Configuración Centralizada**: Todas las configuraciones en un solo lugar
- **📝 Sistema de Logging**: Logs detallados para debugging y monitoreo
- **🛡️ Manejo de Errores**: Gestión robusta de excepciones
- **📊 Modelos de Datos**: Estructuras de datos claras y tipadas
- **🔄 Reutilización de Código**: Eliminación de código duplicado
- **🧪 Fácil Testing**: Estructura modular para pruebas
- **📚 Documentación**: Código autodocumentado con docstrings

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/jgarteag/buscador-estados-rama-judicial.git
cd buscador-estados-rama-judicial
```

### 2. Crear entorno virtual
```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```env
USER=tu_usuario_mongodb
PASSWORD=tu_contraseña_mongodb
```

## 🎮 Uso

### 💻 Interfaz de Línea de Comandos (CLI)

#### Listar juzgados disponibles
```bash
python3 cli.py --list
```

#### Procesar un juzgado específico
```bash
python3 cli.py --juzgado JPMCONTADERO
```

#### Procesar todos los juzgados
```bash
python3 cli.py
```

#### Ejecutar con logs detallados
```bash
python3 cli.py --verbose
```

### 🚀 Script Principal

Procesar todos los juzgados automáticamente:
```bash
python3 main.py
```

### 🔍 Scripts Individuales

Ejecutar búsqueda en un juzgado específico:
```bash
cd JPMCONTADERO
python3 buscador.py
```

## 📊 Flujo de Trabajo

1. **📥 Preparación**: Colocar archivos PDF en la carpeta `pdf/` del juzgado
2. **🔍 Ejecución**: Ejecutar el script de búsqueda
3. **📋 Resultados**: Revisar los resultados en la carpeta `revision/`

## 🔧 Configuración

### ⚙️ Variables de Entorno Requeridas

| Variable | Descripción |
|----------|-------------|
| `USER` | Usuario de MongoDB |
| `PASSWORD` | Contraseña de MongoDB |

### 🏛️ Estructura de Juzgados

Cada juzgado debe tener:
```
NOMBRE_JUZGADO/
├── buscador.py    # Script de búsqueda
├── pdf/           # Archivos PDF (entrada)
└── revision/      # Resultados (salida)
```

## 📝 Beneficios de la Nueva Arquitectura

### 🔄 Mantenibilidad
- Código organizado en módulos especializados
- Eliminación de código duplicado
- Fácil localización y corrección de bugs

### 🚀 Escalabilidad
- Fácil agregar nuevos juzgados
- Arquitectura preparada para crecimiento
- Componentes reutilizables

### 🧪 Testabilidad
- Componentes independientes
- Separación clara de responsabilidades
- Fácil creación de tests unitarios

### 🔒 Robustez
- Manejo completo de errores
- Validación de datos y configuraciones
- Logging detallado para debugging
    