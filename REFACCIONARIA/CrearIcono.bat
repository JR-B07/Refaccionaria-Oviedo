@echo off
chcp 65001 >nul
title Crear Icono y Acceso Directo - Refaccionaria Oviedo

echo.
echo ========================================================================
echo            CREAR ICONO Y ACCESO DIRECTO
echo                Refaccionaria Oviedo
echo ========================================================================
echo.

REM Verificar si existe Pillow
python -c "import PIL" 2>nul
if %errorlevel% neq 0 (
    echo [!] Instalando Pillow para convertir imágenes...
    pip install Pillow
    echo.
)

REM Convertir PNG a ICO
echo [1/2] Convirtiendo logo PNG a formato ICO...
python convertir_logo_ico.py
echo.

REM Verificar si se creó el ICO
if not exist "logo-refaccionaria.ico" (
    echo [X] Error: No se pudo crear el archivo ICO
    pause
    exit /b 1
)

REM Crear acceso directo
echo [2/2] Creando acceso directo en el Escritorio...
powershell -ExecutionPolicy Bypass -File "crear_acceso_directo.ps1"

echo.
echo ========================================================================
echo   PROCESO COMPLETADO
echo ========================================================================
echo.
echo Ahora tienes:
echo   - logo-refaccionaria.ico (icono de Windows)
echo   - Acceso directo en el Escritorio con el logo
echo.

pause
