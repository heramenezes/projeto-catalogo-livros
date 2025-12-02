// script.js - Gerenciamento do catálogo de livros

let paginaAtual = 1;
let totalPaginas = 1;
let filtroAtual = 'todos';
let searchTerm = '';
let generoChart = null;

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    carregarEstatisticas();
    carregarLivros();
    configurarFiltros();
    configurarViewToggle();
});

// Carregar estatísticas
async function carregarEstatisticas() {
    try {
        const response = await fetch('http://localhost:3000/api/estatisticas');
        const stats = await response.json();

        document.getElementById('totalLivros').textContent = stats.totalLivros;
        document.getElementById('totalFavoritos').textContent = stats.totalFavoritos;
        document.getElementById('mediaAvaliacao').textContent = stats.mediaAvaliacao.toFixed(1);

        // Criar gráfico de gêneros
        renderizarGraficoGeneros(stats.porGenero);
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

// Renderizar gráfico de gêneros
function renderizarGraficoGeneros(dados) {
    const ctx = document.getElementById('generoChart').getContext('2d');
    
    if (generoChart) {
        generoChart.destroy();
    }

    generoChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: dados.map(item => item.genero || 'Sem gênero'),
            datasets: [{
                data: dados.map(item => item.total),
                backgroundColor: [
                    '#6366f1',
                    '#8b5cf6',
                    '#ec4899',
                    '#f59e0b',
                    '#10b981',
                    '#3b82f6',
                    '#ef4444',
                    '#a855f7'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Carregar livros com filtros e paginação
async function carregarLivros(page = 1) {
    paginaAtual = page;
    
    const sortValue = document.getElementById('sortSelect').value;
    const params = new URLSearchParams({
        page: page,
        limit: 12
    });

    if (searchTerm) {
        params.append('search', searchTerm);
    }

    if (sortValue) {
        params.append('sort', sortValue);
    }

    // Filtros
    if (filtroAtual === 'favoritos') {
        params.append('favorito', '1');
    } else if (filtroAtual !== 'todos') {
        // Filtro por estrelas
        params.append('avaliacao', filtroAtual);
    }

    try {
        const response = await fetch(`http://localhost:3000/api/livros?${params}`);
        const data = await response.json();

        renderizarLivros(data.livros);
        totalPaginas = data.totalPages;
        renderizarPaginacao();
    } catch (error) {
        console.error('Erro ao carregar livros:', error);
        document.getElementById('booksContainer').innerHTML = '<div class="empty-state"><h3>Erro ao carregar livros</h3></div>';
    }
}

// Renderizar livros na página
function renderizarLivros(livros) {
    const container = document.getElementById('booksContainer');

    if (livros.length === 0) {
        container.innerHTML = '<div class="empty-state"><h3>Nenhum livro encontrado</h3><p>Tente ajustar os filtros ou adicione novos livros</p></div>';
        return;
    }

    container.innerHTML = livros.map(livro => `
        <div class="book-card">
            <div class="book-card-header">
                ${livro.favorito ? '<div class="favorite-badge">❤️</div>' : ''}
                ${livro.capa 
                    ? `<img src="${livro.capa}" alt="${livro.titulo}" class="book-cover" onerror="this.outerHTML='<div class=\\'no-cover\\'>${livro.titulo[0]}</div>'">` 
                    : `<div class="no-cover">${livro.titulo[0]}</div>`
                }
            </div>
            <div class="book-card-body">
                <h3 class="book-title">${livro.titulo}</h3>
                <p class="book-author">${livro.autor}</p>
                
                <div class="book-meta">
                    ${livro.genero ? `<span>${livro.genero}</span>` : ''}
                    ${livro.ano ? `<span>${livro.ano}</span>` : ''}
                </div>

                <div class="book-rating">
                    <span class="stars">${'★'.repeat(livro.avaliacao)}${'☆'.repeat(5 - livro.avaliacao)}</span>
                    <span class="rating-text">${livro.avaliacao}/5</span>
                </div>

                ${livro.sinopse ? `<p class="book-synopsis">${livro.sinopse}</p>` : ''}

                <div class="book-actions">
                    <button onclick="toggleFavorito(${livro.id}, ${livro.favorito})" class="btn-favorite" title="Favoritar">
                        ❤️
                    </button>
                    <button onclick="duplicarLivro(${livro.id})" class="btn-duplicate" title="Duplicar">
                        📋
                    </button>
                    <button onclick="window.location.href='book.html?id=${livro.id}'" class="btn-edit" title="Editar">
                        ✏️
                    </button>
                    <button onclick="excluirLivro(${livro.id})" class="btn-delete" title="Excluir">
                        🗑️
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Renderizar paginação
function renderizarPaginacao() {
    const container = document.getElementById('pagination');
    
    if (totalPaginas <= 1) {
        container.innerHTML = '';
        return;
    }

    let html = '';

    // Botão anterior
    html += `<button onclick="carregarLivros(${paginaAtual - 1})" ${paginaAtual === 1 ? 'disabled' : ''}>Anterior</button>`;

    // Números das páginas
    for (let i = 1; i <= totalPaginas; i++) {
        if (i === 1 || i === totalPaginas || (i >= paginaAtual - 1 && i <= paginaAtual + 1)) {
            html += `<button onclick="carregarLivros(${i})" class="${i === paginaAtual ? 'active' : ''}">${i}</button>`;
        } else if (i === paginaAtual - 2 || i === paginaAtual + 2) {
            html += '<span>...</span>';
        }
    }

    // Botão próximo
    html += `<button onclick="carregarLivros(${paginaAtual + 1})" ${paginaAtual === totalPaginas ? 'disabled' : ''}>Próximo</button>`;

    container.innerHTML = html;
}

// Configurar filtros
function configurarFiltros() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            filtroAtual = button.dataset.filter;
            carregarLivros(1);
        });
    });
}

// Configurar toggle de visualização
function configurarViewToggle() {
    const viewButtons = document.querySelectorAll('.view-btn');
    const booksContainer = document.getElementById('booksContainer');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', () => {
            viewButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            const view = button.dataset.view;
            if (view === 'list') {
                booksContainer.classList.add('list-view');
            } else {
                booksContainer.classList.remove('list-view');
            }
        });
    });
}

// Buscar livros
function buscar() {
    searchTerm = document.getElementById('searchInput').value;
    carregarLivros(1);
}

// Toggle favorito
async function toggleFavorito(id, favoritoAtual) {
    try {
        const response = await fetch(`http://localhost:3000/api/livros/${id}/favorito`, {
            method: 'PATCH'
        });
        
        if (response.ok) {
            carregarLivros(paginaAtual);
            carregarEstatisticas();
        }
    } catch (error) {
        console.error('Erro ao favoritar livro:', error);
        alert('Erro ao favoritar livro');
    }
}

// Duplicar livro
async function duplicarLivro(id) {
    try {
        const response = await fetch(`http://localhost:3000/api/livros/${id}`);
        const livro = await response.json();
        
        const novoLivro = {
            ...livro,
            titulo: `${livro.titulo} (Cópia)`,
            favorito: 0
        };
        delete novoLivro.id;
        delete novoLivro.criado_em;
        
        const createResponse = await fetch('http://localhost:3000/api/livros', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(novoLivro)
        });
        
        if (createResponse.ok) {
            alert('Livro duplicado com sucesso!');
            carregarLivros(paginaAtual);
            carregarEstatisticas();
        }
    } catch (error) {
        console.error('Erro ao duplicar livro:', error);
        alert('Erro ao duplicar livro');
    }
}

// Excluir livro
async function excluirLivro(id) {
    if (!confirm('Tem certeza que deseja excluir este livro?')) {
        return;
    }
    
    try {
        const response = await fetch(`http://localhost:3000/api/livros/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Livro excluído com sucesso!');
            carregarLivros(paginaAtual);
            carregarEstatisticas();
        }
    } catch (error) {
        console.error('Erro ao excluir livro:', error);
        alert('Erro ao excluir livro');
    }
}

// Aplicar filtros avançados
function aplicarFiltrosAvancados() {
    // Implementar lógica de filtros avançados se necessário
    alert('Filtros avançados ainda não implementados');
}

// Limpar filtros
function limparFiltros() {
    document.getElementById('searchInput').value = '';
    document.getElementById('yearFilter').value = '';
    document.getElementById('genreFilter').value = '';
    document.getElementById('sortSelect').value = '';
    
    searchTerm = '';
    filtroAtual = 'todos';
    
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.filter === 'todos') {
            btn.classList.add('active');
        }
    });
    
    carregarLivros(1);
}
