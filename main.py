import sqlite3
from datetime import datetime

class Produto:
    def __init__(self, id=None, nome="", descricao="", quantidade=0, preco=0.0):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.quantidade = quantidade
        self.preco = preco

    def salvar(self, conexao):
        cursor = conexao.cursor()
        if self.id:
            cursor.execute("""
                UPDATE produtos SET nome=?, descricao=?, quantidade=?, preco=? WHERE id=?
            """, (self.nome, self.descricao, self.quantidade, self.preco, self.id))
        else:
            cursor.execute("""
                INSERT INTO produtos (nome, descricao, quantidade, preco) VALUES (?, ?, ?, ?)
            """, (self.nome, self.descricao, self.quantidade, self.preco))
            self.id = cursor.lastrowid
        conexao.commit()

    @staticmethod
    def buscar_por_id(conexao, id):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id=?", (id,))
        resultado = cursor.fetchone()
        if resultado:
            return Produto(*resultado)
        return None

    @staticmethod
    def listar_todos(conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos")
        return [Produto(*row) for row in cursor.fetchall()]

    def atualizar_estoque(self, conexao, quantidade_vendida):
        if self.quantidade >= quantidade_vendida:
            self.quantidade -= quantidade_vendida
            self.salvar(conexao)
            return True
        return False


class Venda:
    def __init__(self, id=None, produto_id=None, quantidade=0, data=None):
        self.id = id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.data = data or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def salvar(self, conexao):
        produto = Produto.buscar_por_id(conexao, self.produto_id)
        if not produto:
            print(f"Erro: Produto com ID {self.produto_id} não encontrado.")
            return False

        if not produto.atualizar_estoque(conexao, self.quantidade):
            print(f"Erro: Estoque insuficiente para o produto '{produto.nome}'.")
            return False

        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO vendas (produto_id, quantidade, data) VALUES (?, ?, ?)
        """, (self.produto_id, self.quantidade, self.data))
        self.id = cursor.lastrowid
        conexao.commit()
        return True

    @staticmethod
    def listar_todas(conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM vendas")
        return [Venda(*row) for row in cursor.fetchall()]


def inicializar_banco():
    try:
        conexao = sqlite3.connect("db.db")
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                quantidade INTEGER NOT NULL DEFAULT 0,
                preco REAL NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                data TEXT NOT NULL,
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
        """)

        conexao.commit()
        return conexao

    except sqlite3.Error as e:
        print(f"Erro ao conectar ou executar operação no banco de dados: {e}")
        return None


if __name__ == "__main__":
    conexao = inicializar_banco()

    if conexao:
        # Cadastrar novos produtos
        produtos = [
            Produto(nome="Água Alcalina", descricao="Água alcalina vendida em caixa", quantidade=100, preco=19.99),
            Produto(nome="Suco Natural", descricao="Suco natural de frutas", quantidade=50, preco=12.50),
            Produto(nome="Cerveja Artesanal", descricao="Cerveja artesanal premium", quantidade=200, preco=25.00)
        ]

        for produto in produtos:
            produto.salvar(conexao)

        print("Lista de Produtos:")
        for produto in Produto.listar_todos(conexao):
            print(f"ID: {produto.id}, Nome: {produto.nome}, Descrição: {produto.descricao}, Quantidade: {produto.quantidade}, Preço: {produto.preco}")

    
        vendas = [
            Venda(produto_id=1, quantidade=10), 
            Venda(produto_id=2, quantidade=5),  
            Venda(produto_id=3, quantidade=20),  ]

        for venda in vendas:
            if venda.salvar(conexao):
                print(f"Venda registrada: Produto ID {venda.produto_id}, Quantidade: {venda.quantidade}, Data: {venda.data}")
            else:
                print(f"Falha ao registrar venda para Produto ID {venda.produto_id}.")

        print("\nLista de Produtos Após Vendas:")
        for produto in Produto.listar_todos(conexao):
            print(f"ID: {produto.id}, Nome: {produto.nome}, Quantidade: {produto.quantidade}")

        print("\nLista de Vendas:")
        for v in Venda.listar_todas(conexao):
            print(f"ID: {v.id}, Produto ID: {v.produto_id}, Quantidade: {v.quantidade}, Data: {v.data}")

        conexao.close()