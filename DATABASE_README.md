# 🗄️ Base de Datos - Refaccionaria Oviedo

## Archivo Principal de Base de Datos

**📄 Archivo único:** [`refaccionaria_db.sql`](refaccionaria_db.sql)

Este es el único archivo SQL que debes usar para inicializar o restaurar la base de datos completa del sistema.

## ✅ Contenido Consolidado

El archivo `refaccionaria_db.sql` incluye **TODAS** las definiciones de tablas y datos iniciales:

### Módulos del Sistema

1. **Configuración del Sistema** - Parámetros generales
2. **Locales/Sucursales** - Gestión multi-sucursal
3. **Usuarios** - Autenticación y roles
4. **Catálogo de Productos** - Marcas, productos e inventario
5. **Clientes y Proveedores** - Gestión de relaciones comerciales
6. **Ventas** - Sistema completo de ventas y facturación
7. **Compras** - Gestión de adquisiciones
8. **Traspasos** - Movimientos entre sucursales
9. **Módulo de Caja** - Arqueos, cierres y retiros
10. **Vales de Venta** - Sistema de vales y devoluciones
11. **Paquetes** - Kits y grupos de productos
12. **Promociones** - Sistema de descuentos
13. **Asistencia** - Control de empleados
14. **Gastos** - Registro de gastos operativos

### Total: 25 Tablas Principales

```
configuracion_sistema      locales
usuarios                   marcas
productos                  inventario_local
clientes                   proveedores
ventas                     detalle_ventas
compras                    detalle_compras
traspasos                  detalle_traspasos
gastos                     arqueos_caja
cierres_caja              retiros_caja
vales_venta               paquetes
paquete_productos         grupos
grupo_productos           grupo_aplicaciones
promociones               asistencia_empleados
```

## 🚀 Cómo Usar

### Opción 1: Ejecutar desde línea de comandos

```bash
# Desde la raíz del proyecto
mysql -u root -p < refaccionaria_db.sql
```

### Opción 2: Desde el cliente MySQL

```sql
mysql -u root -p
source /ruta/completa/refaccionaria_db.sql;
```

### Opción 3: Dejar que SQLAlchemy lo maneje

La aplicación creará automáticamente todas las tablas al iniciar:

```bash
python run.py
```

## ⚠️ Archivos Deprecados

Los siguientes archivos SQL **YA NO DEBEN USARSE** (están consolidados):

### En `REFACCIONARIA/scripts/`:
- ❌ `create_arqueos_caja_table.sql`
- ❌ `create_cierres_caja_table.sql`
- ❌ `create_retiros_caja_table.sql`

### En `REFACCIONARIA/`:
- ❌ `add_retiros_columns.sql`
- ❌ `insertar_paquetes.sql`

**Nota:** Estos archivos se mantienen en el repositorio solo como referencia histórica.

## 📝 Características del Esquema

- ✅ Motor InnoDB con soporte transaccional
- ✅ Llaves foráneas con políticas de eliminación apropiadas
- ✅ Índices optimizados para consultas frecuentes
- ✅ Charset UTF-8 para caracteres especiales
- ✅ Campos de auditoría (`fecha_creacion`, `fecha_actualizacion`)
- ✅ Estructura normalizada y escalable

## 🔄 Migración desde Versión Anterior

Si tienes una base de datos antigua con archivos SQL separados:

1. **Hacer backup:**
   ```bash
   mysqldump -u root -p refaccionaria_db > backup_$(date +%Y%m%d).sql
   ```

2. **Eliminar base antigua:**
   ```sql
   DROP DATABASE IF EXISTS refaccionaria_db;
   ```

3. **Crear nueva estructura:**
   ```bash
   mysql -u root -p < refaccionaria_db.sql
   ```

4. **Restaurar datos (si es necesario):**
   ```bash
   mysql -u root -p refaccionaria_db < backup_YYYYMMDD.sql
   ```

## 📊 Datos de Ejemplo

El archivo incluye algunos datos de ejemplo comentados. Para activarlos:

1. Abre `refaccionaria_db.sql`
2. Busca la sección `DATOS DE EJEMPLO`
3. Descomenta los `INSERT` que necesites

## 🛠️ Mantenimiento

### Backup Regular

```bash
# Backup completo
mysqldump -u root -p refaccionaria_db > backup_refaccionaria_$(date +%Y%m%d_%H%M%S).sql

# Solo estructura (sin datos)
mysqldump -u root -p --no-data refaccionaria_db > estructura_refaccionaria.sql

# Solo datos (sin estructura)
mysqldump -u root -p --no-create-info refaccionaria_db > datos_refaccionaria.sql
```

### Ver Estado de la Base

```sql
-- Ver todas las tablas
SHOW TABLES;

-- Ver estructura de una tabla
DESCRIBE nombre_tabla;

-- Ver tamaño de las tablas
SELECT 
    table_name AS 'Tabla',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Tamaño (MB)'
FROM information_schema.TABLES 
WHERE table_schema = 'refaccionaria_db'
ORDER BY (data_length + index_length) DESC;
```

## 📖 Documentación Adicional

- Ver [`REFACCIONARIA/scripts/README_SCRIPTS_SQL.md`](REFACCIONARIA/scripts/README_SCRIPTS_SQL.md) para más detalles sobre la consolidación

## 🆘 Soporte

Si tienes problemas con la base de datos:

1. Verifica que MySQL esté corriendo
2. Comprueba los permisos del usuario
3. Revisa los logs de MySQL
4. Asegúrate de usar el archivo correcto: `refaccionaria_db.sql`

---

**Última actualización:** Febrero 2026  
**Versión del esquema:** 2.0 (Consolidado)
