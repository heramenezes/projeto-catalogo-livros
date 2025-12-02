const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const dbFile = path.join(__dirname, '../database/livros.db');
const db = new sqlite3.Database(dbFile);

function init() {
    db.serialize(() => {
        db.run(`CREATE TABLE IF NOT EXISTS livros (
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
        )`);

        db.run(`CREATE INDEX IF NOT EXISTS idx_livros_titulo ON livros(titulo)`);
        db.run(`CREATE INDEX IF NOT EXISTS idx_livros_autor ON livros(autor)`);
        db.run(`CREATE INDEX IF NOT EXISTS idx_livros_genero ON livros(genero)`);
        db.run(`CREATE INDEX IF NOT EXISTS idx_livros_avaliacao ON livros(avaliacao)`);
        db.run(`CREATE INDEX IF NOT EXISTS idx_livros_favorito ON livros(favorito)`);

        console.log('Conectado ao banco de dados SQLite');
        console.log('Tabela de livros pronta');
    });
}

module.exports = { db, init };
