# api-astrobit  <img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/bit.gif"/>

Criação da API para os testes iniciais da plataforma website educativo Astrobit, projeto desenvolvido para a XV Mostratech, sendo a mostra tecnológica do segundo semestre do curso técnico de informática para web, na Escola Técnica da FPFtech [(Etech-FPFtech)](https://www.fpf-etech.com/).
A API possui athenticação JWT para usuários, garantindo confiabilidade e segurança.

### <img height="45" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/senior.gif"/> Configurações iniciais:
- Passo 1: Criar diretório local para armazenar o projeto.
  - Passo 2: Gerar uma *virtual enviroment (venv)*;
  ```bash
  py -m venv .venv
  ```
- Passo 3: Ativar a *venv*;
  ```bash
  .venv\Scripts\activate
- Passo 4: Atualizar o instalador de pacotes pip;  
  ```bash
  python.exe -m pip install --upgrade pip
  ```
- Passo 5: Instalar as dependências do projeto através do arquivo *requirements.txt*;
  ```bash
  pip install -r requirements.txt
  ```   
- Passo 6: Criar banco de dados relacional utilizando o SGBD [PostgreSQL](https://www.postgresql.org/) para a migração de dados da API conforme os parâmetros do arquivo `api-astrobit.config` ou ajustando conforme as portas de acesso;
- Passo 7: Realizar, mostrar e executar as migrações;
  ```bash
  python manage.py makemigrations
  ```
  ```bash
  python manage.py migrate
  ```
  <img height="28" src="https://raw.githubusercontent.com/lexmoraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/><img height="28" src="https://raw.githubusercontent.com/alexsandro-moraes/api-astrobit/refs/heads/alex-developer/enemy.gif"/>
