@echo off
cd /d c:\Users\india\Desktop\REFACCIONARIA
echo Agregando productos a la base de datos...
python -c "import sys; sys.path.insert(0, 'c:/Users/india/Desktop/REFACCIONARIA'); exec(open('scripts/agregar_productos_iniciales.py').read())"
pause
