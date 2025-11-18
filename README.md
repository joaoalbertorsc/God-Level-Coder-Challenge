# 📊 Nola - Plataforma de Análise de Dados para Restaurantes

Nola é uma plataforma de Business Intelligence projetada para capacitar donos de restaurantes a explorar e visualizar seus dados operacionais de forma intuitiva. A solução oferece dashboards interativos e a capacidade de criar análises personalizadas, transformando dados brutos de vendas, produtos e clientes em insights acionáveis.

## 🚀 Origem do Projeto

Este projeto foi desenvolvido como solução para o desafio **God Level Coder**, que propôs a criação de uma ferramenta de BI específica para o setor de food service, permitindo que gestores de restaurantes pudessem tomar decisões mais estratégicas com base em seus próprios dados.

<img width="1919" height="875" alt="desafio-god-level-nola (8)" src="https://github.com/user-attachments/assets/76e17566-83f6-46b4-9bc3-be7888043d2e" />
<img width="1919" height="873" alt="desafio-god-level-nola (7)" src="https://github.com/user-attachments/assets/11e6914c-f08f-43e1-a602-ef6f2792b008" />
<img width="1919" height="869" alt="desafio-god-level-nola (6)" src="https://github.com/user-attachments/assets/83ec1686-4527-44b9-b456-24f67dc6a152" />
<img width="1919" height="874" alt="desafio-god-level-nola (5)" src="https://github.com/user-attachments/assets/6a164e2a-9a21-495a-8e19-1721cd74bb5e" />
<img width="1919" height="874" alt="desafio-god-level-nola (4)" src="https://github.com/user-attachments/assets/49e22fe2-0e7e-4b75-ab33-11fbaed60667" />
<img width="1919" height="871" alt="desafio-god-level-nola (3)" src="https://github.com/user-attachments/assets/c7ee8764-ad55-417f-84ed-229e1b3675e4" />
<img width="1919" height="871" alt="desafio-god-level-nola (2)" src="https://github.com/user-attachments/assets/2015afb6-7f34-4fa5-a85f-66f89050a6bd" />
<img width="1919" height="872" alt="desafio-god-level-nola (1)" src="https://github.com/user-attachments/assets/cc4c94c9-4c6d-49d1-9697-6d08f8869d13" />

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
