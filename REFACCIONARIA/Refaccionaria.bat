@echo off
setlocal enabledelayedexpansion

REM Cambiar a la carpeta del script
cd /d "%~dp0"

echo.
echo Verificando Python...

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    pause
    exit /b 1
)

echo Python encontrado
echo.

REM Verificar e instalar dependencias silenciosamente
python -c "import webview" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -q pywebview requests >nul 2>&1
    echo Dependencias instaladas
    echo.
)

echo Iniciando Refaccionaria ERP...
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

REM Intentar usar pythonw.exe (Python sin ventana de consola)
where pythonw.exe >nul 2>&1
if %errorlevel% equ 0 (
    REM pythonw.exe existe, usarlo
    start "" pythonw.exe launch_desktop.py
    timeout /t 3 /nobreak >nul
    exit /b 0
)

REM Si pythonw no existe, usar python normalmente
python launch_desktop.py
