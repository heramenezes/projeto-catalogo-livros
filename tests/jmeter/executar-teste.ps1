# Script para executar testes JMeter e gerar relatório HTML
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Executando Testes de Carga - JMeter" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Limpar resultados anteriores
if (Test-Path "tests\jmeter\resultados.jtl") {
    Remove-Item "tests\jmeter\resultados.jtl" -Force
    Write-Host "Arquivo anterior removido: resultados.jtl" -ForegroundColor Yellow
}

if (Test-Path "tests\jmeter\relatorio-html") {
    Remove-Item "tests\jmeter\relatorio-html" -Recurse -Force
    Write-Host "Diretório anterior removido: relatorio-html" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Iniciando testes..." -ForegroundColor Green
Write-Host "Aguarde... Isso pode levar alguns minutos." -ForegroundColor Yellow
Write-Host ""

# Executar JMeter em modo non-GUI
$jmeterPath = "$env:USERPROFILE\JMeter\apache-jmeter-5.6.3\bin\jmeter.bat"
$arguments = "-n -t tests/jmeter/teste-carga.jmx -l tests/jmeter/resultados.jtl -e -o tests/jmeter/relatorio-html"

Start-Process -FilePath $jmeterPath -ArgumentList $arguments -Wait -NoNewWindow

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Testes concluídos!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Relatório HTML gerado em: relatorio-html\index.html" -ForegroundColor Cyan
Write-Host ""

# Abrir relatório no navegador
if (Test-Path "tests\jmeter\relatorio-html\index.html") {
    Write-Host "Abrindo relatório no navegador..." -ForegroundColor Green
    Start-Process "tests\jmeter\relatorio-html\index.html"
} else {
    Write-Host "ERRO: Relatório não foi gerado!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Pressione qualquer tecla para sair..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
