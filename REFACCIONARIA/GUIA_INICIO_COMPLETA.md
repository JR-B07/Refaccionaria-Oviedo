# Refaccionaria ERP - Guía de Inicio

## Descripción
Sistema ERP completo para la gestión de refacciones automotrices. Incluye:
- Gestión de inventario de productos
- Sistema de paquetes (kits) de reparación
- Control de sucursales
- Arqueos de caja
- Sistema de usuarios

## Requisitos del Sistema
- Windows 10 o superior
- Python 3.8 o superior
- MySQL 5.7 o superior (instalado y configurado como servicio)
- Permiso de Administrador (recomendado)

## Instalación

### 1. Requisitos Previos
```bash
# Verificar Python
python --version

# Verificar MySQL está instalado
mysql --version

# Asegurar que MySQL está como servicio de Windows
# Abrir Services.msc y verificar "MySQL" o "MySQL80"
```

### 2. Instalación de Dependencias
```bash
pip install -r requirements.txt
```

O instalará automáticamente al iniciar cualquier launcher.

### 3. Configuración de Base de Datos
Se crea automáticamente con el archivo `.env`. Por defecto:
- Host: localhost
- Usuario: root
- Contraseña: root
- Base de datos: refaccionaria_db

## Iniciadores de Aplicación

### Opción 1: Launcher Avanzado (RECOMENDADO)
**Archivo:** `Refaccionaria.bat`

Características:
- ✅ Verificación automática de dependencias
- ✅ Inicialización automática de base de datos
- ✅ Comprobación de puertos
- ✅ Interfaz amigable
- ✅ Manejo de errores robusto

```bash
Refaccionaria.bat
```

### Opción 2: Servidor API Solo
**Archivo:** `start.bat`

Características:
- API FastAPI en http://127.0.0.1:8001
- Acceso a documentación en /docs
- Para desarrollo o integración con clientes

```bash
start.bat
```

### Opción 3: Inicio Rápido Browser
**Archivo:** `InicioRapido.bat`

Características:
- Abre la aplicación en el navegador predeterminado
- Más ligero que la versión desktop

```bash
InicioRapido.bat
```

### Opción 4: Launcher Avanzado Python
**Archivo:** `advanced_launcher.py`

Características:
- Verificación exhaustiva de dependencias
- Inicialización automática completa
- Salida con colores
- Reporte detallado

```bash
python advanced_launcher.py
```

## Verificación del Sistema

Para diagnosticar problemas, ejecuta:
```bash
python diagnostico.py
```

Este script verificará:
- ✅ Versión de Python
- ✅ Dependencias instaladas
- ✅ Conexión a MySQL
- ✅ Estado de la base de datos
- ✅ Estructura del proyecto
- ✅ Disponibilidad de puertos

## Acceso a la Aplicación

### Desktop (GUI)
- Ejecuta: `Refaccionaria.bat`
- Se abrirá automáticamente una ventana de aplicación

### Web Browser
- Ejecuta: `start.bat` o `InicioRapido.bat`
- Accede a: `http://127.0.0.1:8001`

### API REST
- Base URL: `http://127.0.0.1:8001`
- Documentación interactiva: `http://127.0.0.1:8001/docs`
- Usuario predeterminado: `admin`
- Contraseña predeterminada: `admin`

## Estructura de Carpetas

```
REFACCIONARIA/
├── Refaccionaria.bat           # Launcher principal (RECOMENDADO)
├── start.bat                   # Launcher servidor API
├── InicioRapido.bat            # Launcher browser
├── advanced_launcher.py        # Launcher avanzado Python
├── diagnostico.py              # Script de diagnóstico
├── launch_desktop.py           # Launcher de escritorio
├── start.py                    # Servidor uvicorn
├── requirements.txt            # Dependencias Python
├── .env                        # Configuración (creado automáticamente)
├── app/
│   ├── main.py                 # API FastAPI
│   ├── models.py               # Modelos de datos
│   ├── database.py             # Configuración de BD
│   └── static/                 # Archivos HTML/CSS/JS
├── scripts/
│   ├── inicializar_datos.py   # Inicializador de BD
│   ├── cargar_productos.py    # Cargador de productos
│   └── cargar_paquetes.py     # Cargador de paquetes
└── logs/                       # Archivos de registro
```

## Solución de Problemas

### MySQL no inicia
```bash
# Verificar servicio
sc query MySQL

# Iniciar manualmente
net start MySQL

# Si no existe, verificar:
# - MySQL está instalado
# - El servicio está configurado en Windows
```

### Puerto 8001 ya en uso
```bash
# Encontrar proceso usando puerto
netstat -ano | find "8001"

# Matar proceso (cambiar PID)
taskkill /PID xxxx /F

# O cambiar puerto en .env
PORT=8002
```

### Base de datos no existe
```bash
# Recrear base de datos
python scripts/inicializar_datos.py

# O ejecutar:
diagnostico.py
```

### Dependencias faltantes
```bash
# Reinstalar
pip install -r requirements.txt

# O ejecutar el launcher que las instala automáticamente
```

## Funciones Principales

### Gestión de Productos
- Listar, crear, actualizar y eliminar productos
- Búsqueda y filtrado avanzado
- Control de inventario
- Seguimiento de precios

### Gestión de Paquetes (Kits)
- Crear paquetes de reparación
- Asignar productos a paquetes
- Gestionar contenido de kits
- Reportes de paquetes

### Control de Sucursales
- Gestión multi-sucursal
- Transferencia de inventario
- Reportes por sucursal

### Arqueos de Caja
- Registro de entradas/salidas
- Conciliación diaria
- Reportes de caja

## Logs y Debugging

Los logs se guardan en:
- `logs/` - Carpeta de registros de aplicación
- `server.log` - Log del último servidor ejecutado

Para ver logs en tiempo real:
```bash
# Windows
tail -f server.log

# O abrir en editor
notepad server.log
```

## API REST Endpoints Principales

```
GET    /api/productos           # Listar productos
POST   /api/productos           # Crear producto
GET    /api/productos/{id}      # Obtener producto
PUT    /api/productos/{id}      # Actualizar producto
DELETE /api/productos/{id}      # Eliminar producto

GET    /api/paquetes            # Listar paquetes
POST   /api/paquetes            # Crear paquete
GET    /api/paquetes/{id}       # Obtener paquete
```

Documentación completa disponible en: `http://127.0.0.1:8001/docs`

## Comandos Útiles

```bash
# Ver versión de Python
python --version

# Ver versión de MySQL
mysql --version

# Verificar puerto disponible
netstat -ano | find "8001"

# Ver procesos Python
tasklist | find "python"

# Matar proceso
taskkill /PID xxxx /F

# Ver logs
type server.log
tail -f server.log
```

## Soporte

Para reportar problemas o sugerencias:
1. Ejecutar `diagnostico.py` y guardar salida
2. Revisar `server.log` para errores
3. Contactar al desarrollador con la información

## Actualización

```bash
# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Limpiar base de datos (CUIDADO - borra datos)
python scripts/limpiar_db.py

# Reinicializar con datos por defecto
python scripts/inicializar_datos.py
```

## Notas Importantes

- ⚠️ **Permisos de Administrador**: Recomendado para iniciar/detener servicios MySQL
- ⚠️ **Puerto 8001**: Debe estar disponible y no bloqueado por firewall
- ⚠️ **MySQL**: Debe estar corriendo antes de iniciar la aplicación
- ⚠️ **Datos**: Los datos se guardan en MySQL, no en archivos locales
- ℹ️ **Primeros datos**: Se cargan automáticamente en primer uso

## Versión
**Refaccionaria ERP v1.0**
Última actualización: 4 de Febrero 2026

---

¡Gracias por usar Refaccionaria ERP!
