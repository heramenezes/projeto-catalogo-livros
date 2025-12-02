# Documentação

Guias completos sobre execução de testes, análise de resultados e interpretação de métricas.

## Guias Disponíveis

### [GUIA_EXECUCAO_TESTES.md](GUIA_EXECUCAO_TESTES.md)
Instruções completas para executar testes de carga.

**Conteúdo:**
- Pré-requisitos
- Instalação do JMeter
- Execução em Windows e Linux
- Parâmetros do JMeter
- Solução de problemas
- Scripts de automação

### [ANALISE_RESULTADOS.md](ANALISE_RESULTADOS.md)
Interpretação detalhada dos relatórios HTML do JMeter.

**Conteúdo:**
- Estrutura do relatório
- Explicação de cada métrica
- APDEX, percentis, throughput
- Análise por endpoint
- Identificação de gargalos
- Tipos de teste executados
- Ações recomendadas

### [GUIA_ANALISE_PYTHON.md](GUIA_ANALISE_PYTHON.md)
Sistema de análise automatizada com Python.

**Conteúdo:**
- Instalação do Python e dependências
- Execução do script de análise
- Descrição dos 8 gráficos gerados
- Interpretação de cores e métricas
- Customização
- Comparação com outras soluções
- Análise avançada

## Fluxo de Uso Recomendado

1. **Preparação**
   - Leia: GUIA_EXECUCAO_TESTES.md
   - Instale pré-requisitos
   - Configure ambiente

2. **Execução**
   - Inicie o servidor: `npm start`
   - Execute testes: `tests/jmeter/executar-teste.ps1`
   - Aguarde conclusão (2-5 min)

3. **Análise HTML**
   - Abra: `tests/jmeter/relatorio-html/index.html`
   - Leia: ANALISE_RESULTADOS.md
   - Interprete métricas

4. **Análise Python**
   - Leia: GUIA_ANALISE_PYTHON.md
   - Execute: `python tests/analysis/analisar-resultados.py`
   - Visualize: `tests/analysis/analise-graficos/`

5. **Ações**
   - Identifique gargalos
   - Otimize código
   - Re-execute testes
   - Compare resultados

## Referências Rápidas

### Comandos Principais

```bash
# Iniciar servidor
npm start

# Popular banco
npm run seed

# Executar testes (Windows)
powershell -ExecutionPolicy Bypass -File tests/jmeter/executar-teste.ps1

# Analisar resultados
cd tests/analysis && python analisar-resultados.py
```

### Métricas-Chave

| Métrica | Ótimo | Bom | Crítico |
|---------|-------|-----|---------|
| Taxa de Erro | < 1% | < 5% | > 20% |
| P95 | < 500ms | < 1s | > 2s |
| APDEX | > 0.90 | > 0.70 | < 0.50 |
| Throughput | Crescente | Estável | Decrescente |

### Tipos de Gargalo

- **CPU-bound**: Tempo cresce linear, /heavy-cpu lento
- **I/O-bound**: Latência alta, /heavy-io lento
- **Memory-bound**: Tempos erráticos, GC frequente
- **Network-bound**: Diferença latency vs response time

## Glossário

**APDEX** - Application Performance Index (0-1)
**P90/P95/P99** - Percentis de tempo de resposta
**Throughput** - Requisições por segundo
**Latency** - Tempo até primeiro byte
**Response Time** - Tempo total da requisição
**Ramp-up** - Tempo para atingir carga total
**Thread** - Usuário virtual no JMeter
**JTL** - JMeter Test Log (arquivo de resultados)

## Suporte

Para dúvidas específicas:
1. Consulte o guia correspondente
2. Verifique seção de "Solução de Problemas"
3. Revise os READMEs das pastas específicas

## Contribuindo

Para melhorar a documentação:
1. Identifique lacunas ou erros
2. Proponha melhorias
3. Adicione exemplos práticos
4. Atualize referências

---

**Dica:** Mantenha esta documentação atualizada conforme o projeto evolui.
