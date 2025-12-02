# Análise de Resultados com Python

Sistema automatizado de análise e visualização de resultados dos testes JMeter.

## Arquivos

### analisar-resultados.py
Script Python principal que:
- Lê arquivo JTL do JMeter
- Calcula métricas avançadas
- Gera 8 gráficos profissionais
- Cria relatório textual detalhado

### requirements.txt
Dependências Python necessárias:
- pandas - Manipulação de dados
- matplotlib - Gráficos
- seaborn - Visualizações avançadas
- numpy - Operações numéricas

### analise-graficos/
Pasta com gráficos gerados (criada automaticamente).

## Instalação

```bash
cd tests/analysis
pip install -r requirements.txt
```

## Execução

```bash
python analisar-resultados.py
```

**Pré-requisito:** Arquivo `../jmeter/resultados.jtl` deve existir.

## Gráficos Gerados

### 1. Dashboard Completo (`01-dashboard-completo.png`)
Painel com 6 visualizações:
- Total de requisições
- Taxa de erro (com limites)
- Throughput
- Tempos médio e máximo
- Sucessos vs Falhas
- Percentis (P90, P95, P99)

### 2. Comparativo de Performance (`02-comparativo-performance.png`)
4 gráficos horizontais:
- Tempo médio de resposta
- Taxa de erro (cores indicativas)
- Throughput
- Total de requisições

### 3. Distribuição de Percentis (`03-distribuicao-percentis.png`)
Barras agrupadas com P50, P90, P95, P99.

### 4. Taxa de Erro e Throughput (`04-erro-throughput.png`)
Evolução temporal com linhas de limite.

### 5. Heatmap de Endpoints (`05-heatmap-endpoints.png`)
Mapa de calor: tempo por endpoint.

### 6. Análise de Escalabilidade (`06-analise-escalabilidade.png`)
4 gráficos:
- Escalabilidade de throughput
- Degradação de estabilidade
- Degradação de performance
- Índice de eficiência

### 7. Comparativo de Tempos (`07-comparativo-tempos.png`)
6 métricas: Min, Médio, P90, P95, P99, Max.

### 8. Gráfico Radar (`08-radar-performance.png`)
Análise multidimensional por teste.

## Relatório Textual

**Arquivo:** `analise-graficos/relatorio-completo.txt`

**Conteúdo:**
- Métricas gerais por teste
- Tempos de resposta detalhados
- Análise por endpoint
- Comparações entre testes

## Métricas Calculadas

### Básicas
- Total de requisições
- Requisições bem-sucedidas
- Taxa de erro (%)
- Throughput (req/s)

### Tempos de Resposta
- Mínimo
- Médio
- Máximo
- P50 (Mediana)
- P90
- P95
- P99

### Por Endpoint
- Contagem
- Tempo médio
- Tempo máximo
- Taxa de erro

## Customização

### Alterar Resolução

Linha 16-17 em `analisar-resultados.py`:
```python
plt.rcParams['figure.dpi'] = 300  # 150 para web, 600 para impressão
```

### Alterar Paleta de Cores

Linha 14:
```python
sns.set_palette("husl")  # Opções: "Set2", "Paired", "viridis"
```

### Adicionar Gráfico

Crie método na classe `GeradorGraficos`:
```python
def grafico_09_meu_grafico(self):
    fig, ax = plt.subplots(figsize=(12, 6))
    # Seu código
    plt.savefig(self.output_dir / '09-meu-grafico.png')
```

Adicione em `gerar_todos_graficos()`:
```python
self.grafico_09_meu_grafico()
```

## Formato JTL

O script espera CSV com colunas:
- `timeStamp` - Timestamp da requisição
- `elapsed` - Tempo de resposta (ms)
- `label` - Nome do endpoint
- `success` - Boolean de sucesso

## Análise Individual por Teste

Para analisar testes separadamente:

```python
gerador = GeradorGraficos('analise-teste1')
gerador.adicionar_teste('Teste 1', '../jmeter/teste1.jtl')
gerador.gerar_todos_graficos()
```

## Exportar para Excel

Adicione ao script:
```python
import pandas as pd
df = pd.DataFrame(gerador.resultados).T
df.to_excel('analise-graficos/resultados.xlsx')
```

## Comparar Versões

Para comparar antes/depois:
```python
gerador.adicionar_teste('Versão 1.0', 'v1-resultados.jtl')
gerador.adicionar_teste('Versão 2.0', 'v2-resultados.jtl')
```

## Solução de Problemas

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### FileNotFoundError
Execute os testes JMeter primeiro.

### Gráficos não aparecem
Verifique pasta `analise-graficos/`.

### Encoding error no relatório
```powershell
Get-Content analise-graficos\relatorio-completo.txt -Encoding UTF8
```

## Performance

- Processa ~10.000 requisições em 2-5 segundos
- Gera 8 gráficos em 10-15 segundos
- Usa ~100MB de memória

## Documentação

Ver: [../../docs/GUIA_ANALISE_PYTHON.md](../../docs/GUIA_ANALISE_PYTHON.md)
