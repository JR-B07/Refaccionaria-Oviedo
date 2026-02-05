# 🔧 Diagnóstico y Solución: Error de Conexión a MySQL

**Última actualización**: 4 de febrero de 2026

## ❌ Error Actual

```
❌ Error en DB: (pymysql.err.OperationalError) (1045, "Access denied for user 'root'@'localhost' (using password: NO)")
```

## 🔍 Diagnóstico

El error `(using password: NO)` significa que **MySQL rechazó la conexión porque no se está enviando contraseña**.

### Causas Posibles

1. **MySQL no está corriendo**
2. **Credenciales incorrectas en `.env`**
3. **Usuario MySQL no existe**
4. **Base de datos no está inicializada**

---

## ✅ SOLUCIONES POR ESCENARIO

### **ESCENARIO A: Ejecutar en Docker (Recomendado)**

#### Paso 1: Verificar Docker
```bash
# Ver si Docker está corriendo
docker --version
docker ps

# Iniciar Docker Desktop si es necesario
```

#### Paso 2: Ejecutar Docker Compose
```bash
cd REFACCIONARIA

# Detener contenedores previos
docker-compose down

# Iniciar todo (MySQL, Redis, API)
docker-compose up -d

# Ver estado
docker-compose ps
```

#### Paso 3: Verificar Conexión
```bash
# Ver logs del API
docker-compose logs -f api

# Prueba conexión a MySQL dentro del contenedor
docker exec refaccionaria_mysql mysql -u refaccionaria -pSecurePass123! -e "SELECT 1"
```

**Esperado**: Verde en logs, sin errores de conexión.

---

### **ESCENARIO B: Ejecutar Localmente (MySQL en localhost)**

#### Paso 1: Verificar que MySQL esté Corriendo

**Windows**:
```bash
# Ver estado del servicio MySQL
services.msc
# O busca "MySQL" y verifica que esté corriendo

# O desde línea de comandos
mysql --version
mysql -u root -e "SELECT 1"
```

**Mac/Linux**:
```bash
# Ver si MySQL está corriendo
sudo systemctl status mysql
# o
brew services list | grep mysql
```

#### Paso 2: Crear Base de Datos y Usuario

Si MySQL está corriendo pero la BD no existe, ejecuta:

```bash
# Conectar como root
mysql -u root -p

# Dentro de MySQL:
```sql
-- Crear base de datos
CREATE DATABASE IF NOT EXISTS refaccionaria_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Opción B1: Usar usuario root (más simple)
-- No requiere cambios en .env

-- Opción B2: Crear usuario específico (más seguro)
CREATE USER 'refaccionaria'@'localhost' IDENTIFIED BY 'SecurePass123!';
GRANT ALL PRIVILEGES ON refaccionaria_db.* TO 'refaccionaria'@'localhost';
FLUSH PRIVILEGES;

-- Luego en .env cambiar a:
-- MYSQL_USER=refaccionaria
-- MYSQL_PASSWORD=SecurePass123!

-- Verificar
SELECT User, Host FROM mysql.user;
```

#### Paso 3: Actualizar `.env`

**Opción B1** (usuario root sin contraseña):
```env
MYSQL_SERVER=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=refaccionaria_db
MYSQL_PORT=3306
```

**Opción B2** (usuario específico):
```env
MYSQL_SERVER=localhost
MYSQL_USER=refaccionaria
MYSQL_PASSWORD=SecurePass123!
MYSQL_DB=refaccionaria_db
MYSQL_PORT=3306
```

#### Paso 4: Ejecutar la Aplicación

```bash
cd REFACCIONARIA

# Activar entorno virtual
python -m venv venv
source venv/Scripts/activate  # Windows
# o
source venv/bin/activate      # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python start.py
# o
uvicorn app.main:app --reload
```

#### Paso 5: Verificar Conexión

Abre el navegador:
```
http://localhost:8000
http://localhost:8000/docs
```

Si ves la API sin errores de BD ✅ funcionó.

---

## 🧪 VERIFICACIÓN RÁPIDA

### Probar Conexión MySQL

```bash
# Test 1: Verificar que MySQL está corriendo
ping localhost:3306

# Test 2: Conectar con credenciales
mysql -h localhost -u root -p refaccionaria_db

# Test 3: Desde Python
python -c "
import pymysql
try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',  # Cambiar si es necesario
        database='refaccionaria_db'
    )
    print('✅ Conexión exitosa')
    conn.close()
except Exception as e:
    print(f'❌ Error: {e}')
"
```

---

## 📋 Checklist de Solución

- [ ] Docker Desktop está instalado y corriendo
- [ ] MySQL está corriendo (local o en Docker)
- [ ] Base de datos `refaccionaria_db` existe
- [ ] Usuario MySQL tiene las credenciales correctas
- [ ] `.env` tiene credenciales que coinciden
- [ ] `docker-compose down` seguido de `docker-compose up -d` ejecutado
- [ ] Espere 10 segundos a que MySQL se inicialice
- [ ] Logs no muestran error de conexión

---

## 🚀 RECOMENDACIÓN

**Para desarrollo más rápido**: Usar Docker Compose

```bash
cd REFACCIONARIA
docker-compose up -d
# Listo, todo funciona automáticamente
```

**Logs en tiempo real**:
```bash
docker-compose logs -f api
```

---

## 💡 Notas

1. **Error `(using password: NO)`** = Contraseña no se está pasando
2. **Puerto 3306** = Puerto por defecto de MySQL (asegúrate no esté en uso)
3. **Firewall** = Si MySQL está en otra máquina, verifica firewall
4. **InnoDB** = Motor de BD requerido (Docker lo instala automáticamente)

---

## 📞 Si Sigue Sin Funcionar

1. Verifica los logs completos:
   ```bash
   docker-compose logs mysql
   docker-compose logs api
   ```

2. Resetea todo:
   ```bash
   docker-compose down -v  # Borra volúmenes
   docker-compose up -d    # Nuevo inicio
   ```

3. Verifica que puertos no estén en uso:
   ```bash
   # Puerto 3306 (MySQL)
   # Puerto 6379 (Redis) 
   # Puerto 8000 (API)
   ```

---

**Resumen**: Si usas Docker, debe funcionar automáticamente. Si ejecutas localmente, verifica que MySQL esté corriendo y credenciales sean correctas. 🎯
