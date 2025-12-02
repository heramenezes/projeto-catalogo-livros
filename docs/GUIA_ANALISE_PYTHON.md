# Guia de Análise Avançada de Resultados

## Sistema de Análise Automatizada com Python

Este sistema extrai dados diretamente dos arquivos JTL gerados pelo JMeter e cria visualizações profissionais automaticamente.

## Diferenciais em Relação a Outras Soluções

### Vantagens sobre análises manuais:

1. **Extração Automática de Dados**
   - Lê arquivos JTL diretamente (formato nativo do JMeter)
   - Não requer entrada manual de dados
   - Processa milhares de requisições automaticamente

2. **Gráficos Profissionais e Avançados**
   - 8 tipos diferentes de visualizações
   - Dashboard completo em uma única imagem
   - Gráficos radar multidimensionais
   - Heatmaps de performance por endpoint
   - Análise de escalabilidade

3. **Métricas Avançadas**
   - Cálculo automático de percentis (P50, P90, P95, P99)
   - Throughput preciso
   - Análise por endpoint individual
   - Correlação entre múltiplas métricas

4. **Relatório Textual Detalhado**
   - Geração automática de relatório completo
   - Formatação profissional
   - Métricas organizadas por categoria

## Instalação

### Passo 1: Instalar Python

Se ainda não tiver Python instalado:

**Windows:**
```powershell
winget install Python.Python.3.11
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### Passo 2: Instalar Dependências

```bash
pip install -r requirements.txt
```

Ou instalar individualmente:

```bash
pip install pandas matplotlib seaborn numpy
```

## Como Usar

### Cenário 1: Análise de Todos os Testes Combinados

1. Execute os testes normalmente:
```powershell
powershell -ExecutionPolicy Bypass -File executar-teste.ps1
```

2. Execute a análise:
```bash
python analisar-resultados.py
```

3. Os gráficos serão gerados em: `analise-graficos/`

### Cenário 2: Análise Individual por Tipo de Teste

Para análise mais detalhada, execute cada teste separadamente e analise individualmente.

#### Windows:

```powershell
# Teste 1: Carga Espersa
& "$env:USERPROFILE\JMeter\apache-jmeter-5.6.3\bin\jmeter.bat" -n -t teste-carga.jmx -l teste1-carga-espersa.jtl -Jteste=1

# Teste 2: Rajada
& "$env:USERPROFILE\JMeter\apache-jmeter-5.6.3\bin\jmeter.bat" -n -t teste-carga.jmx -l teste2-rajada.jtl -Jteste=2

# Teste 3: Estresse
& "$env:USERPROFILE\JMeter\apache-jmeter-5.6.3\bin\jmeter.bat" -n -t teste-carga.jmx -l teste3-estresse.jtl -Jteste=3
```

#### Linux:

```bash
# Teste 1: Carga Espersa
~/JMeter/apache-jmeter-5.6.3/bin/jmeter -n -t teste-carga.jmx -l teste1-carga-espersa.jtl -Jteste=1

# Teste 2: Rajada
~/JMeter/apache-jmeter-5.6.3/bin/jmeter -n -t teste-carga.jmx -l teste2-rajada.jtl -Jteste=2

# Teste 3: Estresse
~/JMeter/apache-jmeter-5.6.3/bin/jmeter -n -t teste-carga.jmx -l teste3-estresse.jtl -Jteste=3
```

## Gráficos Gerados

### 1. Dashboard Completo (`01-dashboard-completo.png`)
Visão geral com 6 painéis:
- Total de requisições por teste
- Taxa de erro com limites visuais
- Throughput comparativo
- Tempos médio e máximo (escala logarítmica)
- Distribuição de sucessos e falhas
- Percentis P90, P95, P99

### 2. Comparativo de Performance (`02-comparativo-performance.png`)
4 gráficos horizontais comparando:
- Tempo médio de resposta
- Taxa de erro com cores indicativas
- Throughput
- Total de requisições

### 3. Distribuição de Percentis (`03-distribuicao-percentis.png`)
Gráfico de barras agrupadas mostrando P50, P90, P95 e P99 para cada teste.

### 4. Taxa de Erro e Throughput (`04-erro-throughput.png`)
Evolução temporal de:
- Taxa de erro com limites aceitável (5%) e crítico (20%)
- Throughput ao longo dos testes

### 5. Heatmap de Endpoints (`05-heatmap-endpoints.png`)
Mapa de calor mostrando tempo médio por endpoint em cada teste.
- Cores quentes: endpoints mais lentos
- Cores frias: endpoints mais rápidos

### 6. Análise de Escalabilidade (`06-analise-escalabilidade.png`)
4 gráficos analisando:
- Escalabilidade de throughput
- Degradação da estabilidade
- Degradação de performance
- Índice de eficiência relativa

### 7. Comparativo Detalhado de Tempos (`07-comparativo-tempos.png`)
Gráfico de barras com 6 métricas de tempo:
- Mínimo, Médio, P90, P95, P99, Máximo
- Escala logarítmica para melhor visualização

### 8. Gráfico Radar (`08-radar-performance.png`)
Gráficos radar individuais para cada teste mostrando:
- Estabilidade (inverso da taxa de erro)
- Throughput
- Performance (inverso do tempo médio)
- Consistência P95
- Consistência P99

## Interpretação dos Resultados

### Cores Utilizadas

**Taxa de Erro:**
- Verde: < 5% (excelente)
- Laranja: 5-20% (aceitável)
- Vermelho: > 20% (crítico)

**Performance:**
- Verde: Bom desempenho
- Amarelo/Laranja: Desempenho moderado
- Vermelho: Desempenho ruim

### Métricas Chave

**Estabilidade:**
- Taxa de erro < 1%: Sistema muito estável
- Taxa de erro < 5%: Sistema estável
- Taxa de erro > 20%: Sistema instável, requer ação

**Performance:**
- P95 < 500ms: Excelente
- P95 < 1000ms: Bom
- P95 > 2000ms: Requer otimização

**Throughput:**
- Crescente com carga: Boa escalabilidade
- Estável: Capacidade máxima atingida
- Decrescente: Gargalo identificado

## Relatório Textual

O arquivo `relatorio-completo.txt` contém:

1. **Cabeçalho**
   - Data de geração
   - Total de testes analisados

2. **Por Teste:**
   - Métricas gerais (requisições, erros, throughput)
   - Tempos de resposta (min, médio, max, percentis)
   - Análise por endpoint (se disponível)

## Comparação com Outras Soluções

| Característica | Solução Manual | Nossa Solução |
|----------------|----------------|---------------|
| Extração de dados | Manual | Automática |
| Tipos de gráficos | 4 básicos | 8 avançados |
| Percentis | Não | P50, P90, P95, P99 |
| Análise por endpoint | Limitada | Completa com heatmap |
| Gráfico radar | Não | Sim |
| Relatório textual | Não | Sim |
| Escalabilidade | Básica | Multidimensional |
| Resolução | 72 DPI | 300 DPI |
| Formato profissional | Não | Sim |

## Customização

### Alterar Resolução

No arquivo `analisar-resultados.py`, linha 16-17:
```python
plt.rcParams['figure.dpi'] = 300  # Altere para 150 (web) ou 600 (impressão)
plt.rcParams['savefig.dpi'] = 300
```

### Alterar Cores

Linha 14:
```python
sns.set_palette("husl")  # Opções: "Set2", "Paired", "viridis", "plasma"
```

### Adicionar Novos Gráficos

Crie um novo método na classe `GeradorGraficos`:
```python
def grafico_09_seu_grafico(self):
    fig, ax = plt.subplots(figsize=(12, 6))
    # Seu código aqui
    plt.savefig(self.output_dir / '09-seu-grafico.png', bbox_inches='tight')
    print("✅ Gráfico 9: Seu Gráfico")
```

E adicione ao método `gerar_todos_graficos()`:
```python
def gerar_todos_graficos(self):
    # ... gráficos existentes ...
    self.grafico_09_seu_grafico()
```

## Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'pandas'"

**Solução:**
```bash
pip install pandas matplotlib seaborn numpy
```

### Erro: "FileNotFoundError: resultados.jtl"

**Solução:**
Execute os testes primeiro:
```powershell
powershell -ExecutionPolicy Bypass -File executar-teste.ps1
```

### Gráficos não aparecem

**Solução:**
Verifique o diretório `analise-graficos/`. Os gráficos são salvos, não exibidos na tela.

### Erro de codificação no relatório textual

**Solução:**
No Windows, use:
```powershell
Get-Content analise-graficos\relatorio-completo.txt -Encoding UTF8
```

## Análise Avançada (Opcional)

### Análise Estatística Adicional

Adicione ao final do script para análise estatística:

```python
import scipy.stats as stats

# Teste de normalidade
for nome, resultado in gerador.resultados.items():
    dados = resultado['tempos_raw']  # Se disponível
    stat, p_value = stats.shapiro(dados)
    print(f"{nome}: p-value = {p_value:.4f}")
```

### Exportar para Excel

```python
import pandas as pd

# Criar DataFrame
df_resultados = pd.DataFrame(gerador.resultados).T
df_resultados.to_excel('analise-graficos/resultados.xlsx')
```

### Gerar PDF com todos os gráficos

```bash
pip install img2pdf
```

```python
import img2pdf
from pathlib import Path

images = sorted(Path('analise-graficos').glob('*.png'))
with open('analise-graficos/relatorio-completo.pdf', 'wb') as f:
    f.write(img2pdf.convert([str(img) for img in images]))
```

## Boas Práticas

1. **Execute os testes em horários consistentes** para comparação justa
2. **Mantenha histórico de resultados** para análise de tendências
3. **Compare sempre com baseline** para validar regressões
4. **Documente mudanças** entre testes (código, infraestrutura)
5. **Compartilhe os gráficos** em formato PNG (alta qualidade)

## Conclusão

Este sistema oferece uma análise profissional e automatizada dos testes de carga, superando soluções manuais em precisão, velocidade e qualidade visual dos resultados.
