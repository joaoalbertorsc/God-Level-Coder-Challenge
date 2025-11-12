# 📊 Nola - Plataforma de Análise de Dados para Restaurantes

Nola é uma plataforma de Business Intelligence projetada para capacitar donos de restaurantes a explorar e visualizar seus dados operacionais de forma intuitiva. A solução oferece dashboards interativos e a capacidade de criar análises personalizadas, transformando dados brutos de vendas, produtos e clientes em insights acionáveis.

## 🚀 Origem do Projeto

Este projeto foi desenvolvido como solução para o desafio **God Level Coder**, que propôs a criação de uma ferramenta de BI específica para o setor de food service, permitindo que gestores de restaurantes pudessem tomar decisões mais estratégicas com base em seus próprios dados.

## 🛠️ Tecnologias Utilizadas

A plataforma foi construída utilizando uma arquitetura de microsserviços, com as seguintes tecnologias:

- **Frontend:** [Vue.js](https://vuejs.org/)
- **Backend:** [Python](https://www.python.org/) com [FastAPI](https://fastapi.tiangolo.com/)
- **Banco de Dados:** [PostgreSQL](https://www.postgresql.org/)
- **Cache:** [Redis](https://redis.io/)
- **Containerização:** [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)
- **Geração de Dados:** Script em Python para popular o banco com dados realistas.

## 🏁 Como Executar o Projeto (Getting Started)

Para executar o projeto localmente, você precisará ter o Docker e o Docker Compose instalados.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/lucasvieira94/nola-god-level.git
    cd nola-god-level
    ```

2.  **Construa e suba os containers:**
    O comando a seguir irá construir as imagens, iniciar os serviços (PostgreSQL, Redis, Backend, Frontend) e gerar os dados de exemplo.
    ```bash
    docker-compose up --build -d
    ```
    *Aguarde alguns minutos para que o script `data-generator` popule o banco de dados com aproximadamente 500.000 registros de vendas.*

3.  **Acesse a aplicação:**
    - **Frontend:** [http://localhost:3000](http://localhost:3000)
    - **Backend (API Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)

4.  **Para parar a aplicação:**
    ```bash
    docker-compose down
    ```

## 📂 Estrutura do Projeto

O repositório está organizado da seguinte forma:

- **/backend:** Contém a aplicação FastAPI (Python) que serve a API.
- **/frontend:** Contém a aplicação Vue.js que consome a API e renderiza os dashboards.
- **/database-schema.sql:** Script SQL para a criação do schema do banco de dados.
- **/generate_data.py:** Script Python para geração de dados de teste.
- **docker-compose.yml:** Orquestra a inicialização de todos os serviços.

---
_Nola • 2025_
