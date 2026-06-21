# [Gestor de Biblioteca de Media com Metadados Automatizados]

Com tanta informação digital, seja de assuntos sérios, como trabalhos científicos, reportagens... ou de assuntos menos importantes como livros, filmes (ou suas características), informações de jogos... os utilizadores necessitam cada vez mais de organizar todos estes conteúdos digitais. Apesar disso, não é fácil reunir toda a informação dispersa pela internet, quanto mais organizá-la. Mesmo assim, continua a ser importante a criação de um sistema centralizado para gestão de bibliotecas pessoais. 
Neste contexto, este projeto aborda o desenvolvimento de uma aplicação de gestão de biblioteca de media (filmes e/ou livros). Nesta é possivel adicionar títulos pelo utilizador com enriquecimento automático de dados.

Para este projeto foram escolhidas as APIs externas The Movie Database (TMDB) e Google Books, para organização de filmes e livros, respetivamente. O gestor de biblioteca de media com metadados automatizados utiliza a respetiva API externa, por exemplo a The Movie Database para filmes, para organizar uma biblioteca com os filmes do utilizador, armazenando os metadados ricos desse filme como o título, género, cartaz, sinopse, etc... Isto foi feito através de código backend escrito em Python (linguagem escolhida por nós, mas também podia ser em Java ou outra linguagem de programação adequada), ficheiros Docker, e uma base de dados SQL que é responsável por armazenar os filmes (ou livros) e os seus metadados.

Quando ao frontend, este fornece a parte visual do gestor de biblioteca, a parte que o utilizador realmente vê. Além de mostrar os filmes armazenados numa galeria visual, também é possível utilizar uma ferramenta de pesquisa com função de filtros, para pesquisar por filmes, por exemplo, lançados em uma certa data, ou de um género específico, etc... Esta ferramente de pesquisa com filtros funciona de forma semelhante a uma plataforma de streaming, facilitando ao utilizador encontrar o filme que pretende, ou procurar por filmes dentro de uma certa categoria. Para desenvolver esta galeria visual, utilizaram-se linguagens de programação como HTML (para criar o "corpo" dessa galeria), JavaScript (para programar funções como as de adicionar/remover filmes e de pesquisa com filtros) e CSS (para criar a parte visual).

## Arquitetura


### Arquitetura do projeto

O diagrama a seguir ilustra a arquitetura do projeto:

<p align="center">
  <img src="assets/Projeto2.drawio.png" alt="Arquitetura do projeto (esquema)" width="300"/>
</p>

Começando pelo **Frontend**, este consiste na interface com a qual o utilizador interage. É nesta camada que o utilizador realiza as ações pretendidas para obter as informações ou funcionalidades disponibilizadas pelo sistema. Estas ações são convertidas em pedidos HTTP, que são posteriormente enviados para o backend.

O **Spring Boot (Controller)** é responsável por receber os pedidos HTTP provenientes do Frontend. Ao receber um pedido, extrai os parâmetros necessários e encaminha a informação para a camada seguinte, denominada **Service Layer**.

Ao chegarmos ao **Service Layer**, encontramos a lógica de negócio da aplicação. É nesta camada que são tomadas decisões como verificar se um filme já existe na base de dados, determinar se deve ser guardado, processar e transformar dados recebidos ou decidir qual a API externa a consultar. Em outras palavras, esta camada coordena e gere o funcionamento interno da aplicação.

De seguida, o fluxo passa para o **JPA Repository**, responsável pelo acesso e gestão dos dados. Esta camada funciona como intermediária entre a lógica de negócio e a base de dados, permitindo guardar, consultar, atualizar e remover informação sem necessidade de escrever consultas SQL manualmente.

Por fim, encontramos o **PostgreSQL**, onde os dados são armazenados de forma permanente. Desta maneira, mesmo após o encerramento ou reinício da aplicação, toda a informação guardada continua disponível para futuras utilizações.

### Arquitetura do repositório

O diagrama seguinte demonstra a esquematização/organização do repositório deste trabalho, sendo que na pasta "assets" encontram-se todas as imagens relativas ao projeto e a pasta "scripts" contém todos os códigos necessários para o funcionamento do projeto. Todas estas pastas estam localizadas numa pasta principal chamada "projeto-02-132807_132909_tema04", que também contém os ficheiros "README.md"  e "LICENSE".

```
detiaveiro/ 
│ 
└── projecto-02-132807_132909_tema04/
    |
    ├── .vscode/
    |    └── settings.json
    │
    ├── assets/
    │    ├── adicao_filme_saite.png
    │    ├── adicao_pesquisa_filme_saite.png
    │    ├── biblioteca_docs.png
    │    ├── favoritos_saite.png
    │    ├── filmes.png
    │    ├── filtro_acao_saite.png
    │    ├── filtro_ano_saite.png
    │    ├── filtro_favoritos_saite.png
    │    ├── filtro_nome_saite.png
    │    ├── informacao_filme_saite.png
    │    ├── Projeto2.drawio.png
    │    ├── saite_inicial.png
    │    ├── sem_filtros_saite.png
    |    └── vermaistarde_saite.png
    │  
    ├── scripts/
    │   └── biblioteca-digital/
    |        ├──backend/
    │        |   ├── app/
    |        |   |   |
    |        |   │   ├── __init__.py
    |        |   │   ├── main.py              # ponto de entrada FastAPI
    |        |   │   ├── database.py          # ligação à base de dados
    |        |   │   ├── models.py             # modelos SQLAlchemy (tabelas)
    |        |   │   ├── schemas.py            # modelos Pydantic (validação)
    |        |   │   ├── crud.py                # operações na base de dados
    |        |   │   ├── tmdb_client.py         # cliente da API externa TMDB
    |        |   │   ├── routers/
    |        |   │   |   ├── __init__.py
    |        |   │   |   ├── filmes.py
    |        |   │   |   ├── pesquisa.py
    |        |   │   |   └── __pycache__/
    |        |   │   |         └── (...)
    |        |   │   | 
    |        |   |   └── __pycache__/
    |        |   |       └── (...)
    |        |   ├── requirements.txt
    |        |   ├── Dockerfile
    |        |   ├── docker-compose.yml
    |        |   ├── .env
    |        |   └── venv/
    |        |        └── (...)
    |        |  
    |        └── frontend/
    |             ├── index.html
    |             ├── style.css
    |             └── app.js
    │ 
    ├── README.md
    └── LICENSE
```
## Execução

### Pré-requisitos
* Integração de APIs Externas;
* SQL;
* Metadados Multimédia;
* Docker.

### Funcionamento

A lista a seguir explica como utilizar a biblioteca digital e cada passo que o programa gestor da biblioteca faz durante a sua execução.

1. Para que a biblioteca funcione, é preciso começar por executar alguns comandos no terminal. Com o comando ```cd```, ir para scripts/biblioteca-digital/backend.
2. Executar o comando ```docker compose up --build``` e esperar até aparecer a seguinte mensagem:
```
db-1       |  database system is ready to accept connections
backend-1  |  INFO: Application startup complete.
```
3. Se não houver nenhum erro, isto executa o ficheiro Docker e faz com que ele se ligue à base de dados (database.py e main.py).
4. Para verificar que o programa está a responder, abrir no browser o seguinte link: http://127.0.0.1:8000/docs
5. Abrir no browser o ficheiro index.html localizado na pasta scripts/biblioteca-digital/frontend.
6. Quando o utilizador pesquisa por um filme que pretende adicionar, o programa vai buscar as informações necessárias, ou seja, os metadados dos filmes que podem corresponder ao nome que foi pesquisado, à API externa (neste caso, a TMDB) através do ficheiro tmdb_client.py.
7. Ao clicar no filme desejado, o ficheiro schemas.py reúne os seus metadados e o filme é adicionado à biblioteca. O programa também adiciona outros dados, como a data em que o filme foi adicionado à biblioteca.
8. Se o filme já estiver na biblioteca, ou caso o utilizador pretenda remover um filme dela, isto é resolvido através do ficheiro crud.py. No caso do filme já estar na biblioteca, a página web exibe uma mensagem que informe isso ao utilizador.
9. Ainda no crud.py, se o utilizador pretender pesquisar por um filme já presente na biblioteca, pode usar a função de pesquisa.
10. Com as tabelas do ficheiro models.py, o crud.py permite ao utilizador pesquisar por filmes utilizando filtros. Estes filtros incluem título, género, ano de lançamento, data de adição à biblioteca, entre outros.
11. Por fim, quando pretender sair, abrir o terminal e premir as teclas ctrl + C. Isto irá terminar a conexão do docker.

Nota: O comando ```docker compose up --build``` só é necessário na primeira vez. Nas próximas vezes que se utilizar a biblioteca, basta escrever ```docker compose up```, sem a parte "--build".

## Aparência da biblioteca digital
A imagem abaixo mostra um exemplo de como a biblioteca se parece ao abri-la no browser.

(adicionar uma print do site quando estiver pronto)

## Autores

```markdown
## Autores

* [**Gabriela Fonseca**](https://github.com/gabriela-fonseca)
* [**Ana Teresa**] (https://github.com/AnaTeresa44)
```

## Ajudantes

Prestou apoio na escolha do tema e na definição da abordagem inicial do projeto.

```markdown
## Ajudantes

* [**Francisco Ribeiro**](https://github.com/FranciscoRibeiro03)
```

## Licença

```markdown
## Licença

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
