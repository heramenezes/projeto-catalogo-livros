// book.js - Formulário de adicionar/editar livros

let livroId = null;

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    livroId = urlParams.get('id');

    if (livroId) {
        document.getElementById('formTitle').textContent = 'Editar Livro';
        carregarLivro(livroId);
    }

    // Atualizar valor da avaliação em tempo real
    const avaliacaoInput = document.getElementById('avaliacao');
    const ratingValue = document.getElementById('ratingValue');
    
    avaliacaoInput.addEventListener('input', (e) => {
        ratingValue.textContent = e.target.value;
    });

    // Enviar formulário
    document.getElementById('bookForm').addEventListener('submit', salvarLivro);
});

// Carregar dados do livro para edição
async function carregarLivro(id) {
    try {
        const response = await fetch(`http://localhost:3000/api/livros/${id}`);
        const livro = await response.json();

        document.getElementById('bookId').value = livro.id;
        document.getElementById('titulo').value = livro.titulo;
        document.getElementById('autor').value = livro.autor;
        document.getElementById('genero').value = livro.genero || '';
        document.getElementById('ano').value = livro.ano || '';
        document.getElementById('sinopse').value = livro.sinopse || '';
        document.getElementById('capa').value = livro.capa || '';
        document.getElementById('avaliacao').value = livro.avaliacao || 0;
        document.getElementById('ratingValue').textContent = livro.avaliacao || 0;
        document.getElementById('favorito').checked = livro.favorito === 1;
    } catch (error) {
        console.error('Erro ao carregar livro:', error);
        alert('Erro ao carregar dados do livro');
    }
}

// Salvar livro (criar ou atualizar)
async function salvarLivro(e) {
    e.preventDefault();

    const dados = {
        titulo: document.getElementById('titulo').value,
        autor: document.getElementById('autor').value,
        genero: document.getElementById('genero').value,
        ano: parseInt(document.getElementById('ano').value) || null,
        sinopse: document.getElementById('sinopse').value,
        capa: document.getElementById('capa').value,
        avaliacao: parseInt(document.getElementById('avaliacao').value),
        favorito: document.getElementById('favorito').checked ? 1 : 0
    };

    try {
        let response;
        
        if (livroId) {
            // Atualizar livro existente
            response = await fetch(`http://localhost:3000/api/livros/${livroId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dados)
            });
        } else {
            // Criar novo livro
            response = await fetch('http://localhost:3000/api/livros', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dados)
            });
        }

        if (response.ok) {
            alert(livroId ? 'Livro atualizado com sucesso!' : 'Livro criado com sucesso!');
            window.location.href = 'index.html';
        } else {
            const error = await response.json();
            alert('Erro ao salvar livro: ' + error.error);
        }
    } catch (error) {
        console.error('Erro ao salvar livro:', error);
        alert('Erro ao salvar livro');
    }
}
