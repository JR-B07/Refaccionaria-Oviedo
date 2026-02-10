# 📊 Consolidación de Archivos SQL

**Última actualización**: Febrero 4, 2026

## 📋 Resumen

Todos los archivos SQL del sistema han sido consolidados en **UN ÚNICO ARCHIVO MAESTRO** para simplificar el mantenimiento y evitar inconsistencias.

## 🎯 Archivo Maestro

### `refaccionaria_db.sql`
- **Ubicación**: Raíz del proyecto
- **Tamaño**: 681 líneas
- **Tablas**: 25 tablas principales + índices

Este es el archivo que reemplaza a todos los demás archivos SQL individuales.

## ❌ Archivos Obsoletos (Ya Consolidados)

Los siguientes archivos SQL ya no son necesarios y han sido completamente integrados en el archivo maestro:

| Archivo | Motivo | Contenido Consolidado |
|---------|--------|----------------------|
| `REFACCIONARIA/scripts/create_retiros_caja_table.sql` | Obsoleto | ✅ En `retiros_caja` table |
| `REFACCIONARIA/scripts/create_cierres_caja_table.sql` | Obsoleto | ✅ En `cierres_caja` table |
| `REFACCIONARIA/scripts/create_arqueos_caja_table.sql` | Obsoleto | ✅ En `arqueos_caja` table |
| `REFACCIONARIA/add_retiros_columns.sql` | Obsoleto | ✅ Columnas ya en `arqueos_caja` |
| `REFACCIONARIA/insertar_paquetes.sql` | Obsoleto | ✅ En `paquetes` table (con comentarios) |

## ✅ Contenido Consolidado

### Módulo de Caja
```sql
-- Arqueos de Caja (con campos retiros_*)
CREATE TABLE IF NOT EXISTS arqueos_caja (
    -- Columnas de RETIROS ya consolidadas
    retiros_declarado DECIMAL(12, 2) DEFAULT 0,
    retiros_contado DECIMAL(12, 2) DEFAULT 0,
    diferencia_retiros DECIMAL(12, 2) DEFAULT 0,
    -- + 40+ columnas más con comentarios descriptivos
)

-- Cierres de Caja
CREATE TABLE IF NOT EXISTS cierres_caja (...)

-- Retiros de Caja
CREATE TABLE IF NOT EXISTS retiros_caja (...)
```

### Datos de Ejemplo
- ✅ 10 registros de ejemplo en `retiros_caja` (descomentados)
- ✅ 5 ejemplos de `gastos` (descomentados)
- ✅ 1 ejemplo de `promociones` (descomentado)

### Comentarios Descriptivos
Cada columna incluye comentarios `COMMENT = '...'` para auditoría y documentación:
- Significado del campo
- Rango de valores
- Relaciones y dependencias

## 🔧 Cómo Usar

### Docker Compose
```yaml
volumes:
  - ./init.sql:/docker-entrypoint-initdb.d/init.sql
```

El archivo `init.sql` es idéntico al `refaccionaria_db.sql`, permitiendo:
1. ✅ Inicialización automática del contenedor MySQL
2. ✅ Versionado en Git del archivo maestro
3. ✅ Cambios centralizados

### Ejecución Manual
```bash
# Conectar a MySQL y ejecutar
mysql -u root -p refaccionaria_db < refaccionaria_db.sql

# O desde MySQL CLI
source refaccionaria_db.sql;
```

## 📝 Actualizar la Base de Datos

Si necesitas hacer cambios:

1. **EDITA**: `refaccionaria_db.sql` en la raíz
2. **ACTUALIZA**: `REFACCIONARIA/init.sql` (copia el contenido)
3. **REINICIA**: Docker Compose
   ```bash
   docker-compose down
   docker-compose up -d
   ```

## 🔄 Migración Completada

| Elemento | Antiguo | Nuevo | Estado |
|----------|---------|-------|--------|
| Schema Principal | Fragmentado | `refaccionaria_db.sql` | ✅ Unificado |
| Init Docker | `init.sql` | Idéntico a maestro | ✅ Sincronizado |
| Documentación | Referencias dispersas | Actualizada | ✅ Centralizada |
| Datos Ejemplo | Comentados | Descomentados | ✅ Funcionales |
| Comentarios DB | Parciales | Completos | ✅ Documentado |

## 📌 Referencias en Documentación

Los siguientes documentos han sido actualizados para referenciar el archivo maestro:

- ✅ `QUICK_START_CIERRE.md` - Actualizado
- ✅ `TESTING_CIERRE_CAJA.md` - Actualizado
- ✅ `VISUAL_GUIDE_CIERRE_CAJA.md` - Actualizado
- ✅ `IMPLEMENTACION_ARQUEOS_CAJA.md` - Actualizado
- ✅ `CHECKLIST_ARQUEOS_CAJA.md` - Actualizado

## ⚠️ Notas Importantes

1. **Backup**: Mantén un backup de `refaccionaria_db.sql` antes de hacer cambios
2. **Versionado**: Este archivo será versionado en Git - confirma cambios importantes
3. **Sincronización**: `init.sql` y `refaccionaria_db.sql` deben estar sincronizados
4. **Archivos Antiguos**: Los scripts individuales en `scripts/` pueden ser archivados/eliminados

## 🚀 Próximos Pasos

1. ✅ Eliminar/archivar archivos SQL obsoletos en `REFACCIONARIA/scripts/`
2. ✅ Actualizar cualquier script Python que haga referencia directa a esos archivos
3. ✅ Documentar en el README principal

---

**Resumen**: Un único archivo maestro (`refaccionaria_db.sql`) con 681 líneas que consolida todo el esquema, índices, comentarios y datos iniciales del sistema. 🎯
