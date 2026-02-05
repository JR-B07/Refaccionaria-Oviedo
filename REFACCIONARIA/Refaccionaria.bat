@echo off
setlocal enabledelayedexpansion
title Refaccionaria Oviedo - Sistema ERP v1.0

REM Cambiar a la carpeta del script
cd /d "%~dp0"

color 0B
cls

echo.
echo ========================================
echo   REFACCIONARIA ERP - INICIO
echo ========================================
echo   Version: 1.0.0
echo   Fecha: 4 de Febrero 2026
echo ========================================
echo.

REM Verificar permisos de administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ADVERTENCIA] Se recomienda ejecutar como Administrador
    echo.
)

REM Verificar e iniciar MySQL
echo Verificando MySQL...
sc query MySQL >nul 2>&1
if not errorlevel 1 (
    echo Servicio MySQL encontrado
    REM Verificar si MySQL ya esta corriendo
    sc query MySQL | find "RUNNING" >nul
    if errorlevel 1 (
        echo Iniciando servicio MySQL...
        net start MySQL >nul 2>&1
        if errorlevel 1 (
            echo [ADVERTENCIA] No se pudo iniciar MySQL (puede requerir permisos de administrador)
            echo Intenta ejecutar como Administrador o inicia MySQL manualmente
        ) else (
            echo MySQL iniciado correctamente
            timeout /t 2 /nobreak >nul
        )
    ) else (
        echo MySQL ya esta ejecutandose
    )
) else (
    REM Intentar con MySQL80 (nombre comun en instalaciones recientes)
    sc query MySQL80 >nul 2>&1
    if not errorlevel 1 (
        echo Servicio MySQL80 encontrado
        sc query MySQL80 | find "RUNNING" >nul
        if errorlevel 1 (
            echo Iniciando servicio MySQL80...
            net start MySQL80 >nul 2>&1
            if not errorlevel 1 (
                echo MySQL80 iniciado correctamente
                timeout /t 2 /nobreak >nul
            )
        ) else (
            echo MySQL80 ya esta ejecutandose
        )
    ) else (
        echo [ADVERTENCIA] No se encontro servicio MySQL instalado
        echo Asegurate de tener MySQL instalado y configurado
        echo.
    )
)
echo.

echo Verificando Python...

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    echo Por favor instala Python 3.8 o superior
    pause
    exit /b 1
)

echo Python encontrado
echo.

REM Verificar e instalar dependencias
echo Verificando dependencias necesarias...
python -c "import webview" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias principales...
    pip install -q pywebview requests uvicorn sqlalchemy pymysql python-dotenv >nul 2>&1
    if errorlevel 1 (
        echo [ADVERTENCIA] Hubo problemas al instalar algunas dependencias
    ) else (
        echo Dependencias instaladas correctamente
    )
    echo.
)

REM Verificar estructura de directorios
echo Verificando estructura del proyecto...
if not exist "app\main.py" (
    echo [ERROR] No se encontro app/main.py
    echo El proyecto podria estar incompleto
    pause
    exit /b 1
)
echo Estructura del proyecto verificada
echo.

REM Crear carpeta logs si no existe
if not exist "logs" (
    mkdir logs
)

REM Crear archivo de configuracion si no existe
if not exist ".env" (
    echo Creando archivo de configuracion...
    (
        echo DEBUG=true
        echo MYSQL_SERVER=localhost
        echo MYSQL_USER=root
        echo MYSQL_PASSWORD=root
        echo MYSQL_DB=refaccionaria_db
        echo MYSQL_PORT=3306
    ) > .env
    echo Archivo de configuracion creado
    echo.
)

echo Iniciando Refaccionaria ERP...
echo.
echo ========================================
echo   INICIANDO SERVIDOR Y APLICACION
echo ========================================
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
timeout /t 2 /nobreak >nul

REM Intentar usar pythonw.exe (Python sin ventana de consola)
where pythonw.exe >nul 2>&1
if %errorlevel% equ 0 (
    REM pythonw.exe existe, usarlo para ocultar la consola de Python
    start "" pythonw.exe launch_desktop.py
    timeout /t 3 /nobreak >nul
    exit /b 0
)

REM Si pythonw no existe, usar python normalmente
python launch_desktop.py
pause
