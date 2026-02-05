# 🔧 Configuración de Conexión a Base de Datos

**Última actualización**: 4 de febrero de 2026

## ❌ Problema Encontrado

El servicio `api` en Docker no estaba recibiendo las credenciales de MySQL, causando el error:

```
❌ Error en DB: (pymysql.err.OperationalError) (1045, "Access denied for user 'root'@'localhost' (using password: NO)")
```

## ✅ Solución Implementada

### 1. **docker-compose.yaml** - ACTUALIZADO
Agregadas las variables de entorno necesarias al servicio `api`:

```yaml
environment:
  MYSQL_SERVER: mysql          # Nombre del servicio MySQL
  MYSQL_USER: refaccionaria    # Usuario de BD
  MYSQL_PASSWORD: SecurePass123!
  MYSQL_DB: refaccionaria_db
  MYSQL_PORT: 3306
  REDIS_URL: redis://redis:6379/0
```

### 2. **app/core/config.py** - ACTUALIZADO
Ahora lee las credenciales desde variables de entorno:

```python
MYSQL_SERVER: str = os.getenv("MYSQL_SERVER", "localhost")
MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB: str = os.getenv("MYSQL_DB", "refaccionaria_db")
MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
```

Esto permite:
- ✅ Usar variables de entorno en Docker
- ✅ Usar archivo `.env` en desarrollo local
- ✅ Valores por defecto sensatos

## 🚀 Cómo Ejecutar

### Opción 1: Docker Compose (Recomendado)

```bash
cd REFACCIONARIA
docker-compose down    # Detener contenedores anteriores
docker-compose up -d   # Iniciar servicios
```

Verifica que todo funcione:
```bash
# Ver logs
docker-compose logs api

# La aplicación estará en
http://localhost:8000
http://localhost:8000/docs
```

### Opción 2: Desarrollo Local

Requiere:
- MySQL 8.0+ corriendo en `localhost:3306`
- Usuario `root` con contraseña vacía (o actualizar `.env`)

```bash
cd REFACCIONARIA

# Activar entorno virtual
python -m venv venv
source venv/Scripts/activate  # Windows
# o
source venv/bin/activate      # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python run.py
# o
uvicorn app.main:app --reload
```

## 📋 Verificación

### Archivo `.env` (desarrollo local)
```
PROJECT_NAME="Refaccionaria ERP"
VERSION="1.0.0"
DEBUG=true

MYSQL_SERVER=localhost
MYSQL_USER=root
MYSQL_PASSWORD=                    # O tu contraseña local
MYSQL_DB=refaccionaria_db
MYSQL_PORT=3306
```

### Archivo `docker-compose.yaml` (Docker)
```yaml
services:
  mysql:
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: refaccionaria_db
      MYSQL_USER: refaccionaria
      MYSQL_PASSWORD: SecurePass123!

  api:
    environment:
      MYSQL_SERVER: mysql           # ✅ AHORA INCLUIDO
      MYSQL_USER: refaccionaria     # ✅ AHORA INCLUIDO  
      MYSQL_PASSWORD: SecurePass123! # ✅ AHORA INCLUIDO
```

## 🔍 Troubleshooting

### Error: "Access denied for user 'root'@'localhost'"

**Causa**: Las credenciales de MySQL no son correctas.

**Soluciones**:
1. Verifica que MySQL esté corriendo
2. Verifica las credenciales en `.env` (desarrollo local)
3. Verifica que Docker esté iniciado y los contenedores corriendo (`docker ps`)

```bash
# Prueba conexión en Docker
docker exec refaccionaria_mysql mysql -u refaccionaria -pSecurePass123! -e "SELECT 1"

# Prueba conexión local
mysql -u root -p refaccionaria_db
```

### Error: "Connection refused"

**Causa**: MySQL no está disponible.

**Solución**: 
```bash
# En Docker
docker-compose ps  # Verifica que mysql esté UP
docker-compose logs mysql

# En desarrollo local
# Asegúrate de que MySQL esté corriendo en localhost:3306
```

## 📊 Credenciales por Entorno

| Entorno | Host | Usuario | Contraseña | BD |
|---------|------|---------|------------|-----|
| **Docker** | mysql | refaccionaria | SecurePass123! | refaccionaria_db |
| **Local** | localhost | root | (vacío) | refaccionaria_db |

## 🔐 Seguridad

⚠️ **Importante para Producción**:
- Cambiar `SECRET_KEY` en `config.py`
- Cambiar contraseñas de MySQL
- No dejar DEBUG=true
- Usar variables de entorno seguras

---

**Resumen**: Ahora el sistema pasa las credenciales correctas de MySQL al contenedor Docker y lee variables de entorno según el contexto (Docker o local). 🎯
