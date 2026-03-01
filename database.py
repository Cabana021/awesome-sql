import sqlite3
from faker import Faker

fake = Faker("pt_BR")

DB_PATH = "pratica.db"


def criar_tabelas(conn: sqlite3.Connection) -> None:
    """Cria as tabelas do banco."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT,
            cidade TEXT,
            data_cadastro TEXT
        )
    """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            categoria TEXT
        )
    """
    )
    conn.commit()


def popular_clientes(conn: sqlite3.Connection, quantidade: int = 100000) -> None:
    """Insere clientes fictícios na tabela."""
    for _ in range(quantidade):
        conn.execute(
            """
            INSERT INTO clientes (nome, email, telefone, cidade, data_cadastro)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                fake.name(),
                fake.email(),
                fake.phone_number(),
                fake.city(),
                fake.date_this_decade().isoformat(),
            ),
        )
    conn.commit()


def popular_produtos(conn: sqlite3.Connection, quantidade: int = 100000) -> None:
    """Insere produtos fictícios na tabela."""
    categorias = ["Eletrônicos", "Roupas", "Alimentos", "Livros", "Casa"]
    for _ in range(quantidade):
        conn.execute(
            """
            INSERT INTO produtos (nome, preco, categoria)
            VALUES (?, ?, ?)
            """,
            (
                fake.catch_phrase(),
                round(fake.random_number(digits=3) / 10, 2),
                fake.random_element(categorias),
            ),
        )
    conn.commit()


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        criar_tabelas(conn)
        popular_clientes(conn)
        popular_produtos(conn)
        print(f"Banco '{DB_PATH}' criado com sucesso.")
        print("Tabelas: clientes, produtos")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
