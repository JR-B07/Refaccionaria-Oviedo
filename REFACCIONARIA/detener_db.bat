@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo   DETENIENDO BASE DE DATOS
echo ========================================
echo.

REM Intentar detener MySQL
sc query MySQL >nul 2>&1
if not errorlevel 1 (
    echo Deteniendo servicio MySQL...
    net stop MySQL
    if errorlevel 1 (
        echo [ERROR] No se pudo detener MySQL (puede requerir permisos de administrador)
        pause
        exit /b 1
    ) else (
        echo MySQL detenido correctamente
    )
) else (
    REM Intentar con MySQL80
    sc query MySQL80 >nul 2>&1
    if not errorlevel 1 (
        echo Deteniendo servicio MySQL80...
        net stop MySQL80
        if errorlevel 1 (
            echo [ERROR] No se pudo detener MySQL80 (puede requerir permisos de administrador)
            pause
            exit /b 1
        ) else (
            echo MySQL80 detenido correctamente
        )
    ) else (
        echo [ERROR] No se encontro servicio MySQL instalado
        pause
        exit /b 1
    )
)

echo.
echo Base de datos detenida correctamente
echo.
pause
