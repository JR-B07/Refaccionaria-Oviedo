@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo   CONFIGURAR MYSQL COMO SERVICIO
echo ========================================
echo.

REM Buscar instalacion de MySQL
set MYSQL_PATH=
set MYSQL_BIN=

echo Buscando instalacion de MySQL...
echo.

REM Buscar en Program Files
if exist "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe" (
    set "MYSQL_PATH=C:\Program Files\MySQL\MySQL Server 8.0"
    set "MYSQL_BIN=!MYSQL_PATH!\bin"
)

if exist "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe" (
    set "MYSQL_PATH=C:\Program Files\MySQL\MySQL Server 8.4"
    set "MYSQL_BIN=!MYSQL_PATH!\bin"
)

if exist "C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysqld.exe" (
    set "MYSQL_PATH=C:\Program Files (x86)\MySQL\MySQL Server 8.0"
    set "MYSQL_BIN=!MYSQL_PATH!\bin"
)

REM Buscar en XAMPP
if exist "C:\xampp\mysql\bin\mysqld.exe" (
    set "MYSQL_PATH=C:\xampp\mysql"
    set "MYSQL_BIN=!MYSQL_PATH!\bin"
)

if "%MYSQL_BIN%"=="" (
    echo [ERROR] No se encontro MySQL instalado en ubicaciones comunes
    echo.
    echo Ubicaciones revisadas:
    echo   - C:\Program Files\MySQL\MySQL Server 8.0
    echo   - C:\Program Files\MySQL\MySQL Server 8.4
    echo   - C:\Program Files (x86)\MySQL\MySQL Server 8.0
    echo   - C:\xampp\mysql
    echo.
    echo Por favor, indica manualmente la ruta de instalacion de MySQL
    echo o instala MySQL desde: https://dev.mysql.com/downloads/installer/
    echo.
    pause
    exit /b 1
)

echo [OK] MySQL encontrado en: !MYSQL_PATH!
echo.

REM Verificar permisos de administrador
net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Este script requiere permisos de administrador
    echo.
    echo Por favor, ejecuta este archivo como Administrador:
    echo   1. Click derecho en el archivo .bat
    echo   2. Selecciona "Ejecutar como administrador"
    echo.
    pause
    exit /b 1
)

echo [OK] Ejecutando con permisos de administrador
echo.

REM Verificar si el servicio ya existe
sc query MySQL80 >nul 2>&1
if not errorlevel 1 (
    echo Servicio MySQL80 ya existe
    echo Verificando estado...
    sc query MySQL80 | find "RUNNING" >nul
    if errorlevel 1 (
        echo Iniciando servicio...
        net start MySQL80
    ) else (
        echo [OK] MySQL80 ya esta corriendo
    )
    echo.
    goto :crear_db
)

sc query MySQL >nul 2>&1
if not errorlevel 1 (
    echo Servicio MySQL ya existe
    echo Verificando estado...
    sc query MySQL | find "RUNNING" >nul
    if errorlevel 1 (
        echo Iniciando servicio...
        net start MySQL
    ) else (
        echo [OK] MySQL ya esta corriendo
    )
    echo.
    goto :crear_db
)

echo Instalando MySQL como servicio...
echo.

REM Cambiar a directorio de MySQL
cd /d "!MYSQL_BIN!"

REM Instalar servicio
echo Ejecutando: mysqld --install MySQL80
mysqld --install MySQL80

if errorlevel 1 (
    echo [ERROR] No se pudo instalar el servicio
    echo Intentando con nombre alternativo...
    mysqld --install MySQL
    if errorlevel 1 (
        echo [ERROR] Fallo al instalar servicio MySQL
        pause
        exit /b 1
    )
    set SERVICE_NAME=MySQL
) else (
    set SERVICE_NAME=MySQL80
)

echo [OK] Servicio !SERVICE_NAME! instalado correctamente
echo.

echo Iniciando servicio !SERVICE_NAME!...
net start !SERVICE_NAME!

if errorlevel 1 (
    echo [ERROR] No se pudo iniciar el servicio
    echo.
    echo Posibles soluciones:
    echo   1. Verifica que el puerto 3306 no este en uso
    echo   2. Revisa los logs en: !MYSQL_PATH!\data
    echo   3. Ejecuta: sc delete !SERVICE_NAME! y vuelve a intentar
    echo.
    pause
    exit /b 1
)

echo [OK] Servicio iniciado correctamente
echo.

:crear_db
echo.
echo ========================================
echo   CONFIGURANDO BASE DE DATOS
echo ========================================
echo.

cd /d "%~dp0"

echo Creando base de datos refaccionaria_db...
"!MYSQL_BIN!\mysql.exe" -u root -e "CREATE DATABASE IF NOT EXISTS refaccionaria_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>nul

if errorlevel 1 (
    echo.
    echo [ADVERTENCIA] No se pudo crear la base de datos automaticamente
    echo.
    echo Crea la base de datos manualmente:
    echo   1. Abre CMD y ejecuta: mysql -u root -p
    echo   2. Ingresa tu password de root
    echo   3. Ejecuta: CREATE DATABASE refaccionaria_db;
    echo   4. Ejecuta: exit;
    echo.
    echo Si no recuerdas la password, puedes resetearla
    pause
) else (
    echo [OK] Base de datos creada correctamente
)

echo.
echo ========================================
echo   CONFIGURACION COMPLETADA
echo ========================================
echo.
echo MySQL esta configurado y corriendo como servicio
echo Ahora puedes ejecutar: Refaccionaria.bat
echo.
pause
