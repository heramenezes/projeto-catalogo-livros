# Guia de Execução dos Testes de Carga

Este documento descreve o processo completo para executar os testes de carga utilizando Apache JMeter e gerar relatórios HTML detalhados.

## Pré-requisitos

- Node.js (versão 14 ou superior)
- Apache JMeter 5.6.3 ou superior
- Java JDK 8 ou superior (necessário para executar o JMeter)

## Estrutura do Projeto

```
projeto-laura-antonio/
├── server.js              # Servidor Node.js/Express
├── teste-carga.jmx        # Arquivo de configuração dos testes JMeter
├── executar-teste.ps1     # Script PowerShell para Windows
├── executar-teste.sh      # Script Bash para Linux
└── package.json           # Dependências do projeto
```

## Passo 1: Instalação das Dependências

Antes de executar os testes, instale as dependências do projeto Node.js:

```bash
npm install
```

## Passo 2: Iniciar a Aplicação

A aplicação deve estar em execução antes de iniciar os testes de carga.

### Iniciar o Servidor

```bash
npm start
```

O servidor será iniciado na porta 3000. Aguarde até ver a mensagem:

```
Servidor rodando em http://localhost:3000
Catálogo de Livros - Sistema de Gestão de Leituras
```

**Importante:** Mantenha o servidor em execução durante toda a duração dos testes. Não feche o terminal onde o servidor está rodando.

## Passo 3: Executar os Testes e Gerar Relatórios

### Windows

#### Opção 1: Usando Script PowerShell (Recomendado)

1. Abra um novo terminal PowerShell no diretório do projeto
2. Execute o script:

```powershell
powershell -ExecutionPolicy Bypass -File executar-teste.ps1
```

O script irá:
- Limpar resultados anteriores
- Executar todos os testes configurados
- Gerar o relatório HTML automaticamente
- Abrir o relatório no navegador padrão

#### Opção 2: Comando Manual

```powershell
& "$env:USERPROFILE\JMeter\apache-jmeter-5.6.3\bin\jmeter.bat" -n -t teste-carga.jmx -l resultados.jtl -e -o relatorio-html
```

### Linux

#### Opção 1: Usando Script Bash (Recomendado)

1. Torne o script executável (apenas na primeira vez):

```bash
chmod +x executar-teste.sh
```

2. Execute o script:

```bash
./executar-teste.sh
```

#### Opção 2: Comando Manual

```bash
~/JMeter/apache-jmeter-5.6.3/bin/jmeter -n -t teste-carga.jmx -l resultados.jtl -e -o relatorio-html
```

**Nota:** Ajuste o caminho do JMeter conforme a localização da sua instalação.

## Passo 4: Visualizar os Relatórios

Após a conclusão dos testes, o relatório HTML será gerado no diretório `relatorio-html/`.

### Windows

O relatório será aberto automaticamente no navegador. Caso não abra, execute:

```powershell
Start-Process relatorio-html\index.html
```

Ou navegue manualmente até o arquivo e abra-o com um navegador web.

### Linux

```bash
xdg-open relatorio-html/index.html
```

Ou abra o arquivo `relatorio-html/index.html` diretamente no navegador de sua preferência.

## Parâmetros do JMeter

### Explicação dos Parâmetros Utilizados

- `-n` : Executa o JMeter em modo non-GUI (linha de comando)
- `-t teste-carga.jmx` : Especifica o arquivo de teste a ser executado
- `-l resultados.jtl` : Define o arquivo onde os resultados serão salvos
- `-e` : Gera o relatório HTML após a execução dos testes
- `-o relatorio-html` : Define o diretório de saída para o relatório HTML

## Interpretação dos Resultados

O relatório HTML gerado contém diversas seções com métricas detalhadas:

- **Test and Report information**: Informações gerais sobre o teste
- **APDEX**: Índice de satisfação do desempenho da aplicação
- **Requests Summary**: Resumo total de requisições, sucessos e falhas
- **Statistics**: Estatísticas detalhadas por endpoint
- **Response Time**: Gráficos de tempo de resposta ao longo do tempo
- **Throughput**: Taxa de requisições processadas por segundo
- **Latency**: Tempo de latência das requisições

## Testes Configurados

O arquivo `teste-carga.jmx` contém 8 cenários de teste diferentes:

1. **Carga Espersa**: 20 usuários, carga constante
2. **Rajada**: 100 usuários em 2 segundos
3. **Estresse**: 50 usuários com carga crescente
4. **Baseline**: 5 usuários em condições normais
5. **Volume**: 10 usuários com 100 requisições cada
6. **Escalabilidade - Fase 1**: 10 usuários
7. **Escalabilidade - Fase 2**: 30 usuários
8. **Escalabilidade - Fase 3**: 60 usuários

## Solução de Problemas

### Erro: "Connection refused" ou 100% de falhas

**Causa:** O servidor Node.js não está em execução.

**Solução:** Certifique-se de que executou `npm start` antes de iniciar os testes.

### Erro: "Command not found: jmeter"

**Causa:** O JMeter não está instalado ou não está no PATH do sistema.

**Solução:** Verifique a instalação do JMeter e ajuste o caminho no script de execução.

### Erro: "Java not found"

**Causa:** Java JDK não está instalado ou não está configurado no PATH.

**Solução:** Instale o Java JDK e configure a variável de ambiente JAVA_HOME.

### Relatório HTML não é gerado

**Causa:** O diretório de saída já existe e contém arquivos.

**Solução:** Delete o diretório `relatorio-html` antes de executar novamente:

**Windows:**
```powershell
Remove-Item -Recurse -Force relatorio-html
```

**Linux:**
```bash
rm -rf relatorio-html
```

## Notas Adicionais

- Os testes podem levar de 2 a 5 minutos para serem concluídos, dependendo da configuração do sistema.
- Durante a execução, é normal ver avisos (WARN) relacionados ao scan de plugins. Eles não afetam os resultados.
- O arquivo `resultados.jtl` contém os dados brutos dos testes e pode ser recarregado no JMeter para análise adicional.
- Recomenda-se executar os testes em um ambiente isolado para obter resultados consistentes.

## Arquivo de Script Bash para Linux

Crie o arquivo `executar-teste.sh` com o seguinte conteúdo:

```bash
#!/bin/bash

echo "========================================"
echo "Executando Testes de Carga - JMeter"
echo "========================================"
echo ""

# Limpar resultados anteriores
if [ -f "resultados.jtl" ]; then
    rm resultados.jtl
    echo "Arquivo anterior removido: resultados.jtl"
fi

if [ -d "relatorio-html" ]; then
    rm -rf relatorio-html
    echo "Diretório anterior removido: relatorio-html"
fi

echo ""
echo "Iniciando testes..."
echo "Aguarde... Isso pode levar alguns minutos."
echo ""

# Executar JMeter em modo non-GUI
~/JMeter/apache-jmeter-5.6.3/bin/jmeter -n -t teste-carga.jmx -l resultados.jtl -e -o relatorio-html

echo ""
echo "========================================"
echo "Testes concluídos!"
echo "========================================"
echo ""
echo "Relatório HTML gerado em: relatorio-html/index.html"
echo ""

# Abrir relatório no navegador
if [ -f "relatorio-html/index.html" ]; then
    echo "Abrindo relatório no navegador..."
    xdg-open relatorio-html/index.html
else
    echo "ERRO: Relatório não foi gerado!"
fi

echo ""
read -p "Pressione ENTER para sair..."
```

## Customização dos Testes

Para modificar os parâmetros dos testes (número de usuários, duração, etc.), edite o arquivo `teste-carga.jmx` diretamente no JMeter GUI:

```bash
# Windows
& "$env:USERPROFILE\JMeter\apache-jmeter-5.6.3\bin\jmeter.bat"

# Linux
~/JMeter/apache-jmeter-5.6.3/bin/jmeter
```

Abra o arquivo `teste-carga.jmx` através do menu File > Open.
