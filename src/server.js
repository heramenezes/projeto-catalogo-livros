const express = require('express');
const cors = require('cors');
const path = require('path');
const { db, init } = require('./db.js');

const app = express();
app.use(express.static(path.join(__dirname, '../public')));
app.use(express.json());
app.use(cors());

// Inicializar banco de dados
init();

// ===== ROTAS DE LIVROS =====

// Listar livros com filtros, paginação e busca
app.get('/api/livros', (req, res) => {
    const { page = 1, limit = 12, search, sort, favorito } = req.query;
    const offset = (page - 1) * limit;

    let whereConditions = [];
    let params = [];

    // Filtro de busca
    if (search) {
        whereConditions.push('(titulo LIKE ? OR autor LIKE ?)');
        params.push(`%${search}%`, `%${search}%`);
    }

    // Filtro de favoritos
    if (favorito === '1') {
        whereConditions.push('favorito = 1');
    }

    const whereClause = whereConditions.length > 0 ? 'WHERE ' + whereConditions.join(' AND ') : '';

    // Ordenação
    let orderBy = 'ORDER BY id DESC';
    if (sort === 'titulo-asc') orderBy = 'ORDER BY titulo ASC';
    else if (sort === 'titulo-desc') orderBy = 'ORDER BY titulo DESC';
    else if (sort === 'autor-asc') orderBy = 'ORDER BY autor ASC';
    else if (sort === 'autor-desc') orderBy = 'ORDER BY autor DESC';
    else if (sort === 'avaliacao-desc') orderBy = 'ORDER BY avaliacao DESC';
    else if (sort === 'avaliacao-asc') orderBy = 'ORDER BY avaliacao ASC';

    // Query principal
    const query = `SELECT * FROM livros ${whereClause} ${orderBy} LIMIT ? OFFSET ?`;
    params.push(parseInt(limit), parseInt(offset));

    // Query para contar total
    const countQuery = `SELECT COUNT(*) as total FROM livros ${whereClause}`;
    const countParams = whereConditions.length > 0 ? params.slice(0, -2) : [];

    db.get(countQuery, countParams, (err, countRow) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }

        db.all(query, params, (err, rows) => {
            if (err) {
                return res.status(500).json({ error: err.message });
            }
            res.json({
                livros: rows,
                total: countRow.total,
                page: parseInt(page),
                totalPages: Math.ceil(countRow.total / limit)
            });
        });
    });
});

// Filtrar livros por avaliação
app.get('/api/livros/avaliacao/:estrelas', (req, res) => {
    const estrelas = parseInt(req.params.estrelas);
    
    db.all('SELECT * FROM livros WHERE avaliacao = ? ORDER BY id DESC', [estrelas], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(rows);
    });
});

// Buscar livro por ID
app.get('/api/livros/:id', (req, res) => {
    db.get('SELECT * FROM livros WHERE id = ?', [req.params.id], (err, row) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (!row) {
            return res.status(404).json({ error: 'Livro não encontrado' });
        }
        res.json(row);
    });
});

// Criar livro
app.post('/api/livros', (req, res) => {
    const { titulo, autor, genero, ano, sinopse, avaliacao, capa, favorito } = req.body;
    
    db.run(
        'INSERT INTO livros (titulo, autor, genero, ano, sinopse, avaliacao, capa, favorito) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        [titulo, autor, genero, ano, sinopse, avaliacao || 0, capa, favorito || 0],
        function(err) {
            if (err) {
                return res.status(500).json({ error: err.message });
            }
            res.status(201).json({ 
                id: this.lastID, 
                titulo, 
                autor, 
                genero, 
                ano, 
                sinopse, 
                avaliacao: avaliacao || 0,
                capa,
                favorito: favorito || 0
            });
        }
    );
});

// Atualizar livro
app.put('/api/livros/:id', (req, res) => {
    const { titulo, autor, genero, ano, sinopse, avaliacao, capa, favorito } = req.body;
    
    db.run(
        'UPDATE livros SET titulo = ?, autor = ?, genero = ?, ano = ?, sinopse = ?, avaliacao = ?, capa = ?, favorito = ? WHERE id = ?',
        [titulo, autor, genero, ano, sinopse, avaliacao, capa, favorito, req.params.id],
        function(err) {
            if (err) {
                return res.status(500).json({ error: err.message });
            }
            if (this.changes === 0) {
                return res.status(404).json({ error: 'Livro não encontrado' });
            }
            res.json({ 
                id: parseInt(req.params.id), 
                titulo, 
                autor, 
                genero, 
                ano, 
                sinopse, 
                avaliacao,
                capa,
                favorito
            });
        }
    );
});

// Remover livro
app.delete('/api/livros/:id', (req, res) => {
    db.run('DELETE FROM livros WHERE id = ?', [req.params.id], function(err) {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (this.changes === 0) {
            return res.status(404).json({ error: 'Livro não encontrado' });
        }
        res.json({ message: `Livro ${req.params.id} removido` });
    });
});

// Toggle favorito
app.patch('/api/livros/:id/favorito', (req, res) => {
    db.get('SELECT favorito FROM livros WHERE id = ?', [req.params.id], (err, row) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (!row) {
            return res.status(404).json({ error: 'Livro não encontrado' });
        }

        const novoFavorito = row.favorito === 1 ? 0 : 1;
        
        db.run('UPDATE livros SET favorito = ? WHERE id = ?', [novoFavorito, req.params.id], function(err) {
            if (err) {
                return res.status(500).json({ error: err.message });
            }
            res.json({ id: parseInt(req.params.id), favorito: novoFavorito });
        });
    });
});

// Estatísticas
app.get('/api/estatisticas', (req, res) => {
    const stats = {};
    
    // Total de livros
    db.get('SELECT COUNT(*) as total FROM livros', (err, row) => {
        if (err) return res.status(500).json({ error: err.message });
        stats.totalLivros = row.total;
        
        // Livros favoritos
        db.get('SELECT COUNT(*) as total FROM livros WHERE favorito = 1', (err, row) => {
            if (err) return res.status(500).json({ error: err.message });
            stats.totalFavoritos = row.total;
            
            // Média de avaliação
            db.get('SELECT AVG(avaliacao) as media FROM livros', (err, row) => {
                if (err) return res.status(500).json({ error: err.message });
                stats.mediaAvaliacao = row.media ? parseFloat(row.media.toFixed(2)) : 0;
                
                // Livros por gênero
                db.all('SELECT genero, COUNT(*) as total FROM livros GROUP BY genero ORDER BY total DESC', (err, rows) => {
                    if (err) return res.status(500).json({ error: err.message });
                    stats.porGenero = rows;
                    
                    res.json(stats);
                });
            });
        });
    });
});

// ===== ROTAS DE TESTE DE PERFORMANCE =====

// Endpoint para teste de CPU intensivo
app.get('/heavy-cpu', (req, res) => {
    const start = Date.now();
    let result = 0;
    
    // Simulação de processamento pesado de CPU
    for (let i = 0; i < 1000000; i++) {
        result += Math.sqrt(i) * Math.random();
    }
    
    const duration = Date.now() - start;
    res.json({
        message: 'CPU intensive task completed',
        duration: `${duration}ms`,
        result: result.toFixed(2)
    });
});

// Endpoint para teste de I/O intensivo
app.get('/heavy-io', (req, res) => {
    // Simula múltiplas operações de banco de dados
    const queries = [];
    
    for (let i = 0; i < 10; i++) {
        queries.push(new Promise((resolve, reject) => {
            db.all('SELECT * FROM livros ORDER BY RANDOM() LIMIT 5', (err, rows) => {
                if (err) reject(err);
                else resolve(rows);
            });
        }));
    }
    
    Promise.all(queries)
        .then(results => {
            res.json({
                message: 'I/O intensive task completed',
                queries: queries.length,
                totalBooks: results.flat().length
            });
        })
        .catch(err => {
            res.status(500).json({ error: err.message });
        });
});

// Endpoint que retorna muitos itens (teste de volume)
app.get('/many-items', (req, res) => {
    const items = [];
    for (let i = 0; i < 1000; i++) {
        items.push({
            id: i,
            title: `Item ${i}`,
            description: `Description for item ${i}`,
            value: Math.random() * 1000
        });
    }
    res.json({ count: items.length, items });
});

// Endpoint de status simples
app.get('/status', (req, res) => {
    res.json({
        status: 'ok',
        uptime: process.uptime(),
        timestamp: new Date().toISOString()
    });
});

// ===== SERVIDOR =====
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
    console.log('Catálogo de Livros - Sistema de Gestão de Leituras');
});
