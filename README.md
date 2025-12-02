# Catálogo de Livros - Sistema de Gestão de Leituras

Sistema completo de gerenciamento de catálogo de livros com interface web responsiva e testes de carga automatizados.

## Estrutura do Projeto

```
projeto-laura-antonio/
│
├── src/                          # Código-fonte da aplicação
│   ├── server.js                 # Servidor Express
│   └── db.js                     # Configuração do banco de dados
│
├── database/                     # Banco de dados e scripts
│   ├── livros.db                 # Banco SQLite
│   └── seed.js                   # Script de população inicial
│
├── public/                       # Arquivos estáticos (frontend)
│   ├── index.html                # Página principal
│   ├── book.html                 # Formulário de livros
│   ├── css/
│   │   └── styles.css            # Estilos da aplicação
│   └── js/
│       ├── script.js             # JavaScript principal
│       └── book.js               # JavaScript do formulário
│
├── tests/                        # Testes e análises
│   ├── jmeter/                   # Testes de carga JMeter
│   │   ├── teste-carga.jmx       # Configuração dos testes
│   │   ├── executar-teste.ps1    # Script de execução (Windows)
│   │   ├── executar-teste.bat    # Script alternativo (Windows)
│   │   ├── resultados.jtl        # Resultados dos testes (gerado)
│   │   └── relatorio-html/       # Relatório HTML (gerado)
│   │
│   └── analysis/                 # Análise de resultados
│       ├── analisar-resultados.py # Script Python de análise
│       ├── requirements.txt       # Dependências Python
│       └── analise-graficos/      # Gráficos gerados (gerado)
│
├── docs/                         # Documentação
│   ├── GUIA_EXECUCAO_TESTES.md   # Como executar testes
│   ├── ANALISE_RESULTADOS.md     # Interpretação dos resultados
│   └── GUIA_ANALISE_PYTHON.md    # Análise com Python
│
├── package.json                  # Dependências Node.js
└── README.md                     # Este arquivo

```

## ⚠️ Requisitos de Sistema

**Este projeto foi desenvolvido e testado apenas para Windows.**

### Pré-requisitos

- **Sistema Operacional:** Windows 10/11
- **Node.js** 14+ e npm
- **Apache JMeter** 5.6.3 instalado em `C:\Users\SEU_USUARIO\JMeter\`
- **Java JDK** 8+ (necessário para JMeter)
- **Python** 3.8+ (opcional, para análise avançada de resultados)

### ❌ Limitações Conhecidas

- **Linux/Mac:** Os scripts de automação de testes foram desenvolvidos para Windows PowerShell e não foram testados em outros sistemas operacionais
- Para executar em Linux/Mac, será necessário adaptar manualmente os scripts ou usar a interface gráfica do JMeter

## Instalação

### 1. Instalar Dependências Node.js

```bash
npm install
```

### 2. Instalar Dependências Python (opcional, para análise)

```bash
cd tests/analysis
pip install -r requirements.txt
cd ../..
```

## 🚀 Como Executar o Projeto

### Passo 1: Clonar o Repositório

```powershell
git clone https://github.com/heramenezes/projeto-catalogo-livros.git
cd projeto-catalogo-livros
```

### Passo 2: Instalar Dependências

```powershell
npm install
```

### Passo 3: Popular o Banco de Dados (primeira execução)

```powershell
npm run seed
```

Isso criará 10 livros de exemplo no banco de dados.

### Passo 4: Iniciar o Servidor

**Abra um terminal PowerShell e execute:**

```powershell
npm start
```

O servidor estará disponível em: http://localhost:3000

**⚠️ IMPORTANTE:** Mantenha este terminal aberto com o servidor rodando durante toda a execução dos testes!

## Funcionalidades

### Backend (API REST)

- **GET /api/livros** - Lista livros com paginação, busca e filtros
- **GET /api/livros/:id** - Busca livro específico
- **POST /api/livros** - Cria novo livro
- **PUT /api/livros/:id** - Atualiza livro
- **DELETE /api/livros/:id** - Remove livro
- **PATCH /api/livros/:id/favorito** - Toggle favorito
- **GET /api/estatisticas** - Estatísticas do catálogo
- **GET /heavy-cpu** - Endpoint de teste de CPU
- **GET /heavy-io** - Endpoint de teste de I/O
- **GET /many-items** - Endpoint de teste de volume
- **GET /status** - Status do servidor

### Frontend

- Interface responsiva e moderna
- Busca e filtros avançados
- Ordenação por múltiplos critérios
- Visualização em grade ou lista
- Sistema de avaliação (1-5 estrelas)
- Favoritos
- Gráficos estatísticos (Chart.js)
- Paginação

## 🧪 Executar Testes de Carga

### Pré-requisito: Servidor Deve Estar Rodando!

**Antes de executar os testes, certifique-se que o servidor está rodando (Passo 4 acima).**

### Método 1: Executar Testes com Script (Recomendado)

**Abra um NOVO terminal PowerShell (diferente do servidor) e execute:**

```powershell
cd tests\jmeter
.\executar-teste.ps1
```

O script irá:
1. Limpar resultados anteriores
2. Executar 8 cenários de teste (leva 2-3 minutos)
3. Gerar relatório HTML automaticamente
4. Abrir o relatório no navegador

### Método 2: Executar Testes Manualmente

**Se o script não funcionar, execute manualmente:**

```powershell
cd tests\jmeter
Remove-Item -Recurse -Force relatorio-html -ErrorAction SilentlyContinue
Remove-Item -Force resultados.jtl -ErrorAction SilentlyContinue
& "$env:USERPROFILE\JMeter\apache-jmeter-5.6.3\bin\jmeter.bat" -n -t teste-carga.jmx -l resultados.jtl -e -o relatorio-html
```

Após a conclusão, abra o relatório:

```powershell
Start-Process "relatorio-html\index.html"
```

### Tipos de Teste Configurados

1. **Carga Espersa** - 20 usuários, carga constante (10s ramp-up)
2. **Rajada** - 100 usuários em 2 segundos (teste de pico)
3. **Estresse** - 50 usuários com carga crescente (30s ramp-up)
4. **Baseline** - 5 usuários (referência de performance)
5. **Volume** - 10 usuários × 100 requisições cada
6. **Escalabilidade Fase 1** - 10 usuários
7. **Escalabilidade Fase 2** - 30 usuários (3x)
8. **Escalabilidade Fase 3** - 60 usuários (6x)

### 📊 Visualizar Resultados

Os resultados são gerados em:
- **Relatório HTML:** `tests/jmeter/relatorio-html/index.html` (dashboard interativo)
- **Dados brutos:** `tests/jmeter/resultados.jtl` (formato CSV)

### 📈 Análise Avançada com Python (Opcional)

Para gerar gráficos adicionais:

```powershell
cd tests\analysis
pip install -r requirements.txt
python analisar-resultados.py
```

Gera 8 gráficos profissionais em alta resolução (300 DPI) na pasta `analise-graficos/`.

## Documentação Completa

- **[Guia de Execução de Testes](docs/GUIA_EXECUCAO_TESTES.md)** - Instruções detalhadas para executar testes
- **[Análise de Resultados](docs/ANALISE_RESULTADOS.md)** - Como interpretar os resultados do JMeter
- **[Análise com Python](docs/GUIA_ANALISE_PYTHON.md)** - Sistema de análise automatizada

## Tecnologias Utilizadas

### Backend
- Node.js
- Express.js
- SQLite3
- CORS

### Frontend
- HTML5
- CSS3 (Design System customizado)
- JavaScript (Vanilla)
- Chart.js

### Testes
- Apache JMeter 5.6.3
- Python 3.8+
- Pandas
- Matplotlib
- Seaborn
- NumPy

## Scripts NPM

```bash
npm start          # Inicia o servidor
npm run seed       # Popula o banco de dados
```

## Estrutura do Banco de Dados

### Tabela: livros

| Campo      | Tipo    | Descrição                    |
|------------|---------|------------------------------|
| id         | INTEGER | Chave primária (auto)        |
| titulo     | TEXT    | Título do livro              |
| autor      | TEXT    | Autor do livro               |
| genero     | TEXT    | Gênero literário             |
| ano        | INTEGER | Ano de publicação            |
| sinopse    | TEXT    | Sinopse do livro             |
| avaliacao  | INTEGER | Avaliação (0-5 estrelas)     |
| capa       | TEXT    | URL da imagem de capa        |
| favorito   | INTEGER | 0 = não, 1 = sim             |
| criado_em  | DATETIME| Timestamp de criação         |

## Endpoints de Teste de Performance

Endpoints especiais para testes de carga:

- **/heavy-cpu** - Processamento intensivo (1 milhão de operações matemáticas)
- **/heavy-io** - 10 consultas simultâneas ao banco de dados
- **/many-items** - Retorna 1000 itens (teste de volume)
- **/status** - Healthcheck e uptime

## Métricas de Performance

### Targets de Performance

- **Tempo de Resposta P95:** < 500ms
- **Taxa de Erro:** < 1%
- **Throughput:** > 100 req/s
- **APDEX:** > 0.90

## Solução de Problemas

### Erro: "Connection refused"

Certifique-se de que o servidor está rodando:
```bash
npm start
```

### Erro: "ENOENT: no such file or directory"

Execute o seed para criar o banco de dados:
```bash
npm run seed
```

### Testes JMeter com 100% de erro

1. Verifique se o servidor está rodando
2. Confirme que está na porta 3000
3. Teste manualmente: http://localhost:3000/api/livros

### Python não encontra módulos

Instale as dependências:
```bash
cd tests/analysis
pip install -r requirements.txt
```


## Licença

Este projeto está sob a licença GNU GPL 3.0. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autores
 
- Laura Menezes Heráclito Alves
- Antônio Drumond Cota de Sousa



**Nota:** Para informações detalhadas sobre cada componente, consulte a documentação específica na pasta `docs/`.
