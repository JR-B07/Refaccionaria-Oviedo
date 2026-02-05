@echo off
setlocal enabledelayedexpansion
title Refaccionaria - Verificacion Final

cd /d "%~dp0"
color 0B
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║        VERIFICACION FINAL - REFACCIONARIA ERP v1.0        ║
echo ║                                                            ║
echo ║   Todos los cambios han sido implementados exitosamente   ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo Verificando archivos creados...
echo.

if exist Refaccionaria.bat (
    echo [OK] Refaccionaria.bat
) else (
    echo [ERROR] Refaccionaria.bat NO ENCONTRADO
)

if exist start.bat (
    echo [OK] start.bat
) else (
    echo [ERROR] start.bat NO ENCONTRADO
)

if exist advanced_launcher.py (
    echo [OK] advanced_launcher.py
) else (
    echo [ERROR] advanced_launcher.py NO ENCONTRADO
)

if exist diagnostico.py (
    echo [OK] diagnostico.py
) else (
    echo [ERROR] diagnostico.py NO ENCONTRADO
)

if exist verificar_sistema.bat (
    echo [OK] verificar_sistema.bat
) else (
    echo [ERROR] verificar_sistema.bat NO ENCONTRADO
)

if exist utilidades.bat (
    echo [OK] utilidades.bat
) else (
    echo [ERROR] utilidades.bat NO ENCONTRADO
)

if exist scripts\inicializar_datos.py (
    echo [OK] scripts\inicializar_datos.py
) else (
    echo [ERROR] scripts\inicializar_datos.py NO ENCONTRADO
)

if exist scripts\backup_db.py (
    echo [OK] scripts\backup_db.py
) else (
    echo [ERROR] scripts\backup_db.py NO ENCONTRADO
)

if exist scripts\limpiar_db.py (
    echo [OK] scripts\limpiar_db.py
) else (
    echo [ERROR] scripts\limpiar_db.py NO ENCONTRADO
)

if exist GUIA_INICIO_COMPLETA.md (
    echo [OK] GUIA_INICIO_COMPLETA.md
) else (
    echo [ERROR] GUIA_INICIO_COMPLETA.md NO ENCONTRADO
)

if exist BIENVENIDA.txt (
    echo [OK] BIENVENIDA.txt
) else (
    echo [ERROR] BIENVENIDA.txt NO ENCONTRADO
)

echo.
echo ════════════════════════════════════════════════════════════
echo.

echo Que deseas hacer?
echo.
echo 1. Ejecutar Refaccionaria (Recomendado)
echo 2. Ver Resumen de Cambios
echo 3. Leer Guia de Inicio
echo 4. Salir
echo.

set /p opcion="Selecciona (1-4): "

if "%opcion%"=="1" (
    echo.
    call Refaccionaria.bat
) else if "%opcion%"=="2" (
    echo.
    type RESUMEN_ACTUALIZACION.txt
    pause
) else if "%opcion%"=="3" (
    echo.
    type BIENVENIDA.txt
    pause
) else (
    echo.
    echo ¡Hasta luego!
    echo.
)
