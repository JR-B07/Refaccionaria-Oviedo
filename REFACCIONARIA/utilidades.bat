@echo off
setlocal enabledelayedexpansion
title Refaccionaria - Menu Utilidades

cd /d "%~dp0"

color 0B
cls

:menu
echo.
echo ========================================
echo   REFACCIONARIA - MENU DE UTILIDADES
echo ========================================
echo.
echo   1. Iniciar Refaccionaria (Recomendado)
echo   2. Iniciar Servidor API
echo   3. Iniciar desde Browser
echo.
echo   4. Verificar Sistema
echo   5. Ejecutar Diagnostico
echo.
echo   6. Hacer Backup
echo   7. Inicializar Datos
echo   8. Limpiar Base de Datos
echo.
echo   9. Ver Resumen de Cambios
echo   0. Salir
echo.
set /p opcion="Selecciona una opcion (0-9): "

if "%opcion%"=="1" (
    echo.
    echo Iniciando Refaccionaria ERP...
    echo.
    call Refaccionaria.bat
) else if "%opcion%"=="2" (
    echo.
    echo Iniciando Servidor API...
    echo.
    call start.bat
) else if "%opcion%"=="3" (
    echo.
    echo Abriendo en Browser...
    echo.
    call InicioRapido.bat
) else if "%opcion%"=="4" (
    echo.
    echo Verificando Sistema...
    echo.
    call verificar_sistema.bat
) else if "%opcion%"=="5" (
    echo.
    echo Ejecutando Diagnostico...
    echo.
    python diagnostico.py
    pause
) else if "%opcion%"=="6" (
    echo.
    echo Haciendo Backup...
    echo.
    python scripts/backup_db.py
    pause
) else if "%opcion%"=="7" (
    echo.
    echo Inicializando Datos...
    echo.
    python scripts/inicializar_datos.py
    pause
) else if "%opcion%"=="8" (
    echo.
    echo ADVERTENCIA: Esto borrara TODOS los datos
    echo.
    python scripts/limpiar_db.py
    pause
) else if "%opcion%"=="9" (
    echo.
    echo Abriendo Resumen...
    echo.
    if exist RESUMEN_ACTUALIZACION.txt (
        notepad RESUMEN_ACTUALIZACION.txt
    ) else (
        echo No se encontro el archivo de resumen
        pause
    )
) else if "%opcion%"=="0" (
    echo.
    echo Hasta luego!
    echo.
    exit /b 0
) else (
    echo.
    echo Opcion invalida
    echo.
    pause
    cls
    goto menu
)

echo.
pause
cls
goto menu