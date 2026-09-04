<#
Simple PowerShell script to test authentication endpoints locally.
Usage: pwsh ./scripts/test-auth.ps1 -Username admin -Password change_me_now
#>
param(
  [Parameter(Mandatory=$true)][string]$Username,
  [Parameter(Mandatory=$true)][string]$Password,
  [string]$ApiUrl = "http://localhost:8000"
)

$body = @{ username = $Username; password = $Password } | ConvertTo-Json
try {
  $response = Invoke-RestMethod -Method Post -Uri "$ApiUrl/api/auth/login" -Body $body -ContentType "application/json" -ErrorAction Stop
  Write-Host "✅ LOGIN OK"
  $token = $response.access_token
  Write-Host "Token prefix: $($token.Substring(0,20))..."

  $me = Invoke-RestMethod -Method Get -Uri "$ApiUrl/api/auth/me" -Headers @{ Authorization = "Bearer $token" } -ErrorAction Stop
  Write-Host "✅ Usuario autenticado:"
  $me | ConvertTo-Json -Depth 5
} catch {
  $err = $_.Exception.Response
  if ($err -ne $null) {
    $sr = New-Object System.IO.StreamReader($err.GetResponseStream())
    $respBody = $sr.ReadToEnd()
    Write-Host "❌ Error HTTP. Cuerpo de respuesta:`n$respBody"
  } else {
    Write-Host "❌ Error:" $_.Exception.Message
  }
}
