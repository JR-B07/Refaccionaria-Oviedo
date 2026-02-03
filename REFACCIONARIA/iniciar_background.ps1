# Script PowerShell para ejecutar Refaccionaria en segundo plano
# Sin mostrar ventana de consola
# El proceso continúa ejecutándose incluso después de cerrar este script

param(
    [switch]$ShowWindow = $false
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Verificar Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion"
} catch {
    Write-Host "✗ Python no encontrado. Instálalo desde https://www.python.org/"
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar dependencias
$hasWebview = python -c "import webview" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚡ Instalando dependencias..."
    pip install -q pywebview requests
    Write-Host "✓ Dependencias instaladas"
}

# Función para iniciar el proceso en background
function Start-BackgroundProcess {
    param(
        [string]$FilePath,
        [string]$ArgumentList
    )
    
    # Crear proceso sin ventana
    $processStartInfo = New-Object System.Diagnostics.ProcessStartInfo
    $processStartInfo.FileName = $FilePath
    $processStartInfo.Arguments = $ArgumentList
    $processStartInfo.UseShellExecute = $false
    $processStartInfo.RedirectStandardOutput = $true
    $processStartInfo.RedirectStandardError = $true
    $processStartInfo.CreateNoWindow = $true
    $processStartInfo.WindowStyle = 'Hidden'
    
    $process = [System.Diagnostics.Process]::Start($processStartInfo)
    return $process
}

# Iniciar la aplicación
Write-Host "🚀 Iniciando Refaccionaria ERP..."
Write-Host ""

$process = Start-BackgroundProcess -FilePath "python.exe" -ArgumentList "launch_desktop.py"

Write-Host "✓ Sistema iniciado en segundo plano (PID: $($process.Id))"
Write-Host "✓ La ventana se abrirá en unos segundos..."
Write-Host ""
