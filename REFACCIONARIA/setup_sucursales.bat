@echo off
echo ====================================
echo  CONFIGURACION DE SUCURSALES
echo ====================================
echo.

REM Activar entorno virtual
call venv\Scripts\activate.bat

echo [1/2] Creando sucursales...
python scripts\crear_sucursales.py
echo.

echo [2/2] Asignando usuarios a sucursales...
python scripts\asignar_sucursales_usuarios.py
echo.

echo ====================================
echo  PROCESO COMPLETADO
echo ====================================
pause
