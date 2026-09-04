# Bootstrap .env into PowerShell process scope and optionally run create_admin.py
# Usage: from the repository root run: pwsh ./scripts/bootstrap-env.ps1
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
Write-Host "Environment variables loaded into process scope."

# Optional: run create_admin.py non-interactive if password present
if ([System.Environment]::GetEnvironmentVariable('INITIAL_ADMIN_PASSWORD','Process')) {
  Write-Host "Running create_admin.py (non-interactive)..."
  python .\create_admin.py
} else {
  Write-Host "INITIAL_ADMIN_PASSWORD not set — skipping create_admin.py"
}
