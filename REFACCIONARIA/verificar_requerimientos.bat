@echo off
REM Script de verificación de requisitos - Refaccionaria Oviedo
REM Ejecutar ANTES de instalar el sistema

chcp 65001 >nul
cls
color 0A

echo.
echo ========================================================================
echo              VERIFICADOR DE REQUISITOS
echo                  Refaccionaria Oviedo
echo ========================================================================
echo.

set requirements_ok=1

REM Verificar Python
echo [1/5] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ❌ ERROR: Python no está instalado
    echo      Descarga desde: https://www.python.org/downloads/
    set requirements_ok=0
) else (
    for /f "tokens=*" %%A in ('python --version') do (
        echo   ✅ %%A
    )
)

REM Verificar MySQL
echo.
echo [2/5] Verificando MySQL...
mysql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ❌ ERROR: MySQL no está instalado
    echo      Descarga desde: https://dev.mysql.com/downloads/mysql/
    set requirements_ok=0
) else (
    for /f "tokens=*" %%A in ('mysql --version') do (
        echo   ✅ %%A
    )
)

REM Verificar Git (Opcional)
echo.
echo [3/5] Verificando Git (Opcional)...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ⚠️  Git no encontrado (no es crítico)
    echo      Recomendado desde: https://git-scm.com/download/win
) else (
    for /f "tokens=*" %%A in ('git --version') do (
        echo   ✅ %%A
    )
)

REM Verificar pip
echo.
echo [4/5] Verificando pip (gestor de paquetes Python)...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ❌ ERROR: pip no está disponible
    set requirements_ok=0
) else (
    for /f "tokens=*" %%A in ('pip --version') do (
        echo   ✅ %%A
    )
)

REM Verificar espacio en disco
echo.
echo [5/5] Verificando espacio en disco...
for /f "usebackq delims== tokens=2" %%A in (`wmic logicaldisk get name ^| find "C"`) do (
    echo   ✅ Disco C: disponible
)

echo.
echo ========================================================================

if %requirements_ok% equ 0 (
    echo.
    echo ❌ FALTA INSTALAR REQUISITOS
    echo.
    echo Por favor instala los programas marcados como ERROR antes de continuar.
    echo.
    echo 📋 Guía de instalación:
    echo    1. Python: https://www.python.org/downloads/
    echo    2. MySQL: https://dev.mysql.com/downloads/mysql/
    echo    3. Git (Opcional): https://git-scm.com/download/win
    echo.
    echo Después, ejecuta este script nuevamente.
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ✅ TODOS LOS REQUISITOS ESTÁN INSTALADOS
    echo.
    echo Próximos pasos:
    echo    1. Abre CMD en la carpeta del proyecto
    echo    2. Ejecuta: pip install -r requirements.txt
    echo    3. Configura el archivo .env
    echo    4. Crea la base de datos
    echo    5. Ejecuta: python launch_desktop.py
    echo.
    echo Para más información, lee: GUIA_INSTALACION_CLIENTE.md
    echo.
    pause
    exit /b 0
)
