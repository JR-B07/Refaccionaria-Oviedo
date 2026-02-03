# Scripts SQL - Información Importante

## ⚠️ ARCHIVOS DEPRECADOS

Los siguientes archivos SQL en este directorio han sido **consolidados** en el archivo principal de la base de datos:

### Archivos Antiguos (Ya no usar)
- ❌ `create_arqueos_caja_table.sql` - Consolidado
- ❌ `create_cierres_caja_table.sql` - Consolidado
- ❌ `create_retiros_caja_table.sql` - Consolidado

### Archivos del Directorio Principal
- ❌ `../add_retiros_columns.sql` - Ya incluido en el esquema principal
- ❌ `../insertar_paquetes.sql` - Datos de ejemplo disponibles en el principal

## ✅ Archivo Único a Usar

**Usar únicamente:** `refaccionaria_db.sql` en la raíz del proyecto

Este archivo contiene:
- ✅ Todas las 25 tablas del sistema
- ✅ Llaves foráneas y relaciones
- ✅ Índices optimizados
- ✅ Datos de ejemplo (comentados)
- ✅ Configuración completa del sistema

## Cómo Inicializar la Base de Datos

```bash
# Opción 1: Desde MySQL CLI
mysql -u root -p < refaccionaria_db.sql

# Opción 2: Desde el cliente MySQL
mysql -u root -p
source /ruta/completa/refaccionaria_db.sql;

# Opción 3: La aplicación crea las tablas automáticamente con SQLAlchemy
python run.py
```

## Estructura Consolidada

El archivo `refaccionaria_db.sql` incluye:

1. **Configuración del Sistema**
2. **Locales/Sucursales**
3. **Usuarios y Autenticación**
4. **Catálogo de Marcas**
5. **Productos e Inventario**
6. **Clientes**
7. **Proveedores**
8. **Ventas y Detalles**
9. **Compras y Detalles**
10. **Traspasos Entre Locales**
11. **Gastos**
12. **Módulo de Caja (Arqueos, Cierres, Retiros)**
13. **Vales de Venta**
14. **Paquetes y Grupos de Productos**
15. **Promociones**
16. **Asistencia de Empleados**
17. **Datos de Ejemplo**

## Mantenimiento

- **NO** ejecutar los scripts individuales de este directorio
- **NO** modificar estos archivos antiguos
- **SÍ** usar y mantener únicamente `refaccionaria_db.sql`
- **SÍ** crear backups regulares de la base de datos

---

Fecha de consolidación: Febrero 2026
