Write-Host "🚀 Iniciando configuración del entorno..."

$envFile = Join-Path $PSScriptRoot '..\.env'
if (-Not (Test-Path $envFile)) {
  Write-Error ".env not found at $envFile"
  exit 1
}

Get-Content $envFile | ForEach-Object {
  if ($_ -match '^\s*#' -or $_ -match '^\s*$') { return }
  $parts = $_ -split '=',2
  if ($parts.Count -eq 2) {
    $name = $parts[0].Trim()
    $value = $parts[1].Trim()
    [System.Environment]::SetEnvironmentVariable($name, $value, 'Process')
  }
}
Write-Host "✅ Environment variables loaded into process scope."

# Ejecutar create_admin.py desde la raíz del repo si existe
$repoRoot = Join-Path $PSScriptRoot '..'
$createAdminPath = Join-Path $repoRoot 'create_admin.py'

if (Test-Path $createAdminPath) {
  Write-Host "👤 Ejecutando create_admin.py desde la raíz del repo..."
  Push-Location $repoRoot
  try {
    python .\create_admin.py
  } catch {
    Write-Host "⚠️ Error al ejecutar create_admin.py: $_"
  } finally {
    Pop-Location
  }
} else {
  Write-Host "⚠️ No se encontró create_admin.py en la raíz del repo; ejecuta manualmente: python .\\create_admin.py"
}

Write-Host "🎉 Configuración completada!"
