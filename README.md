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

## Pré-requisitos

- Node.js 14+ e npm
- Python 3.8+ (para análise de resultados)
- Apache JMeter 5.6+ (para testes de carga)
- Java JDK 8+ (necessário para JMeter)

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

## Execução

### Iniciar o Servidor

```bash
npm start
```

O servidor estará disponível em: http://localhost:3000

### Popular o Banco de Dados (primeira execução)

```bash
npm run seed
```

Isso criará 10 livros de exemplo no banco de dados.

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

## Testes de Carga

### Tipos de Teste Configurados

1. **Carga Espersa** - 20 usuários, carga constante
2. **Rajada** - 100 usuários em 2 segundos
3. **Estresse** - 50 usuários com carga crescente
4. **Baseline** - 5 usuários (referência)
5. **Volume** - 10 usuários, 100 requisições cada
6. **Escalabilidade Fase 1** - 10 usuários
7. **Escalabilidade Fase 2** - 30 usuários
8. **Escalabilidade Fase 3** - 60 usuários

### Executar Testes

**Windows:**
```powershell
powershell -ExecutionPolicy Bypass -File tests/jmeter/executar-teste.ps1
```

**Linux:**
```bash
cd tests/jmeter
chmod +x executar-teste.sh
./executar-teste.sh
```

### Analisar Resultados com Python

```bash
cd tests/analysis
python analisar-resultados.py
```

Gera 8 gráficos profissionais em alta resolução (300 DPI) e um relatório textual detalhado.

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

Este projeto é livre para uso acadêmico.

## Autores
 
- Laura Menezes Heráclito Alves
- Antonio Drumond Cota de Souza



**Nota:** Para informações detalhadas sobre cada componente, consulte a documentação específica na pasta `docs/`.
