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

async function carregarGaleria() {
  try {
    const resposta = await fetch(`${API_URL}/filmes/`);
    const dados = await resposta.json();
    mostrarGaleria(dados.filmes);
  } catch (erro) {
    console.error('Erro ao carregar galeria:', erro);
  }
}

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
    container.appendChild(card);
  });
}

// --- Carregar a galeria assim que a página abre ---

carregarGaleria();
