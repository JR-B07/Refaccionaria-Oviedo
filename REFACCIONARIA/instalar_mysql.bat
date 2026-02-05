@echo off
echo.
echo ========================================
echo   INSTALACION RAPIDA DE MYSQL SERVER
echo ========================================
echo.
echo Este script instalara MySQL Server 8.0
echo.
pause

echo.
echo Verificando si Chocolatey esta instalado...
where choco >nul 2>&1
if errorlevel 1 (
    echo.
    echo Chocolatey no esta instalado.
    echo Instalando Chocolatey...
    echo.
    
    @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
    
    if errorlevel 1 (
        echo.
        echo [ERROR] No se pudo instalar Chocolatey
        echo Por favor, instala MySQL manualmente desde:
        echo https://dev.mysql.com/downloads/installer/
        pause
        exit /b 1
    )
    
    echo.
    echo Chocolatey instalado correctamente
)

echo.
echo Instalando MySQL Server...
echo (Esto puede tomar varios minutos)
echo.

choco install mysql -y

if errorlevel 1 (
    echo.
    echo [ERROR] No se pudo instalar MySQL con Chocolatey
    echo.
    echo Instalacion manual requerida:
    echo 1. Ve a: https://dev.mysql.com/downloads/installer/
    echo 2. Descarga MySQL Installer
    echo 3. Ejecuta el instalador
    echo 4. Selecciona "Server only"
    echo 5. Configura root sin password o anota la password
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   MYSQL INSTALADO CORRECTAMENTE
echo ========================================
echo.
echo Iniciando servicio MySQL...
net start MySQL

echo.
echo Creando base de datos...
cd /d "%~dp0"

REM Crear la base de datos
mysql -u root -e "CREATE DATABASE IF NOT EXISTS refaccionaria_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if errorlevel 1 (
    echo.
    echo [ADVERTENCIA] No se pudo crear la base de datos automaticamente
    echo Ejecuta manualmente:
    echo   mysql -u root
    echo   CREATE DATABASE refaccionaria_db;
    echo.
)

echo.
echo ========================================
echo   INSTALACION COMPLETADA
echo ========================================
echo.
echo Ahora puedes ejecutar Refaccionaria.bat
echo.
pause
