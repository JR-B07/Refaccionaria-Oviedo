# 📋 GUÍA RÁPIDA DE ACCESO AL SISTEMA

## ✅ Estado Actual

- **Base de datos**: MySQL en Laragon (refaccionaria_db)
- **API**: FastAPI en `http://localhost:8000`
- **Estado de conexión**: ✅ Funcionando
- **Usuarios**: 4 perfiles creados

---

## 🔐 Credenciales de Acceso

### Perfiles Disponibles:

| Usuario | Contraseña | Rol | Email |
|---------|-----------|-----|-------|
| **admin** | admin | administrador | admin@refaccionaria.local |
| **sucursal1** | sucursal1 | gerente | gerente1@refaccionaria.com |
| **sucursal2** | sucursal2 | gerente | gerente2@refaccionaria.com |
| **almacenero** | almacen123 | almacenista | almacenero@refaccionaria.com |

---

## 🚀 Cómo Iniciar el Sistema

### Paso 1: Iniciar Laragon (MySQL)
```
C:\laragon\laragon.exe
```
Haz clic en **"Start All"** y espera que ambos servicios estén verdes ✅

### Paso 2: Iniciar la API (en terminal dentro de REFACCIONARIA)
```bash
python run.py
# o
python start.py
```

La API estará disponible en:
- 🌐 Interfaz: `http://localhost:8000`
- 📚 Documentación Swagger: `http://localhost:8000/docs`
- 📘 ReDoc: `http://localhost:8000/redoc`

---

## 🔧 Configuración de Conexión

**Archivo: `.env`**
```
MYSQL_SERVER=localhost
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DB=refaccionaria_db
MYSQL_PORT=3306
```

---

## ❓ Si Hay Errores de Conexión

### Error: "Access denied for user 'root'@'localhost'"
**Solución:**
1. Abre Laragon
2. Haz clic en "Start All" para iniciar MySQL
3. Espera a que esté verde ✅
4. Vuelve a intentar

### Error: "Database refaccionaria_db doesn't exist"
**Solución:**
La BD se crea automáticamente si usas Docker. Para local:
```bash
# Verificar que la BD existe:
mysql -u root -proot -e "SHOW DATABASES;"

# Si no existe, ejecutar:
mysql -u root -proot < refaccionaria_db.sql
```

---

## 🧪 Verificar que Todo Funciona

```bash
# 1. Verificar conexión a BD
python test_conexion.py

# 2. Verificar usuarios en BD
python crear_usuarios.py

# 3. Ver hashes de contraseñas
python generar_hashes.py

# 4. Actualizar contraseñas si es necesario
python actualizar_contrasenas.py
```

---

## 📊 Base de Datos

**Nombre**: `refaccionaria_db`
**Usuario**: `root`
**Contraseña**: `root`
**Host**: `localhost:3306`

### Tablas principales:
- `usuarios` - Perfiles y credenciales
- `productos` - Catálogo de productos
- `ventas` - Registro de ventas
- `compras` - Registro de compras
- `locales` - Sucursales
- y más...

---

## 📝 Notas Importantes

1. **Las contraseñas están hasheadas** con SHA256 (no se guardan en texto plano)
2. **MySQL debe estar corriendo** antes de iniciar la API
3. **El .env contiene las credenciales** para conectarse a MySQL
4. **La API usa SQLAlchemy** para ORM
5. **Los usuarios ya están creados** en la base de datos

---

## 🎯 Próximos Pasos

1. ✅ Verifica que Laragon y MySQL estén corriendo
2. ✅ Inicia la API con `python run.py`
3. ✅ Accede a `http://localhost:8000`
4. ✅ Usa las credenciales para login
5. ✅ Verifica que todo funciona

---

**¿Necesitas ayuda?**
Si aún tienes errores de conexión, ejecuta en terminal:
```bash
python test_conexion.py
```
para verificar que la conexión a la BD funciona.
