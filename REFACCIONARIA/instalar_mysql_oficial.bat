@echo off
echo.
echo ========================================
echo   INSTALACION MYSQL SERVER OFICIAL
echo ========================================
echo.
echo Este script descargara e instalara MySQL Server 8.0
echo.
echo NOTA: Necesitaras permisos de administrador
echo.
pause

echo.
echo Abriendo pagina de descarga de MySQL...
start https://dev.mysql.com/downloads/installer/

echo.
echo ========================================
echo   INSTRUCCIONES DE INSTALACION
echo ========================================
echo.
echo 1. En la pagina web que se abrio:
echo    - Descarga: "mysql-installer-community-8.0.XX.msi"
echo    - Puedes usar la version "web" (mas pequena)
echo    - NO necesitas crear cuenta, click en "No thanks, just start my download"
echo.
echo 2. Ejecuta el instalador descargado
echo.
echo 3. En "Choosing a Setup Type":
echo    - Selecciona: "Server only"
echo    - Click "Next"
echo.
echo 4. Click "Execute" para instalar
echo.
echo 5. En "Type and Networking":
echo    - Deja todo por defecto (Puerto 3306)
echo    - Click "Next"
echo.
echo 6. En "Authentication Method":
echo    - Selecciona: "Use Legacy Authentication Method"
echo    - Click "Next"
echo.
echo 7. En "Accounts and Roles":
echo    - Root Password: DEJALA VACIA (solo presiona Next)
echo    - O si quieres password, anotala bien
echo    - Click "Next"
echo.
echo 8. En "Windows Service":
echo    - Service Name: MySQL80
echo    - Start at System Startup: MARCADO
echo    - Click "Next"
echo.
echo 9. Click "Execute" para aplicar configuracion
echo.
echo 10. Click "Finish"
echo.
echo ========================================
echo.
echo Una vez completada la instalacion,
echo presiona cualquier tecla para verificar...
echo.
pause

echo.
echo Verificando instalacion...
echo.

sc query MySQL80 >nul 2>&1
if errorlevel 1 (
    sc query MySQL >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] No se detecto el servicio MySQL
        echo.
        echo Posibles causas:
        echo - La instalacion no se completo
        echo - El servicio tiene otro nombre
        echo.
        echo Puedes verificar manualmente:
        echo 1. Abre "services.msc"
        echo 2. Busca "MySQL" en la lista
        echo 3. Verifica que este "Iniciado"
        echo.
        pause
        exit /b 1
    ) else (
        set SERVICE_NAME=MySQL
    )
) else (
    set SERVICE_NAME=MySQL80
)

echo [OK] Servicio %SERVICE_NAME% encontrado
echo.

REM Verificar estado
sc query %SERVICE_NAME% | find "RUNNING" >nul
if errorlevel 1 (
    echo Servicio no esta corriendo. Iniciando...
    net start %SERVICE_NAME%
    if errorlevel 1 (
        echo [ERROR] No se pudo iniciar el servicio
        pause
        exit /b 1
    )
)

echo [OK] MySQL esta corriendo
echo.
echo Creando base de datos...

REM Buscar mysql.exe
set MYSQL_EXE=
if exist "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" set "MYSQL_EXE=C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
if exist "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe" set "MYSQL_EXE=C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe"

if "%MYSQL_EXE%"=="" (
    echo [ADVERTENCIA] No se encontro mysql.exe
    echo Crea la base de datos manualmente:
    echo   mysql -u root
    echo   CREATE DATABASE refaccionaria_db;
    echo.
) else (
    "%MYSQL_EXE%" -u root -e "CREATE DATABASE IF NOT EXISTS refaccionaria_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>nul
    if errorlevel 1 (
        echo [ADVERTENCIA] No se pudo crear la base de datos
        echo Si configuraste password, ejecuta:
        echo   mysql -u root -p
        echo   CREATE DATABASE refaccionaria_db;
    ) else (
        echo [OK] Base de datos creada
    )
)

echo.
echo ========================================
echo   INSTALACION COMPLETADA
echo ========================================
echo.
echo Ejecutando verificacion final...
cd /d "%~dp0"
python verificar_conexion.py
