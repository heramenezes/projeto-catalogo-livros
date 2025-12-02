@echo off
echo ========================================
echo Executando Testes de Carga - JMeter
echo ========================================
echo.

REM Limpar resultados anteriores
if exist resultados.jtl del resultados.jtl
if exist relatorio-html rmdir /s /q relatorio-html

echo Iniciando testes...
echo.

REM Executar JMeter em modo non-GUI com geração de relatório HTML
"%USERPROFILE%\JMeter\apache-jmeter-5.6.3\bin\jmeter.bat" -n -t teste-carga.jmx -l resultados.jtl -e -o relatorio-html

echo.
echo ========================================
echo Testes concluídos!
echo ========================================
echo.
echo Relatório HTML gerado em: relatorio-html\index.html
echo.
echo Abrindo relatório no navegador...
start relatorio-html\index.html

pause
