# INSTALACIÓN MANUAL DE MYSQL SERVER

## Método 1: Descarga directa (Recomendado)

1. **Descargar MySQL Installer**
   - Ve a: https://dev.mysql.com/downloads/installer/
   - Descarga: `mysql-installer-community-8.0.XX.msi`
   - Elige la versión "web" (más pequeña)

2. **Ejecutar instalador**
   - Doble clic en el archivo descargado
   - Selecciona: "Server only" (o "Developer Default")
   - Click en "Execute" para descargar e instalar

3. **Configuración inicial**
   - Type and Networking: Deja valores por defecto (Puerto 3306)
   - Authentication: Usa "Legacy Authentication Method" (más compatible)
   - Accounts and Roles:
     * Root Password: **Déjala vacía** (o anota una contraseña)
   - Windows Service:
     * Nombre: MySQL80 o MySQL
     * Start at System Startup: ✓ (marcado)
   - Apply Configuration

4. **Crear base de datos**
   ```bash
   # Abre CMD como Administrador y ejecuta:
   mysql -u root
   CREATE DATABASE refaccionaria_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   exit;
   ```

5. **Si usaste contraseña, actualiza el archivo .env**
   - Crea/edita: `REFACCIONARIA\.env`
   - Agrega: `MYSQL_PASSWORD=tu_contraseña`

---

## Método 2: Con XAMPP (Más fácil para desarrollo)

1. **Descargar XAMPP**
   - Ve a: https://www.apachefriends.org/
   - Descarga la última versión

2. **Instalar XAMPP**
   - Ejecuta el instalador
   - Desmarca Apache si no lo necesitas
   - Marca solo MySQL

3. **Iniciar MySQL**
   - Abre XAMPP Control Panel
   - Click en "Start" en la fila de MySQL

4. **Crear base de datos**
   - Ve a: http://localhost/phpmyadmin
   - Click en "Nueva"
   - Nombre: `refaccionaria_db`
   - Cotejamiento: `utf8mb4_unicode_ci`
   - Crear

5. **Actualizar configuración** (si usa puerto diferente)
   - XAMPP usa puerto 3306 por defecto
   - Si es diferente, actualiza `MYSQL_PORT` en `.env`

---

## Método 3: Con Chocolatey (Automático)

Si tienes permisos de administrador, ejecuta:

```bash
# Ejecuta como Administrador el archivo:
instalar_mysql.bat
```

Este script instalará MySQL automáticamente.

---

## Verificar instalación

```bash
# Ejecuta cualquiera de estos:
verificar_conexion.bat
# o
python verificar_conexion.py
```

Debe mostrar: ✅ Servicio MySQL está corriendo

---

## Solución de problemas

### "Servicio no inicia"
```bash
# Como Administrador:
net start MySQL
# o
net start MySQL80
```

### "Access denied for user 'root'"
- Editala archivo `.env`
- Agrega tu contraseña: `MYSQL_PASSWORD=tu_contraseña`

### "Can't connect to MySQL server"
- Verifica que MySQL esté corriendo
- Verifica el puerto (3306 es el predeterminado)
- Desactiva temporalmente el firewall para probar

---

## Contacto con errores

Si encuentras errores, ejecuta:
```bash
verificar_conexion.bat
```

Y comparte el resultado para ayudarte mejor.
