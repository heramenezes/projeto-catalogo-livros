# Testes de Carga JMeter

Testes automatizados de carga usando Apache JMeter.

## Arquivos

### teste-carga.jmx
Configuração do JMeter com 8 cenários de teste:

1. **Carga Espersa** - 20 usuários, 10s ramp-up
2. **Rajada** - 100 usuários, 2s ramp-up
3. **Estresse** - 50 usuários, 30s ramp-up
4. **Baseline** - 5 usuários (referência)
5. **Volume** - 10 usuários × 100 requisições
6. **Escalabilidade 1** - 10 usuários
7. **Escalabilidade 2** - 30 usuários
8. **Escalabilidade 3** - 60 usuários

### executar-teste.ps1
Script PowerShell para execução automatizada (Windows).

### executar-teste.bat
Script batch alternativo (Windows).

### resultados.jtl
Arquivo de resultados brutos (gerado após execução).

### relatorio-html/
Relatório HTML interativo (gerado após execução).

## Pré-requisitos

1. Apache JMeter 5.6+ instalado
2. Java JDK 8+ instalado
3. Servidor rodando em localhost:3000

## Execução

### Método 1: Script PowerShell (Recomendado)

```powershell
powershell -ExecutionPolicy Bypass -File executar-teste.ps1
```

### Método 2: Linha de Comando

```powershell
& "$env:USERPROFILE\JMeter\apache-jmeter-5.6.3\bin\jmeter.bat" -n -t teste-carga.jmx -l resultados.jtl -e -o relatorio-html
```

### Método 3: Interface Gráfica

```powershell
& "$env:USERPROFILE\JMeter\apache-jmeter-5.6.3\bin\jmeter.bat"
# File > Open > teste-carga.jmx
# Clique no botão Start
```

## Resultados

### Relatório HTML
Abra `relatorio-html/index.html` no navegador após a execução.

**Seções principais:**
- Dashboard
- APDEX
- Statistics
- Response Times
- Throughput
- Latency

### Arquivo JTL
Contém dados brutos que podem ser:
- Recarregados no JMeter
- Processados com Python
- Analisados com ferramentas externas

## Configuração

### Variáveis Globais

Definidas no Test Plan:
- `SERVER`: localhost
- `PORT`: 3000

Para mudar o servidor, edite essas variáveis no JMeter GUI.

### Threads por Teste

Edite no JMeter GUI:
1. Abra `teste-carga.jmx`
2. Selecione um Thread Group
3. Ajuste:
   - Number of Threads (Usuários)
   - Ramp-up Period (Segundos)
   - Loop Count (Iterações)

## Endpoints Testados

- GET `/api/livros` - Lista de livros
- GET `/api/livros/:id` - Livro específico
- GET `/api/estatisticas` - Estatísticas
- GET `/heavy-cpu` - Teste de CPU
- GET `/heavy-io` - Teste de I/O
- GET `/many-items` - Teste de volume
- GET `/status` - Healthcheck

## Limpeza

Para limpar resultados anteriores:

```powershell
Remove-Item resultados.jtl -Force
Remove-Item -Recurse relatorio-html -Force
```

## Solução de Problemas

### 100% de erros
- Verifique se o servidor está rodando
- Teste manualmente: http://localhost:3000/api/livros

### JMeter não inicia
- Verifique instalação do Java: `java -version`
- Ajuste JAVA_HOME se necessário

### Relatório não gerado
- Delete pasta `relatorio-html` antes de executar
- Verifique permissões de escrita

## Documentação

Ver: [../../docs/GUIA_EXECUCAO_TESTES.md](../../docs/GUIA_EXECUCAO_TESTES.md)
