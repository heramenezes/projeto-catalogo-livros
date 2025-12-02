# Testes de Carga e Análises

Esta pasta contém todos os testes de performance e ferramentas de análise.

## Estrutura

```
tests/
├── jmeter/          # Testes de carga com Apache JMeter
└── analysis/        # Análise de resultados com Python
```

## Testes JMeter

Navegue para `jmeter/` para executar testes de carga.

### Execução Rápida

```powershell
# Windows
powershell -ExecutionPolicy Bypass -File tests/jmeter/executar-teste.ps1
```

```bash
# Linux
cd tests/jmeter && ./executar-teste.sh
```

## Análise de Resultados

Navegue para `analysis/` para gerar gráficos e relatórios.

### Execução Rápida

```bash
cd tests/analysis
python analisar-resultados.py
```

## Fluxo de Trabalho Recomendado

1. **Executar testes:** `tests/jmeter/executar-teste.ps1`
2. **Aguardar conclusão** (2-5 minutos)
3. **Ver relatório HTML:** `tests/jmeter/relatorio-html/index.html`
4. **Gerar gráficos:** `python tests/analysis/analisar-resultados.py`
5. **Analisar gráficos:** `tests/analysis/analise-graficos/`

## Documentação

- [Guia de Execução](../docs/GUIA_EXECUCAO_TESTES.md)
- [Análise de Resultados](../docs/ANALISE_RESULTADOS.md)
- [Análise Python](../docs/GUIA_ANALISE_PYTHON.md)
