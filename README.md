[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/xN-SHTD1)
# [Gestor de Biblioteca de Media com Metadados Automatizados]

Com tanto informação, seja de assuntos sérios, como trabalhos científicos, reportagens, ... ou de assuntos menos importantes como, livros, filmes (ou suas caracteristicas), informações de jogos, ..., o user necessita cada vez mai de organizar todos estes conteúdos digitais. Apesar disso, não é fáciel reunir toda a informação dispersa pela internet, quanto mais organizá-la. Mesmo asim, continua a ser importe a criação de um sistema centralizado para gestão de bibliotecas pessoais. 
Neste contexto, o nosso projeto aborda o desenvolvimento de uma aplicação de gestão de biblioteca de media (filmes e/ou livros). Nesta é possivel adicionar títulos pelo utilizador com enriquecimento automático de dados...

Integração com APIs externas como a The Movie Database e a Google Books
Recolha automática de metadados como sinopse, imagem da capa/poster, avaliação e data de lançamento
Armazenamento da informação numa base de dados SQL
Organização e persistência dos dados da biblioteca pessoal
Possibilidade de pesquisa e filtragem de conteúdos
Interface gráfica em formato de galeria visual
Experiência semelhante a plataformas de streaming
Funcionalidades de pesquisa e filtros por tipo, rating ou ano
Projeto full-stack com integração de APIs REST
Aplicação de conceitos de base de dados e desenvolvimento web
Possibilidade de expansão com funcionalidades como favoritos, tags e recomendações

## Arquitetura


### Arquitetura do projeto

O diagrama a seguir ilustra como o projeto funciona:

<p align="center">
  <img src="assets/Projeto2.drawio.png" alt="Arquitetura do projeto (esquema)" width="300"/>
</p>

O diagrama anterior descreve a arquitetura do nosso projeto, começando pelo **Frontend**, que consiste na interface com a qual o utilizador interage. É nesta camada que o utilizador realiza as ações pretendidas para obter as informações ou funcionalidades disponibilizadas pelo sistema. Estas ações são convertidas em pedidos HTTP, que são posteriormente enviados para o backend.

O **Spring Boot (Controller)** é responsável por receber os pedidos HTTP provenientes do Frontend. Ao receber um pedido, extrai os parâmetros necessários e encaminha a informação para a camada seguinte, denominada **Service Layer**.

Ao chegarmos ao **Service Layer**, encontramos a lógica de negócio da aplicação. É nesta camada que são tomadas decisões como verificar se um filme já existe na base de dados, determinar se deve ser guardado, processar e transformar dados recebidos ou decidir qual a API externa a consultar. Em outras palavras, esta camada coordena e gere o funcionamento interno da aplicação.

De seguida, o fluxo passa para o **JPA Repository**, responsável pelo acesso e gestão dos dados. Esta camada funciona como intermediária entre a lógica de negócio e a base de dados, permitindo guardar, consultar, atualizar e remover informação sem necessidade de escrever consultas SQL manualmente.

Por fim, encontramos o **PostgreSQL**, onde os dados são armazenados de forma permanente. Desta maneira, mesmo após o encerramento ou reinício da aplicação, toda a informação guardada continua disponível para futuras utilizações.

### Arquitetura do repositório

O diagrama seguinte demostra a esquematização/organização do repositório deste trabalho, sendo que na pasta "assents" encontram-se todas as imagens relativas a este projeto e na pasta "scripts" temos todos os códigos necessários para o funcionamento do projeto. Todas estas pastas estam localizadas numa outra chamada "projeto-02-132807_132909_tema04", que também contem os ficheiros "README.md"  e "LICENSE".

```
detiaveiro/ 
│ 
└── projecto-02-132807_132909_tema04/
    │
    ├── assets/
    │   └── Projeto2.drawio.png
    │
    ├── scripts/
    │   └── backend
    │       ├── main.py
    │       
    │ 
    ├── README.md
    └── LICENSE
```

## Configuração e execução

Criação do servidor Nextcloud:
- ir ao sait do nextcloud (https://nextcloud.com/);
- seleciona a onde diz "download" e escolher a opção "Nextcloud server";
- selecionar a onde diz "comunity projects";
- escolher a opção "get docker image";
- anda paar baixo até encontrar "Base version - apache", a onde deve estar um código docker;
- copie esse código, coloque-o num ficheiro no seu computador;
- após isso, onde diz "MYSQL_ROOT_PASSWORD=" ;"MYSQL_PASSWORD=" e "MYSQL_PASSWORD=" coloque á frente, "nextcloud";
- de seguida guarde o ficheiro;
- abra o terminal, na pasta onde guardou o ficheiro;
- execute o seguinte comando : docker compose up;
- entrar em localhost:8080 e seguir a configuração do nextcloud

parte do backup:
- instala o cliente nextcloud, executando os seguintes códigos:
sudo apt update
sudo apt install nextcloud-desktop -y
- abre o nextcloud, escrevendo no terminal "nextcloud";
- ao abrir o nextcloud client, prime login;
- introduz o URL do servidor que esta no ficheiro docker, que é "http://localhost:8080";
- seguir os passos que aparecem de seguida;
- coloca no browser o mesmo URL;
- autoriza o cliente;
- seleciona a pasta de ficheiros que se encontra no canto superior esquerdo, da página;
- agora, passamos ao cron. Voltando ao terminal e executa o comando:
crontab -e
- Acrescenta no fim a seguinte linha de texto:
* * * * * bash  /home/gabriela/Documentos/Secretaria/LSS/projeto1/projecto-01-132807_132909_tema03/scripts/bash_gabi.sh
- colocar o horario em que se pretende que os backups sejam feitos em "* * * * *".
(visitar o sait https://crontab.guru/#*_*_*_*_* para ajuda)

### Pré-requisitos
* Integração de APIs Externas;
* SQL;
* Metadados Multimédia;
* Docker.

### Execução
1. Step one (e.g., clone the repository)
2. Step two (e.g., install dependencies)
3. Step three (e.g., command to run the application)

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
