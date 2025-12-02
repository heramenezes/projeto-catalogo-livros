const { db, init } = require('../src/db');

init();

const livrosExemplo = [
    {
        titulo: "1984",
        autor: "George Orwell",
        genero: "Ficção Distópica",
        ano: 1949,
        sinopse: "Um romance distópico que retrata um regime totalitário que controla todos os aspectos da vida humana.",
        avaliacao: 5,
        capa: "https://images-na.ssl-images-amazon.com/images/I/71kxa1-0mfL.jpg",
        favorito: 1
    },
    {
        titulo: "O Senhor dos Anéis",
        autor: "J.R.R. Tolkien",
        genero: "Fantasia",
        ano: 1954,
        sinopse: "Uma épica jornada de um hobbit para destruir um anel poderoso e salvar a Terra Média.",
        avaliacao: 5,
        capa: "https://images-na.ssl-images-amazon.com/images/I/71jLBXtWJWL.jpg",
        favorito: 1
    },
    {
        titulo: "Dom Casmurro",
        autor: "Machado de Assis",
        genero: "Romance",
        ano: 1899,
        sinopse: "A história de Bentinho e sua suspeita de traição por parte de Capitu, sua grande paixão.",
        avaliacao: 4,
        capa: "https://images-na.ssl-images-amazon.com/images/I/71Q5H5qYZDL.jpg",
        favorito: 0
    },
    {
        titulo: "Harry Potter e a Pedra Filosofal",
        autor: "J.K. Rowling",
        genero: "Fantasia",
        ano: 1997,
        sinopse: "Um jovem bruxo descobre seu destino ao ingressar na Escola de Magia e Bruxaria de Hogwarts.",
        avaliacao: 5,
        capa: "https://images-na.ssl-images-amazon.com/images/I/81YOuOGFCJL.jpg",
        favorito: 1
    },
    {
        titulo: "Cem Anos de Solidão",
        autor: "Gabriel García Márquez",
        genero: "Realismo Mágico",
        ano: 1967,
        sinopse: "A saga da família Buendía ao longo de várias gerações na fictícia cidade de Macondo.",
        avaliacao: 4,
        capa: "https://images-na.ssl-images-amazon.com/images/I/71JLmTmKGxL.jpg",
        favorito: 0
    },
    {
        titulo: "O Pequeno Príncipe",
        autor: "Antoine de Saint-Exupéry",
        genero: "Fábula",
        ano: 1943,
        sinopse: "Uma fábula poética sobre um pequeno príncipe que viaja de planeta em planeta.",
        avaliacao: 5,
        capa: "https://images-na.ssl-images-amazon.com/images/I/71OZY035QKL.jpg",
        favorito: 1
    },
    {
        titulo: "A Culpa é das Estrelas",
        autor: "John Green",
        genero: "Romance",
        ano: 2012,
        sinopse: "A história de amor entre dois adolescentes que se conhecem em um grupo de apoio para pacientes com câncer.",
        avaliacao: 4,
        capa: "https://images-na.ssl-images-amazon.com/images/I/71vY3sNJhNL.jpg",
        favorito: 0
    },
    {
        titulo: "O Código Da Vinci",
        autor: "Dan Brown",
        genero: "Suspense",
        ano: 2003,
        sinopse: "Um professor de simbologia investiga um assassinato no Louvre que revela segredos ancestrais.",
        avaliacao: 4,
        capa: "https://images-na.ssl-images-amazon.com/images/I/91Q5dCjc2KL.jpg",
        favorito: 0
    },
    {
        titulo: "O Hobbit",
        autor: "J.R.R. Tolkien",
        genero: "Fantasia",
        ano: 1937,
        sinopse: "A aventura de Bilbo Bolseiro em busca de um tesouro guardado por um dragão.",
        avaliacao: 5,
        capa: "https://images-na.ssl-images-amazon.com/images/I/71V2v2GtAtL.jpg",
        favorito: 1
    },
    {
        titulo: "A Menina que Roubava Livros",
        autor: "Markus Zusak",
        genero: "Drama Histórico",
        ano: 2005,
        sinopse: "Durante a Segunda Guerra Mundial, uma menina encontra consolo nos livros que rouba.",
        avaliacao: 5,
        capa: "https://images-na.ssl-images-amazon.com/images/I/81IzbMPXzjL.jpg",
        favorito: 1
    }
];

function runSeed() {
    db.serialize(() => {
        // Verificar se já existem livros
        db.get('SELECT COUNT(*) as count FROM livros', (err, row) => {
            if (err) {
                console.error('Erro ao verificar livros:', err);
                return;
            }

            if (row.count > 0) {
                console.log(`Banco já contém ${row.count} livros. Seed não executado.`);
                db.close();
                return;
            }

            // Inserir livros de exemplo
            const insert = db.prepare(
                'INSERT INTO livros (titulo, autor, genero, ano, sinopse, avaliacao, capa, favorito) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            );

            livrosExemplo.forEach(livro => {
                insert.run(
                    livro.titulo,
                    livro.autor,
                    livro.genero,
                    livro.ano,
                    livro.sinopse,
                    livro.avaliacao,
                    livro.capa,
                    livro.favorito
                );
            });

            insert.finalize(() => {
                console.log(`Seed finalizado com ${livrosExemplo.length} livros.`);
                db.close();
            });
        });
    });
}

runSeed();
