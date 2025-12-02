# Banco de Dados

Esta pasta contém o banco de dados SQLite e scripts relacionados.

## Arquivos

### livros.db
Banco de dados SQLite com a tabela de livros.

**Esquema:**
```sql
CREATE TABLE livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    genero TEXT,
    ano INTEGER,
    sinopse TEXT,
    avaliacao INTEGER DEFAULT 0,
    capa TEXT,
    favorito INTEGER DEFAULT 0,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

**Índices:**
- idx_livros_titulo
- idx_livros_autor
- idx_livros_genero
- idx_livros_avaliacao
- idx_livros_favorito

### seed.js
Script para popular o banco com dados de exemplo.

**Dados inseridos:**
- 10 livros clássicos
- Informações completas (título, autor, gênero, sinopse, capa)
- Avaliações variadas
- Alguns marcados como favoritos

## Uso

```bash
# Popular banco de dados
npm run seed

# Ou diretamente
node database/seed.js
```

## Backup

Para fazer backup do banco:
```bash
cp database/livros.db database/livros-backup-$(date +%Y%m%d).db
```

## Restore

Para restaurar:
```bash
cp database/livros-backup-YYYYMMDD.db database/livros.db
```
