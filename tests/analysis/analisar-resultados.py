"""
Sistema de Análise Automatizada de Testes de Carga
Projeto: Catálogo de Livros
Extrai dados dos arquivos JTL do JMeter e gera visualizações avançadas
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configurações de estilo profissional
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['figure.titlesize'] = 14
plt.rcParams['figure.titleweight'] = 'bold'

class AnalisadorJMeter:
    """Classe para análise de resultados JMeter"""
    
    def __init__(self, arquivo_jtl):
        """Inicializa o analisador com arquivo JTL"""
        self.arquivo = arquivo_jtl
        self.df = None
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega dados do arquivo JTL"""
        try:
            # JTL pode ser CSV ou XML, tentamos CSV primeiro
            self.df = pd.read_csv(self.arquivo)
            # Renomear colunas para padrão
            if 'timeStamp' in self.df.columns:
                self.df['timestamp'] = pd.to_datetime(self.df['timeStamp'], unit='ms')
            if 'elapsed' in self.df.columns:
                self.df['response_time'] = self.df['elapsed']
            if 'label' in self.df.columns:
                self.df['endpoint'] = self.df['label']
            if 'success' in self.df.columns:
                self.df['is_success'] = self.df['success']
        except:
            print(f"Erro ao carregar {self.arquivo}")
            self.df = pd.DataFrame()
    
    def calcular_metricas(self):
        """Calcula métricas principais"""
        if self.df.empty:
            return {}
        
        total_requests = len(self.df)
        success_requests = self.df['is_success'].sum() if 'is_success' in self.df.columns else 0
        failed_requests = total_requests - success_requests
        error_rate = (failed_requests / total_requests * 100) if total_requests > 0 else 0
        
        metricas = {
            'total_requests': total_requests,
            'success_requests': success_requests,
            'failed_requests': failed_requests,
            'error_rate': error_rate,
            'avg_response_time': self.df['response_time'].mean() if 'response_time' in self.df.columns else 0,
            'min_response_time': self.df['response_time'].min() if 'response_time' in self.df.columns else 0,
            'max_response_time': self.df['response_time'].max() if 'response_time' in self.df.columns else 0,
            'p50': self.df['response_time'].quantile(0.50) if 'response_time' in self.df.columns else 0,
            'p90': self.df['response_time'].quantile(0.90) if 'response_time' in self.df.columns else 0,
            'p95': self.df['response_time'].quantile(0.95) if 'response_time' in self.df.columns else 0,
            'p99': self.df['response_time'].quantile(0.99) if 'response_time' in self.df.columns else 0,
            'throughput': self._calcular_throughput(),
            'endpoints': self._analisar_endpoints()
        }
        
        return metricas
    
    def _calcular_throughput(self):
        """Calcula throughput (req/s)"""
        if 'timestamp' not in self.df.columns or self.df.empty:
            return 0
        
        duracao = (self.df['timestamp'].max() - self.df['timestamp'].min()).total_seconds()
        return len(self.df) / duracao if duracao > 0 else 0
    
    def _analisar_endpoints(self):
        """Analisa métricas por endpoint"""
        if 'endpoint' not in self.df.columns:
            return {}
        
        endpoints = {}
        for endpoint in self.df['endpoint'].unique():
            df_endpoint = self.df[self.df['endpoint'] == endpoint]
            endpoints[endpoint] = {
                'count': len(df_endpoint),
                'avg_time': df_endpoint['response_time'].mean() if 'response_time' in df_endpoint.columns else 0,
                'max_time': df_endpoint['response_time'].max() if 'response_time' in df_endpoint.columns else 0,
                'error_rate': ((~df_endpoint['is_success']).sum() / len(df_endpoint) * 100) if 'is_success' in df_endpoint.columns else 0
            }
        
        return endpoints

class GeradorGraficos:
    """Classe para geração de gráficos avançados"""
    
    def __init__(self, output_dir='analise-graficos'):
        """Inicializa gerador de gráficos"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.resultados = {}
    
    def adicionar_teste(self, nome, arquivo_jtl):
        """Adiciona resultado de um teste"""
        analisador = AnalisadorJMeter(arquivo_jtl)
        self.resultados[nome] = analisador.calcular_metricas()
    
    def gerar_todos_graficos(self):
        """Gera todos os gráficos de análise"""
        print("📊 Gerando gráficos de análise...\n")
        
        self.grafico_01_visao_geral()
        self.grafico_02_comparativo_performance()
        self.grafico_03_distribuicao_percentis()
        self.grafico_04_taxa_erro_throughput()
        self.grafico_05_heatmap_endpoints()
        self.grafico_06_analise_escalabilidade()
        self.grafico_07_comparativo_tempos()
        self.grafico_08_radar_performance()
        
        print("\n✅ Todos os gráficos foram gerados com sucesso!")
        print(f"📁 Salvos em: {self.output_dir}/")
    
    def grafico_01_visao_geral(self):
        """Dashboard com visão geral de todos os testes"""
        fig = plt.figure(figsize=(16, 10))
        fig.suptitle('Dashboard Completo - Análise de Testes de Carga', fontsize=16, y=0.995)
        
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Total de Requisições
        ax1 = fig.add_subplot(gs[0, 0])
        nomes = list(self.resultados.keys())
        total_reqs = [self.resultados[n]['total_requests'] for n in nomes]
        colors = plt.cm.viridis(np.linspace(0, 1, len(nomes)))
        ax1.bar(range(len(nomes)), total_reqs, color=colors)
        ax1.set_title('Total de Requisições')
        ax1.set_ylabel('Requisições')
        ax1.set_xticks(range(len(nomes)))
        ax1.set_xticklabels([n.replace(' ', '\n') for n in nomes], fontsize=8)
        for i, v in enumerate(total_reqs):
            ax1.text(i, v, f'{v}', ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        # 2. Taxa de Erro
        ax2 = fig.add_subplot(gs[0, 1])
        error_rates = [self.resultados[n]['error_rate'] for n in nomes]
        colors_error = ['green' if e < 5 else 'orange' if e < 20 else 'red' for e in error_rates]
        ax2.bar(range(len(nomes)), error_rates, color=colors_error)
        ax2.set_title('Taxa de Erro (%)')
        ax2.set_ylabel('Erro (%)')
        ax2.set_xticks(range(len(nomes)))
        ax2.set_xticklabels([n.replace(' ', '\n') for n in nomes], fontsize=8)
        ax2.axhline(y=5, color='orange', linestyle='--', alpha=0.5, label='Limite Aceitável')
        ax2.axhline(y=20, color='red', linestyle='--', alpha=0.5, label='Limite Crítico')
        ax2.legend(fontsize=7)
        for i, v in enumerate(error_rates):
            ax2.text(i, v, f'{v:.1f}%', ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        # 3. Throughput
        ax3 = fig.add_subplot(gs[0, 2])
        throughputs = [self.resultados[n]['throughput'] for n in nomes]
        ax3.bar(range(len(nomes)), throughputs, color='teal')
        ax3.set_title('Throughput (req/s)')
        ax3.set_ylabel('Requisições/segundo')
        ax3.set_xticks(range(len(nomes)))
        ax3.set_xticklabels([n.replace(' ', '\n') for n in nomes], fontsize=8)
        for i, v in enumerate(throughputs):
            ax3.text(i, v, f'{v:.1f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        # 4. Tempo Médio de Resposta
        ax4 = fig.add_subplot(gs[1, :])
        avg_times = [self.resultados[n]['avg_response_time'] for n in nomes]
        max_times = [self.resultados[n]['max_response_time'] for n in nomes]
        x = np.arange(len(nomes))
        width = 0.35
        ax4.bar(x - width/2, avg_times, width, label='Tempo Médio', color='steelblue')
        ax4.bar(x + width/2, max_times, width, label='Tempo Máximo', color='coral')
        ax4.set_title('Comparativo de Tempos de Resposta (ms)')
        ax4.set_ylabel('Tempo (ms)')
        ax4.set_xticks(x)
        ax4.set_xticklabels(nomes, rotation=15, ha='right')
        ax4.legend()
        ax4.set_yscale('log')
        
        # 5. Sucessos vs Falhas
        ax5 = fig.add_subplot(gs[2, 0])
        success = [self.resultados[n]['success_requests'] for n in nomes]
        failed = [self.resultados[n]['failed_requests'] for n in nomes]
        ax5.bar(range(len(nomes)), success, label='Sucesso', color='green', alpha=0.7)
        ax5.bar(range(len(nomes)), failed, bottom=success, label='Falha', color='red', alpha=0.7)
        ax5.set_title('Distribuição de Sucessos e Falhas')
        ax5.set_ylabel('Requisições')
        ax5.set_xticks(range(len(nomes)))
        ax5.set_xticklabels([n.replace(' ', '\n') for n in nomes], fontsize=8)
        ax5.legend()
        
        # 6. Percentis P90, P95, P99
        ax6 = fig.add_subplot(gs[2, 1:])
        p90 = [self.resultados[n]['p90'] for n in nomes]
        p95 = [self.resultados[n]['p95'] for n in nomes]
        p99 = [self.resultados[n]['p99'] for n in nomes]
        x = np.arange(len(nomes))
        width = 0.25
        ax6.bar(x - width, p90, width, label='P90', color='lightgreen')
        ax6.bar(x, p95, width, label='P95', color='yellow')
        ax6.bar(x + width, p99, width, label='P99', color='orange')
        ax6.set_title('Percentis de Tempo de Resposta (ms)')
        ax6.set_ylabel('Tempo (ms)')
        ax6.set_xticks(x)
        ax6.set_xticklabels(nomes, rotation=15, ha='right')
        ax6.legend()
        
        plt.savefig(self.output_dir / '01-dashboard-completo.png', bbox_inches='tight')
        print("✅ Gráfico 1: Dashboard Completo")
    
    def grafico_02_comparativo_performance(self):
        """Gráfico comparativo de performance geral"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Análise Comparativa de Performance', fontsize=14)
        
        nomes = list(self.resultados.keys())
        
        # Tempo Médio
        avg_times = [self.resultados[n]['avg_response_time'] for n in nomes]
        axes[0, 0].barh(nomes, avg_times, color='steelblue')
        axes[0, 0].set_title('Tempo Médio de Resposta')
        axes[0, 0].set_xlabel('Tempo (ms)')
        for i, v in enumerate(avg_times):
            axes[0, 0].text(v, i, f' {v:.0f}ms', va='center', fontweight='bold')
        
        # Taxa de Erro
        error_rates = [self.resultados[n]['error_rate'] for n in nomes]
        colors = ['green' if e < 5 else 'orange' if e < 20 else 'red' for e in error_rates]
        axes[0, 1].barh(nomes, error_rates, color=colors)
        axes[0, 1].set_title('Taxa de Erro')
        axes[0, 1].set_xlabel('Erro (%)')
        for i, v in enumerate(error_rates):
            axes[0, 1].text(v, i, f' {v:.1f}%', va='center', fontweight='bold')
        
        # Throughput
        throughputs = [self.resultados[n]['throughput'] for n in nomes]
        axes[1, 0].barh(nomes, throughputs, color='teal')
        axes[1, 0].set_title('Throughput')
        axes[1, 0].set_xlabel('Requisições/segundo')
        for i, v in enumerate(throughputs):
            axes[1, 0].text(v, i, f' {v:.1f}', va='center', fontweight='bold')
        
        # Total de Requisições
        total_reqs = [self.resultados[n]['total_requests'] for n in nomes]
        axes[1, 1].barh(nomes, total_reqs, color='purple')
        axes[1, 1].set_title('Total de Requisições')
        axes[1, 1].set_xlabel('Requisições')
        for i, v in enumerate(total_reqs):
            axes[1, 1].text(v, i, f' {v}', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '02-comparativo-performance.png', bbox_inches='tight')
        print("✅ Gráfico 2: Comparativo de Performance")
    
    def grafico_03_distribuicao_percentis(self):
        """Distribuição de percentis para todos os testes"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        nomes = list(self.resultados.keys())
        percentis = ['p50', 'p90', 'p95', 'p99']
        labels_percentis = ['P50 (Mediana)', 'P90', 'P95', 'P99']
        
        x = np.arange(len(nomes))
        width = 0.2
        
        for i, (p, label) in enumerate(zip(percentis, labels_percentis)):
            valores = [self.resultados[n][p] for n in nomes]
            ax.bar(x + i*width - width*1.5, valores, width, label=label)
        
        ax.set_title('Distribuição de Percentis de Tempo de Resposta', fontsize=14)
        ax.set_ylabel('Tempo de Resposta (ms)')
        ax.set_xlabel('Teste')
        ax.set_xticks(x)
        ax.set_xticklabels(nomes, rotation=15, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '03-distribuicao-percentis.png', bbox_inches='tight')
        print("✅ Gráfico 3: Distribuição de Percentis")
    
    def grafico_04_taxa_erro_throughput(self):
        """Correlação entre taxa de erro e throughput"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        nomes = list(self.resultados.keys())
        error_rates = [self.resultados[n]['error_rate'] for n in nomes]
        throughputs = [self.resultados[n]['throughput'] for n in nomes]
        
        # Taxa de Erro ao longo dos testes
        ax1.plot(range(len(nomes)), error_rates, marker='o', linewidth=2, markersize=10, color='red')
        ax1.fill_between(range(len(nomes)), error_rates, alpha=0.3, color='red')
        ax1.set_title('Evolução da Taxa de Erro')
        ax1.set_ylabel('Taxa de Erro (%)')
        ax1.set_xlabel('Teste')
        ax1.set_xticks(range(len(nomes)))
        ax1.set_xticklabels([n.replace(' ', '\n') for n in nomes], fontsize=9)
        ax1.axhline(y=5, color='orange', linestyle='--', alpha=0.5, label='Limite Aceitável (5%)')
        ax1.axhline(y=20, color='darkred', linestyle='--', alpha=0.5, label='Limite Crítico (20%)')
        ax1.legend()
        ax1.grid(alpha=0.3)
        
        # Throughput ao longo dos testes
        ax2.plot(range(len(nomes)), throughputs, marker='s', linewidth=2, markersize=10, color='green')
        ax2.fill_between(range(len(nomes)), throughputs, alpha=0.3, color='green')
        ax2.set_title('Evolução do Throughput')
        ax2.set_ylabel('Throughput (req/s)')
        ax2.set_xlabel('Teste')
        ax2.set_xticks(range(len(nomes)))
        ax2.set_xticklabels([n.replace(' ', '\n') for n in nomes], fontsize=9)
        ax2.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '04-erro-throughput.png', bbox_inches='tight')
        print("✅ Gráfico 4: Taxa de Erro e Throughput")
    
    def grafico_05_heatmap_endpoints(self):
        """Heatmap de performance por endpoint"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Coletar dados de endpoints de todos os testes
        todos_endpoints = set()
        for resultado in self.resultados.values():
            todos_endpoints.update(resultado['endpoints'].keys())
        
        # Criar matriz de dados
        nomes = list(self.resultados.keys())
        endpoints = sorted(list(todos_endpoints))
        
        matriz_tempo = []
        for endpoint in endpoints:
            linha = []
            for nome in nomes:
                if endpoint in self.resultados[nome]['endpoints']:
                    linha.append(self.resultados[nome]['endpoints'][endpoint]['avg_time'])
                else:
                    linha.append(0)
            matriz_tempo.append(linha)
        
        # Criar heatmap
        im = ax.imshow(matriz_tempo, cmap='YlOrRd', aspect='auto')
        
        ax.set_xticks(np.arange(len(nomes)))
        ax.set_yticks(np.arange(len(endpoints)))
        ax.set_xticklabels(nomes, rotation=45, ha='right')
        ax.set_yticklabels([e.replace('GET ', '').replace('POST ', '') for e in endpoints])
        
        # Adicionar valores nas células
        for i in range(len(endpoints)):
            for j in range(len(nomes)):
                text = ax.text(j, i, f'{matriz_tempo[i][j]:.0f}',
                             ha="center", va="center", color="black", fontsize=8)
        
        ax.set_title('Heatmap de Tempo Médio por Endpoint (ms)', fontsize=14, pad=20)
        fig.colorbar(im, ax=ax, label='Tempo (ms)')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '05-heatmap-endpoints.png', bbox_inches='tight')
        print("✅ Gráfico 5: Heatmap de Endpoints")
    
    def grafico_06_analise_escalabilidade(self):
        """Análise de escalabilidade entre testes"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Análise de Escalabilidade', fontsize=14)
        
        nomes = list(self.resultados.keys())
        indices = range(len(nomes))
        
        # 1. Throughput vs Índice do teste
        throughputs = [self.resultados[n]['throughput'] for n in nomes]
        axes[0, 0].plot(indices, throughputs, marker='o', linewidth=2, markersize=10, color='green')
        axes[0, 0].fill_between(indices, throughputs, alpha=0.2, color='green')
        axes[0, 0].set_title('Escalabilidade de Throughput')
        axes[0, 0].set_ylabel('Throughput (req/s)')
        axes[0, 0].set_xlabel('Complexidade do Teste →')
        axes[0, 0].set_xticks(indices)
        axes[0, 0].set_xticklabels([n.split()[0] for n in nomes], fontsize=9)
        axes[0, 0].grid(alpha=0.3)
        
        # 2. Taxa de Erro vs Complexidade
        error_rates = [self.resultados[n]['error_rate'] for n in nomes]
        axes[0, 1].plot(indices, error_rates, marker='o', linewidth=2, markersize=10, color='red')
        axes[0, 1].fill_between(indices, error_rates, alpha=0.2, color='red')
        axes[0, 1].set_title('Degradação da Estabilidade')
        axes[0, 1].set_ylabel('Taxa de Erro (%)')
        axes[0, 1].set_xlabel('Complexidade do Teste →')
        axes[0, 1].set_xticks(indices)
        axes[0, 1].set_xticklabels([n.split()[0] for n in nomes], fontsize=9)
        axes[0, 1].axhline(y=5, color='orange', linestyle='--', alpha=0.5)
        axes[0, 1].grid(alpha=0.3)
        
        # 3. Tempo Médio vs Complexidade
        avg_times = [self.resultados[n]['avg_response_time'] for n in nomes]
        axes[1, 0].plot(indices, avg_times, marker='s', linewidth=2, markersize=10, color='blue')
        axes[1, 0].fill_between(indices, avg_times, alpha=0.2, color='blue')
        axes[1, 0].set_title('Degradação de Performance')
        axes[1, 0].set_ylabel('Tempo Médio (ms)')
        axes[1, 0].set_xlabel('Complexidade do Teste →')
        axes[1, 0].set_xticks(indices)
        axes[1, 0].set_xticklabels([n.split()[0] for n in nomes], fontsize=9)
        axes[1, 0].grid(alpha=0.3)
        
        # 4. Eficiência (Throughput / Tempo Médio)
        eficiencia = [t / (a + 1) for t, a in zip(throughputs, avg_times)]
        axes[1, 1].bar(indices, eficiencia, color='purple', alpha=0.7)
        axes[1, 1].set_title('Eficiência Relativa')
        axes[1, 1].set_ylabel('Índice de Eficiência')
        axes[1, 1].set_xlabel('Teste')
        axes[1, 1].set_xticks(indices)
        axes[1, 1].set_xticklabels([n.split()[0] for n in nomes], fontsize=9)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '06-analise-escalabilidade.png', bbox_inches='tight')
        print("✅ Gráfico 6: Análise de Escalabilidade")
    
    def grafico_07_comparativo_tempos(self):
        """Comparativo detalhado de tempos"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        nomes = list(self.resultados.keys())
        metricas_tempo = ['min_response_time', 'avg_response_time', 'p90', 'p95', 'p99', 'max_response_time']
        labels = ['Mínimo', 'Médio', 'P90', 'P95', 'P99', 'Máximo']
        
        x = np.arange(len(nomes))
        width = 0.12
        
        for i, (metrica, label) in enumerate(zip(metricas_tempo, labels)):
            valores = [self.resultados[n][metrica] for n in nomes]
            ax.bar(x + i*width - width*2.5, valores, width, label=label)
        
        ax.set_title('Análise Detalhada de Distribuição de Tempos', fontsize=14)
        ax.set_ylabel('Tempo (ms)')
        ax.set_xlabel('Teste')
        ax.set_xticks(x)
        ax.set_xticklabels(nomes, rotation=15, ha='right')
        ax.legend(loc='upper left', ncol=3)
        ax.set_yscale('log')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '07-comparativo-tempos.png', bbox_inches='tight')
        print("✅ Gráfico 7: Comparativo de Tempos")
    
    def grafico_08_radar_performance(self):
        """Gráfico radar comparando múltiplas métricas"""
        fig = plt.figure(figsize=(14, 10))
        
        nomes = list(self.resultados.keys())
        num_testes = len(nomes)
        
        # Calcular quantos subplots precisamos
        cols = 3
        rows = (num_testes + cols - 1) // cols
        
        for idx, nome in enumerate(nomes):
            ax = fig.add_subplot(rows, cols, idx + 1, projection='polar')
            
            # Métricas normalizadas (0-100)
            resultado = self.resultados[nome]
            
            # Normalizar métricas (inverter onde menor é melhor)
            max_error = max([self.resultados[n]['error_rate'] for n in nomes])
            max_time = max([self.resultados[n]['avg_response_time'] for n in nomes])
            max_throughput = max([self.resultados[n]['throughput'] for n in nomes])
            
            metricas = [
                100 - (resultado['error_rate'] / max_error * 100) if max_error > 0 else 100,  # Estabilidade
                (resultado['throughput'] / max_throughput * 100) if max_throughput > 0 else 0,  # Throughput
                100 - (resultado['avg_response_time'] / max_time * 100) if max_time > 0 else 100,  # Performance
                100 - (resultado['p95'] / max_time * 100) if max_time > 0 else 100,  # Consistência P95
                100 - (resultado['p99'] / max_time * 100) if max_time > 0 else 100,  # Consistência P99
            ]
            
            categorias = ['Estabilidade', 'Throughput', 'Performance', 'P95', 'P99']
            
            # Fechar o polígono
            metricas += metricas[:1]
            angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
            angulos += angulos[:1]
            
            ax.plot(angulos, metricas, 'o-', linewidth=2)
            ax.fill(angulos, metricas, alpha=0.25)
            ax.set_xticks(angulos[:-1])
            ax.set_xticklabels(categorias, fontsize=8)
            ax.set_ylim(0, 100)
            ax.set_title(nome, fontsize=10, pad=20)
            ax.grid(True)
        
        fig.suptitle('Análise Multidimensional de Performance (Radar Chart)', fontsize=14, y=0.98)
        plt.tight_layout()
        plt.savefig(self.output_dir / '08-radar-performance.png', bbox_inches='tight')
        print("✅ Gráfico 8: Gráfico Radar de Performance")
    
    def gerar_relatorio_textual(self):
        """Gera relatório textual detalhado"""
        relatorio = []
        relatorio.append("="*100)
        relatorio.append("RELATÓRIO DETALHADO DE ANÁLISE DE TESTES DE CARGA".center(100))
        relatorio.append("="*100)
        relatorio.append(f"\nData de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        relatorio.append(f"Total de Testes Analisados: {len(self.resultados)}\n")
        
        for nome, resultado in self.resultados.items():
            relatorio.append("-"*100)
            relatorio.append(f"\n{nome.upper()}")
            relatorio.append("-"*100)
            relatorio.append(f"\n{'MÉTRICAS GERAIS':<50}")
            relatorio.append(f"  Total de Requisições: {resultado['total_requests']:>20,}")
            relatorio.append(f"  Requisições Bem-sucedidas: {resultado['success_requests']:>20,}")
            relatorio.append(f"  Requisições com Falha: {resultado['failed_requests']:>20,}")
            relatorio.append(f"  Taxa de Erro: {resultado['error_rate']:>20.2f}%")
            relatorio.append(f"  Throughput: {resultado['throughput']:>20.2f} req/s")
            
            relatorio.append(f"\n{'TEMPOS DE RESPOSTA (ms)':<50}")
            relatorio.append(f"  Tempo Mínimo: {resultado['min_response_time']:>20.2f}")
            relatorio.append(f"  Tempo Médio: {resultado['avg_response_time']:>20.2f}")
            relatorio.append(f"  Tempo Máximo: {resultado['max_response_time']:>20.2f}")
            relatorio.append(f"  P50 (Mediana): {resultado['p50']:>20.2f}")
            relatorio.append(f"  P90: {resultado['p90']:>20.2f}")
            relatorio.append(f"  P95: {resultado['p95']:>20.2f}")
            relatorio.append(f"  P99: {resultado['p99']:>20.2f}")
            
            if resultado['endpoints']:
                relatorio.append(f"\n{'ANÁLISE POR ENDPOINT':<50}")
                for endpoint, dados in resultado['endpoints'].items():
                    relatorio.append(f"\n  {endpoint}")
                    relatorio.append(f"    Requisições: {dados['count']:>10}")
                    relatorio.append(f"    Tempo Médio: {dados['avg_time']:>10.2f} ms")
                    relatorio.append(f"    Tempo Máximo: {dados['max_time']:>10.2f} ms")
                    relatorio.append(f"    Taxa de Erro: {dados['error_rate']:>10.2f}%")
            
            relatorio.append("")
        
        relatorio.append("="*100)
        relatorio.append("FIM DO RELATÓRIO".center(100))
        relatorio.append("="*100)
        
        # Salvar relatório
        with open(self.output_dir / 'relatorio-completo.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(relatorio))
        
        print("✅ Relatório textual gerado: relatorio-completo.txt")
        
        return '\n'.join(relatorio)

def main():
    """Função principal"""
    print("="*80)
    print("SISTEMA DE ANÁLISE AUTOMATIZADA DE TESTES DE CARGA".center(80))
    print("Projeto: Catálogo de Livros".center(80))
    print("="*80)
    print()
    
    # Criar gerador de gráficos
    gerador = GeradorGraficos('analise-graficos')
    
    # Verificar se existe o arquivo resultados.jtl
    if Path('../jmeter/resultados.jtl').exists():
        print("📂 Arquivo resultados.jtl encontrado")
        print("⚠️  Nota: Este arquivo contém todos os testes combinados")
        print("   Para análise individual por teste, execute testes separados\n")
        
        gerador.adicionar_teste('Todos os Testes Combinados', '../jmeter/resultados.jtl')
        gerador.gerar_todos_graficos()
        print()
        relatorio = gerador.gerar_relatorio_textual()
        print("\n" + "="*80)
        print("RESUMO DOS RESULTADOS")
        print("="*80)
        for linha in relatorio.split('\n')[:30]:  # Mostrar primeiras 30 linhas
            print(linha)
    else:
        print("❌ Arquivo resultados.jtl não encontrado!")
        print("\n📝 Instruções:")
        print("   1. Execute os testes com: powershell -ExecutionPolicy Bypass -File tests/jmeter/executar-teste.ps1")
        print("   2. Aguarde a conclusão dos testes")
        print("   3. Execute este script novamente")
    
    print("\n" + "="*80)
    print("Análise concluída!".center(80))
    print("="*80)

if __name__ == '__main__':
    main()
