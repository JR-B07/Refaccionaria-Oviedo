# Script PowerShell para crear acceso directo con icono personalizado

$WshShell = New-Object -ComObject WScript.Shell
$Escritorio = [Environment]::GetFolderPath("Desktop")
$AccesoDirecto = $WshShell.CreateShortcut("$Escritorio\Refaccionaria Oviedo.lnk")

# Configurar acceso directo
$RutaActual = $PSScriptRoot
$AccesoDirecto.TargetPath = "$RutaActual\Refaccionaria.bat"
$AccesoDirecto.WorkingDirectory = $RutaActual
$AccesoDirecto.Description = "Sistema ERP Refaccionaria Oviedo"
$AccesoDirecto.IconLocation = "$RutaActual\logo-refaccionaria.ico"

# Guardar acceso directo
$AccesoDirecto.Save()

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "  ACCESO DIRECTO CREADO EXITOSAMENTE" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ubicacion: $Escritorio\Refaccionaria Oviedo.lnk" -ForegroundColor Cyan
Write-Host "Icono: logo-refaccionaria.ico" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ya puedes usar el acceso directo desde tu Escritorio" -ForegroundColor Yellow
Write-Host ""

# Pausar para que el usuario vea el mensaje
Read-Host "Presiona Enter para salir"
