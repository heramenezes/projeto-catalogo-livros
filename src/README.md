# Código-Fonte da Aplicação

Esta pasta contém o código principal do servidor e configuração do banco de dados.

## Arquivos

### server.js
Servidor Express com todas as rotas da API REST.

**Rotas principais:**
- `/api/livros` - CRUD de livros
- `/api/estatisticas` - Estatísticas do catálogo
- `/heavy-cpu`, `/heavy-io`, `/many-items` - Endpoints de teste

**Porta:** 3000

### db.js
Configuração e inicialização do banco de dados SQLite.

**Funcionalidades:**
- Criação automática de tabelas
- Criação de índices para performance
- Conexão singleton com o banco

## Execução

```bash
# Iniciar servidor
npm start

# Ou diretamente
node src/server.js
```

## Dependências

- express - Framework web
- cors - Habilitar CORS
- sqlite3 - Driver SQLite

## Ambiente de Desenvolvimento

O servidor usa:
- Express.json() para parsing de JSON
- Express.static() para servir arquivos estáticos do `/public`
- CORS habilitado para todas as origens
