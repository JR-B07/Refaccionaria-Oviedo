# Migración de Bcrypt a SHA256

## 📋 Resumen de Cambios

Se han reemplazado todas las implementaciones de bcrypt por SHA256 en el sistema de autenticación.

## ⚠️ IMPORTANTE: Implicaciones de Seguridad

**SHA256 es significativamente menos seguro que bcrypt para almacenar contraseñas:**

- ❌ **Sin salt**: SHA256 no incluye un salt automático, lo que hace las contraseñas vulnerables a ataques de tablas rainbow
- ❌ **Rápido de calcular**: SHA256 está diseñado para ser rápido, lo que facilita ataques de fuerza bruta
- ❌ **No adaptativo**: bcrypt permite ajustar el costo computacional; SHA256 no

**bcrypt es el estándar recomendado para contraseñas** porque:
- ✅ Incluye salt automático
- ✅ Es computacionalmente costoso (dificulta ataques de fuerza bruta)
- ✅ Es adaptativo (el costo puede aumentarse en el futuro)

**Solo usa SHA256 para desarrollo/pruebas o entornos no críticos.**

## 📁 Archivos Modificados

### Backend Principal
- ✅ `app/core/security.py` - Cambió de passlib/bcrypt a hashlib/SHA256
- ✅ `app/api/v1/endpoints/auth.py` - Cambió validación de bcrypt.checkpw() a comparación SHA256

### Scripts de Utilidad
- ✅ `crear_usuarios.py` - Función hash_password() ahora usa SHA256
- ✅ `generar_hashes.py` - Genera hashes SHA256 en lugar de bcrypt
- ✅ `gen_hash.py` - Usa hashlib SHA256
- ✅ `reset_password.py` - Resetea contraseñas con SHA256
- ✅ `reset_admin.py` - Crea/actualiza usuarios con SHA256
- ✅ `crear_usuarios_sucursal2.py` - Genera hashes SHA256
- ✅ `test_bcrypt.py` - Actualizado para usar SHA256
- ✅ `test_bcrypt_demo.py` - Actualizado para usar SHA256
- ✅ `actualizar_contrasenas.py` - Hashes actualizados a SHA256

### Scripts de Creación
- ✅ `scripts/create_test_users.py` - Comentario actualizado (usa get_password_hash)

### Archivos SQL
- ✅ `setup_usuarios.sql` - Hashes y comentarios actualizados a SHA256
- ✅ `refaccionaria_db.sql` - Comentario actualizado

### Documentación
- ✅ `GUIA_ACCESO.md` - Documentación actualizada

### Dependencias
- ✅ `requirements.txt` - Eliminada dependencia `passlib[bcrypt]==1.7.4`

### Nuevos Scripts
- ✅ `generar_hash_sha256.py` - Script para generar hashes SHA256 interactivamente
- ✅ `migrar_bcrypt_a_sha256.py` - Script de migración para actualizar BD existente

## 🔐 Hashes SHA256 de Contraseñas Comunes

```
admin       -> 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918
admin123    -> 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9
sucursal1   -> 2d7c68c9c52a0744c39ce0d9aa3ccdefdac05166ae07a698470b887ab493e120
sucursal2   -> c90566e7b8c589a456db11cfdfaba5b152238ee4621231899306aecd0b694770
sucursal123 -> c28ec11529a52c617e5b700350aa494b4d3b1d55958a4b9bd125a8a6696005a6
password123 -> ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
```

## 🚀 Pasos para Migrar Base de Datos Existente

Si ya tienes una base de datos con contraseñas en bcrypt, sigue estos pasos:

### 1. Hacer Respaldo
```bash
# Respaldar la base de datos antes de cualquier cambio
mysqldump -u root -p refaccionaria_db > backup_antes_migracion.sql
```

### 2. Ejecutar Script de Migración
```bash
cd REFACCIONARIA
python migrar_bcrypt_a_sha256.py
```

Este script:
- Conecta a tu base de datos
- Actualiza las contraseñas de usuarios conocidos
- Genera nuevos hashes SHA256

### 3. Verificar Migración
```bash
# Probar login con las credenciales actualizadas
python test_login.py
```

## 🛠️ Generar Nuevos Hashes

Para generar hashes de nuevas contraseñas, usa uno de estos métodos:

### Método 1: Script Interactivo
```bash
python generar_hash_sha256.py
```

### Método 2: Línea de Comandos
```bash
python -c "import hashlib; print(hashlib.sha256(b'tu_password').hexdigest())"
```

### Método 3: Python
```python
import hashlib
hash_val = hashlib.sha256("tu_password".encode()).hexdigest()
print(hash_val)
```

## 🔄 Actualización del Sistema

### Instalación de Dependencias
```bash
# Reinstalar dependencias (passlib ya no es necesario)
pip install -r requirements.txt
```

### Reiniciar Servicios
```bash
# Reiniciar el servidor FastAPI
python run.py
```

## 🧪 Pruebas

Después de la migración, prueba:

1. **Login de usuarios existentes**
   ```bash
   python test_login.py
   ```

2. **Creación de nuevos usuarios**
   ```bash
   python crear_usuarios.py
   ```

3. **Reset de contraseñas**
   ```bash
   python reset_password.py
   ```

## 📝 Notas Técnicas

### Cambios en el Código

**Antes (bcrypt):**
```python
import bcrypt
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
valid = bcrypt.checkpw(password.encode(), hash.encode())
```

**Después (SHA256):**
```python
import hashlib
hash = hashlib.sha256(password.encode()).hexdigest()
valid = (hashlib.sha256(password.encode()).hexdigest() == hash)
```

### Función de Hash en app/core/security.py

```python
def get_password_hash(password: str) -> str:
    """Genera hash SHA256 de contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña en texto plano coincide con el hash SHA256"""
    password_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    return password_hash == hashed_password
```

## ❓ Preguntas Frecuentes

### ¿Por qué cambiar de bcrypt a SHA256?
SHA256 es más simple pero menos seguro. Este cambio solo debe hacerse para desarrollo o si no necesitas alta seguridad.

### ¿Puedo revertir a bcrypt?
Sí, pero necesitarás:
1. Restaurar los archivos modificados
2. Reinstalar `passlib[bcrypt]`
3. Migrar las contraseñas de vuelta a bcrypt

### ¿Las contraseñas existentes seguirán funcionando?
No, necesitas ejecutar el script de migración `migrar_bcrypt_a_sha256.py` para actualizar los hashes.

### ¿Qué pasa con usuarios nuevos?
Los nuevos usuarios automáticamente usarán SHA256 a través de `get_password_hash()`.

## 📞 Soporte

Si tienes problemas durante la migración:
1. Verifica que MySQL esté corriendo
2. Confirma las credenciales en `.env`
3. Revisa que hayas hecho backup de la BD
4. Consulta los logs de error

---

**Fecha de migración:** 11 de febrero de 2026
**Sistema:** Refaccionaria Oviedo
**Cambio:** bcrypt -> SHA256
