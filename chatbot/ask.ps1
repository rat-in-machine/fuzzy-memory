param([string]$query = "")

if (-not $query) {
    Write-Host "Uso: .\ask.ps1 'Tu pregunta aquí'"
    Write-Host ""
    Write-Host "Ejemplos:"
    Write-Host '  .\ask.ps1 "dame juegos de rol"'
    Write-Host '  .\ask.ps1 "precio de elden ring"'
    exit
}

$json = @{
    query = $query
} | ConvertTo-Json

Write-Host "➤ Pregunta: $query"
Write-Host ""

$json | Set-Content -Path "q.json"
curl.exe -s -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" --data "@q.json" | ConvertFrom-Json | Select-Object response -ExpandProperty response

Remove-Item "q.json" -Force -ErrorAction SilentlyContinue
