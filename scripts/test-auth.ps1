param(
    [string]$Username = "admin",
    [string]$Password = "change_me_now",
    [string]$BaseUrl = "http://localhost:8000"
)

Write-Host "🔐 Probando autenticación..." -ForegroundColor Cyan
Write-Host "   Usuario: $Username" -ForegroundColor Gray
Write-Host "   URL: $BaseUrl/api/auth/login" -ForegroundColor Gray
Write-Host ""

# 1. Intentar login
Write-Host "1. Intentando login..." -ForegroundColor Yellow
$body = @{ 
    username = $Username
    password = $Password 
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/auth/login" -Body $body -ContentType "application/json" -ErrorAction Stop
    Write-Host "   ✅ Login exitoso!" -ForegroundColor Green
    $token = $response.access_token
    Write-Host "   Token: $($token.Substring(0, 30))..." -ForegroundColor Gray
    
    # 2. Obtener información del usuario
    Write-Host ""
    Write-Host "2. Obteniendo información del usuario..." -ForegroundColor Yellow
    $me = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/auth/me" -Headers @{ Authorization = "Bearer $token" } -ErrorAction Stop
    Write-Host "   ✅ Usuario autenticado:" -ForegroundColor Green
    Write-Host "   ID: $($me.id)" -ForegroundColor Gray
    Write-Host "   Username: $($me.username)" -ForegroundColor Gray
    Write-Host "   Email: $($me.email)" -ForegroundColor Gray
    Write-Host "   Rol: $($me.rol)" -ForegroundColor Gray
    Write-Host "   Activo: $($me.activo)" -ForegroundColor Gray
    
    # 3. Mostrar respuesta completa en JSON
    Write-Host ""
    Write-Host "3. Respuesta completa (JSON):" -ForegroundColor Yellow
    $me | ConvertTo-Json -Depth 5
    
    Write-Host ""
    Write-Host "✅ Prueba completada exitosamente!" -ForegroundColor Green
    
} catch {
    Write-Host "   ❌ Error en la autenticación" -ForegroundColor Red
    $err = $_.Exception.Response
    if ($err) {
        $sr = New-Object System.IO.StreamReader($err.GetResponseStream())
        $respBody = $sr.ReadToEnd()
        Write-Host "   Detalle: $respBody" -ForegroundColor Red
        Write-Host "   Status Code: $($err.StatusCode.value__)" -ForegroundColor Red
    } else {
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
