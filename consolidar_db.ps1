# Script para consolidar la base de datos
cd 'c:\Users\india\Documents\GitHub\Refaccionaria-Oviedo'

# Leer archivos
$original = Get-Content refaccionaria_db.sql
$datos = Get-Content 'REFACCIONARIA\datos_exportados_inserts.sql' | Select-Object -Skip 4

# Crear nuevo archivo tempoporal combinando estructura + datos
$original | Set-Content "refaccionaria_db_temp.sql"
$datos | Add-Content "refaccionaria_db_temp.sql"

# Reemplazar el original
Move-Item -Force "refaccionaria_db_temp.sql" "refaccionaria_db.sql"

# Verificar resultado
$lineas = (Get-Content refaccionaria_db.sql | Measure-Object -Line).Lines
Write-Host "Archivo consolidado: $lineas lineas"

# Verificar que tenga inventario_local
$inventario = (Get-Content refaccionaria_db.sql | Select-String 'INSERT INTO inventario_local').Count
Write-Host "Registros inventario_local: $inventario"
