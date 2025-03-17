# Sistema de Gerenciamento de Produtos e Vendas 🛒

Este é um sistema simples para gerenciar produtos e registrar vendas, utilizando Python, SQLite e Programação Orientada a Objetos (POO). O sistema permite cadastrar produtos, registrar vendas, atualizar o estoque automaticamente e listar todas as operações realizadas.

---

## Funcionalidades 

- **Cadastro de Produtos**:
  - Adicione novos produtos com nome, descrição, quantidade e preço.
- **Registro de Vendas**:
  - Registre vendas informando o ID do produto e a quantidade vendida.
- **Atualização Automática de Estoque**:
  - Após uma venda, o estoque do produto é atualizado automaticamente.
- **Validação de Dados**:
  - Verifica se o produto existe e se há estoque suficiente antes de registrar uma venda.
- **Listagem de Produtos e Vendas**:
  - Exiba todos os produtos cadastrados e todas as vendas registradas no sistema.

---

## Estrutura do Projeto 

- `Produto`: Classe para representar produtos e suas operações (cadastro, atualização, listagem).
- `Venda`: Classe para registrar vendas e atualizar o estoque.
- Banco de dados: Contém tabelas `produtos` e `vendas`.

---

## Requisitos 

1. **Python 3.x**:
   - Certifique-se de ter o Python instalado. Você pode verificar executando:
     ```bash
     python --version
     ```
2. **Ambiente Virtual**:
   - Recomenda-se o uso de um ambiente virtual para isolar as dependências do projeto.
   - Para criar e ativar o ambiente virtual:
     ```bash
     # Criar ambiente virtual
     python -m venv venv

     # Ativar ambiente virtual
     # No Windows:
     venv\Scripts\activate
     # No Linux/Mac:
     source venv/bin/activate
     ```
   - Após ativar o ambiente virtual, você pode instalar as dependências (se houver) usando:
     ```bash
     pip install -r requirements.txt
     ```

3. **SQLite3**:
   - O SQLite3 já está incluído no Python, então não é necessário instalá-lo separadamente.

---

## Como Usar 

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
