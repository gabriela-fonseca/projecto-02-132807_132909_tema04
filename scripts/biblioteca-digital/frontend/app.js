const API_URL = 'http://localhost:8000';

// --- Pesquisa no TMDB (via backend) ---

async function pesquisarFilmes() {
  const titulo = document.getElementById('campoPesquisa').value.trim();

  if (titulo.length < 2) {
    alert('Escreve pelo menos 2 letras para pesquisar.');
    return;
  }

  try {
    const resposta = await fetch(`${API_URL}/pesquisa/?titulo=${encodeURIComponent(titulo)}`);
    const dados = await resposta.json();
    mostrarResultadosPesquisa(dados.resultados);
  } catch (erro) {
    console.error('Erro ao pesquisar:', erro);
    alert('Não foi possível ligar ao backend. Confirma que o Docker está a correr.');
  }
}

function mostrarResultadosPesquisa(resultados) {
  const container = document.getElementById('resultadosPesquisa');
  container.innerHTML = '';

  if (resultados.length === 0) {
    container.innerHTML = '<p>Nenhum filme encontrado.</p>';
    return;
  }

  resultados.forEach(filme => {
    const card = document.createElement('div');
    card.className = 'resultado-card';
    card.innerHTML = `
      <img src="${filme.cartaz_url || ''}" alt="${filme.titulo}">
      <p>${filme.titulo} (${filme.ano || '—'})</p>
    `;
    card.addEventListener('click', () => adicionarFilme(filme.tmdb_id));
    container.appendChild(card);
  });
}

// --- Ligar o botão de pesquisa à função ---

document.getElementById('botaoPesquisar').addEventListener('click', pesquisarFilmes);

// --- Adicionar filme à biblioteca (grava no backend) ---

async function adicionarFilme(tmdbId) {
  try {
    // 1. Buscar os detalhes completos do filme no TMDB (via backend)
    const respostaDetalhes = await fetch(`${API_URL}/pesquisa/${tmdbId}`);
    const detalhes = await respostaDetalhes.json();

    // 2. Enviar esses detalhes para gravar na base de dados
    const respostaCriar = await fetch(`${API_URL}/filmes/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(detalhes),
    });

    if (respostaCriar.status === 409) {
      alert('Esse filme já está na biblioteca.');
      return;
    }

    if (!respostaCriar.ok) {
      throw new Error('Erro ao gravar filme');
    }

    alert('Filme adicionado com sucesso!');
    document.getElementById('resultadosPesquisa').innerHTML = '';
    document.getElementById('campoPesquisa').value = '';
    carregarGaleria(); // actualiza a galeria principal

  } catch (erro) {
    console.error('Erro ao adicionar filme:', erro);
    alert('Não foi possível adicionar o filme.');
  }
}

// --- Carregar e mostrar a galeria principal ---

// --- Filtros da biblioteca ---

async function carregarGaleria() {
  const texto = document.getElementById('filtroTexto').value.trim();
  const genero = document.getElementById('filtroGenero').value;
  const anoMin = document.getElementById('filtroAnoMin').value;
  const anoMax = document.getElementById('filtroAnoMax').value;
  const apenasFavoritos = document.getElementById('filtroFavoritos').checked;

  const parametros = new URLSearchParams();
  if (texto) parametros.append('pesquisa', texto);
  if (genero) parametros.append('genero', genero);
  if (anoMin) parametros.append('ano_min', anoMin);
  if (anoMax) parametros.append('ano_max', anoMax);
  if (apenasFavoritos) parametros.append('apenas_favoritos', 'true');

  try {
    const resposta = await fetch(`${API_URL}/filmes/?${parametros.toString()}`);
    const dados = await resposta.json();
    mostrarGaleria(dados.filmes);
  } catch (erro) {
    console.error('Erro ao carregar galeria:', erro);
  }
}

function limparFiltros() {
  document.getElementById('filtroTexto').value = '';
  document.getElementById('filtroGenero').value = '';
  document.getElementById('filtroAnoMin').value = '';
  document.getElementById('filtroAnoMax').value = '';
  document.getElementById('filtroFavoritos').checked = false;
  carregarGaleria();
}

document.getElementById('filtroTexto').addEventListener('input', carregarGaleria);
document.getElementById('filtroGenero').addEventListener('change', carregarGaleria);
document.getElementById('filtroAnoMin').addEventListener('input', carregarGaleria);
document.getElementById('filtroAnoMax').addEventListener('input', carregarGaleria);
document.getElementById('filtroFavoritos').addEventListener('change', carregarGaleria);
document.getElementById('botaoLimparFiltros').addEventListener('click', limparFiltros);

function mostrarGaleria(filmes) {
  const container = document.getElementById('galeria');
  container.innerHTML = '';

  if (filmes.length === 0) {
    container.innerHTML = '<p>A biblioteca está vazia. Pesquisa um filme acima para começar.</p>';
    return;
  }

  filmes.forEach(filme => {
    const card = document.createElement('div');
    card.className = 'filme-card';
    card.innerHTML = `
      <img src="${filme.cartaz_url || ''}" alt="${filme.titulo}">
      <div class="info">
        <div class="titulo">${filme.titulo}</div>
        <div class="meta">${filme.ano || '—'} · ★ ${filme.nota || '—'}</div>
      </div>
    `;
    card.addEventListener('click', () => abrirModal(filme.id));
    container.appendChild(card);
  });
}

// --- Sidebar de favoritos ---

async function carregarFavoritos() {
  try {
    const resposta = await fetch(`${API_URL}/filmes/?apenas_favoritos=true&ordenar=adicionado_em`);
    const dados = await resposta.json();
    mostrarFavoritos(dados.filmes);
  } catch (erro) {
    console.error('Erro ao carregar favoritos:', erro);
  }
}

function mostrarFavoritos(filmes) {
  const container = document.getElementById('listaFavoritos');
  container.innerHTML = '';

  filmes.forEach(filme => {
    const item = document.createElement('div');
    item.className = 'favorito-item';
    item.innerHTML = `
      <div class="nome-horizontal">${filme.titulo}</div>
      <div class="preview">
        <img src="${filme.cartaz_url || ''}" alt="${filme.titulo}">
      </div>
    `;
    item.addEventListener('click', () => abrirModal(filme.id));
    container.appendChild(item);
  });
}

async function carregarListaDesejos() {
  try {
    const resposta = await fetch(`${API_URL}/filmes/?apenas_quero_ver=true&ordenar=adicionado_em`);
    const dados = await resposta.json();
    mostrarListaDesejos(dados.filmes);
  } catch (erro) {
    console.error('Erro ao carregar lista de desejos:', erro);
  }
}

function mostrarListaDesejos(filmes) {
  const container = document.getElementById('listaQueroVer');
  container.innerHTML = '';

  filmes.forEach(filme => {
    const item = document.createElement('div');
    item.className = 'favorito-item';
    item.innerHTML = `
      <div class="nome-horizontal">${filme.titulo}</div>
      <div class="preview">
        <img src="${filme.cartaz_url || ''}" alt="${filme.titulo}">
      </div>
    `;
    item.addEventListener('click', () => abrirModal(filme.id));
    container.appendChild(item);
  });
}

// --- Modal de detalhes do filme ---

let filmeAtualId = null;

async function abrirModal(filmeId) {
  try {
    const resposta = await fetch(`${API_URL}/filmes/${filmeId}`);
    if (!resposta.ok) throw new Error('Filme não encontrado');
    const filme = await resposta.json();
    filmeAtualId = filme.id;

    // Injeta os dados de texto estruturados
    document.getElementById('modalConteudo').innerHTML = `
      <div class="modal-hero">
        <img src="${filme.cartaz_url || ''}" alt="${filme.titulo}">
        <div class="modal-info">
          <h2>${filme.titulo}</h2>
          <div class="modal-meta">
            ${filme.ano || '—'} · ${filme.duracao_min ? filme.duracao_min + ' min' : '—'} ·  ★ ${filme.nota || '—'}
            ${filme.genero_nome ? ' · ' + filme.genero_nome : ''}
          </div>
        </div>
      </div>
      <p class="modal-sinopse">${filme.sinopse || 'Sem sinopse disponível.'}</p>
      
      <div class="modal-acoes">
        <button id="botaoFavoritoModal" class="${filme.favorito ? 'activo' : ''}">
          ${filme.favorito ? '★ Remover dos favoritos' : '☆ Marcar como favorito'}
        </button>

        <button id="botaoQueroVerModal" class="${filme.quero_ver ? 'activo' : ''}">
          ${filme.quero_ver ? '✓ Remover da lista ver mais tarde' : '👁 Ver mais tarde'}
        </button>

        <button id="botaoApagarModal">🗑 Remover filme</button>
      </div>
    `;

    // --- LOGICA DO TRAILER ATUALIZADA E FORA DO STRING TEMPLATE ---
    const trailerContainer = document.getElementById('trailerContainer');
    const movieTrailer = document.getElementById('movieTrailer');

    if (filme && filme.trailer_url) {
      movieTrailer.src = filme.trailer_url;
      trailerContainer.style.display = 'block'; // Mostra a secção do trailer no modal
    } else {
      movieTrailer.src = '';
      trailerContainer.style.display = 'none';  // Oculta caso não exista trailer
    }

    document.getElementById('botaoFavoritoModal').addEventListener('click', () => alternarFavoritoModal(filme.id));
    document.getElementById('botaoApagarModal').addEventListener('click', () => apagarFilmeModal(filme.id));
    document.getElementById('botaoQueroVerModal').addEventListener('click', () => alternarQueroVerModal(filme.id));

    document.getElementById('modalOverlay').classList.add('aberto');
  } catch (erro) {
    console.error('Erro ao abrir modal:', erro);
    alert('Não foi possível carregar os detalhes do filme.');
  }
}

function fecharModal() {
  document.getElementById('modalOverlay').classList.remove('aberto');
  
  // Limpar o trailer para parar a reprodução de áudio em background imediatamente
  const movieTrailer = document.getElementById('movieTrailer');
  const trailerContainer = document.getElementById('trailerContainer');
  if (movieTrailer) movieTrailer.src = '';
  if (trailerContainer) trailerContainer.style.display = 'none';

  filmeAtualId = null;
}

async function alternarFavoritoModal(filmeId) {
  try {
    await fetch(`${API_URL}/filmes/${filmeId}/favorito`, { method: 'PATCH' });
    fecharModal();
    carregarGaleria();
    carregarFavoritos();
    carregarListaDesejos();
  } catch (erro) {
    console.error('Erro ao alternar favorito:', erro);
  }
}

async function apagarFilmeModal(filmeId) {
  if (!confirm('Tens a certeza que queres remover este filme?')) return;
  try {
    await fetch(`${API_URL}/filmes/${filmeId}`, { method: 'DELETE' });
    fecharModal();
    carregarGaleria();
    carregarFavoritos();
    carregarListaDesejos();
  } catch (erro) {
    console.error('Erro ao apagar filme:', erro);
  }
}

async function alternarQueroVerModal(filmeId) {
  try {
    await fetch(`${API_URL}/filmes/${filmeId}/quero-ver`, { method: 'PATCH' });
    fecharModal();
    carregarGaleria();
    carregarFavoritos();
    carregarListaDesejos();
  } catch (erro) {
    console.error('Erro ao alternar quero ver:', erro);
  }
}

document.getElementById('botaoFecharModal').addEventListener('click', fecharModal);
document.getElementById('modalOverlay').addEventListener('click', (evento) => {
  if (evento.target.id === 'modalOverlay') fecharModal();
});

// --- Carregar a galeria e os favoritos assim que a página abre ---

carregarGaleria();
carregarFavoritos();
carregarListaDesejos();
