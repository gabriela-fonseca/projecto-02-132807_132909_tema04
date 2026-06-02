[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/xN-SHTD1)
# [Gestor de Biblioteca de Media com Metadados Automatizados]

Cada vez mais, a realização de backups dos ficheiros armazenados nos computadores torna-se essencial. Com a constante evolução tecnológica, torna-se também mais fácil para utilizadores mal-intencionados obterem acesso a informações confidenciais, trabalhos pessoais e outros dados importantes presentes nos sistemas informáticos. Para além do risco de roubo de informação, existe igualmente a possibilidade de eliminação acidental de ficheiros, seja por falhas do sistema ou por erro humano. Neste contexto, torna-se importante a existência de sistemas automáticos que garantam a segurança e preservação dos dados, reduzindo a necessidade de intervenção manual e evitando possíveis esquecimentos na realização de backups.

O projeto “Backup Automatizado para o Nextcloud” consiste no desenvolvimento de um sistema de backup automatizado utilizando Bash scripting. O sistema tem como principal função recolher os ficheiros definidos pelo utilizador e comprimi-los num único ficheiro no formato ".tar.gz". Posteriormente, o backup gerado é armazenado numa pasta sincronizada pelo Nextcloud Desktop Client, executado através do Docker.

![Bash scripting](assets/bash_scripting.png)
![Docker](assets/docker.png)
![Ficheiro ".tar.gz"](assets/ficheiro_comprimido.png)

Uma vez que esta pasta se encontra monitorizada pelo cliente Nextcloud, sempre que um novo ficheiro é adicionado, este é automaticamente sincronizado com o servidor remoto. Desta forma, o sistema garante simultaneamente um backup local e um backup na cloud, aumentando a segurança e disponibilidade dos dados armazenados.

![Servidor Nextcloud e local (ambos com backups)](assets/servidores.png)

Além disso, através da utilização do "cron", é possível automatizar completamente a execução do sistema, permitindo que os backups sejam realizados em horários previamente definidos pelo utilizador. Para a implementação deste projeto são utilizadas tecnologias como Docker, Nextcloud, Bash scripting e cron.

![Docker](assets/cron.png)

## Arquitetura


### Arquitetura do projeto

Provide a conceptual diagram explaining how the project works under the hood. 
Describe the main components, data flow, and technologies used.

[ cron ] <br/>
    ↓ <br/>
[ Script Bash ] <br/>
    ↓ <br/>
[ Backup .tar.gz ] <br/>
    ↓ <br/>
[ Pasta sincronizada ] <br/>
    ↓ <br/>
[ Nextcloud Desktop Client ] <br/>
    ↓ <br/>
[ Servidor Nextcloud ] <br/>

### Arquitetura do repositório

detiaveiro/ <br/>
│ <br/>
└── projecto-02-132807_132909_tema04/ <br/>
    │ <br/>
    ├── assets/ <br/>
    │   └── -.png <br/>
    │ <br/>
    ├── scripts/ <br/>
    │   └── -.sh <br/>
    │ <br/>
    ├── README.md <br/>
    └── LICENSE <br/>

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
* Docker;
* NextCloud ( servidor pessoal ou outro );
* Bash;
* cron;
* Linux environment (Ubuntu/Debian recomendado);


### Execução
1. Step one (e.g., clone the repository)
2. Step two (e.g., install dependencies)
3. Step three (e.g., command to run the application)

## Avaliação

Describe the evaluation process conducted to verify that the project functions correctly. 
Plots and graphs are highly welcome to demonstrate the execution and performance of the project. 
At a minimum, you should include screenshots of the working solution.

Aqui o professor quer:

- provas
- testes
- funcionamento

*Note: I will use this section to keep track of the grading for the projects.*

| Component           | Description                                                                    | Value |
| :------------------ | :----------------------------------------------------------------------------- | ----: |
| Code quality        | How well the project is coded and documented.                                  |   0.2 |
| Repository quality  | How well the repository is structured and organized.                           |   0.1 |
| Project functional  | Whether the project achieves the desired objectives.                           |   0.3 |
| Solution quality    | How effective and creative the solution is (AI-based solutions are penalized). |   0.3 |
| Additional features | If the students have added additional features not requested in the guide.     |   0.1 |

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
