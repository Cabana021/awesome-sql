import os

import psycopg2


def _mensagem_erro(e: BaseException) -> str:
    """Formata exceção para exibição, evitando UnicodeDecodeError em mensagens do servidor."""
    if isinstance(e, UnicodeDecodeError):
        try:
            texto = e.object.decode("latin-1")
            return f"Erro do servidor (encoding): {texto}"
        except Exception:
            return f"Erro de encoding ao ler mensagem do servidor: {type(e).__name__}"
    return repr(e)


def _executar_script(cursor: psycopg2.extensions.cursor, sql: str) -> None:
    """Executa um script SQL com múltiplos comandos (um por vez)."""
    for cmd in sql.split(";"):
        cmd = cmd.strip()
        if not cmd:
            continue
        cursor.execute(cmd)


def inicializar_banco() -> None:
    config_setup = {
        "host": "localhost",
        "database": "postgres",
        "user": "postgres",
        "password": "admin",
    }

    config_app = {
        "host": "localhost",
        "database": "pratica",
        "user": "admin",
        "password": "admin",
    }

    try:
        # 1. Tenta conectar como admin para ver se o banco já existe
        try:
            conn = psycopg2.connect(**config_app)
            print("Conectado ao banco 'pratica' com sucesso.")
        except (psycopg2.OperationalError, UnicodeDecodeError):
            print(
                "Banco 'pratica' não encontrado ou usuário 'admin' inexistente. Iniciando criação via setup..."
            )

            # Conecta no postgres para rodar o setup
            conn_setup = psycopg2.connect(**config_setup)
            cursor_setup = conn_setup.cursor()

            with open(os.path.join("sql", "create_setup.sql"), encoding="utf-8") as f:
                _executar_script(cursor_setup, f.read())

            cursor_setup.close()
            conn_setup.close()
            conn_setup = psycopg2.connect(
                host=config_setup["host"],
                database="pratica",
                user=config_setup["user"],
                password=config_setup["password"],
            )
            cur = conn_setup.cursor()
            cur.execute("GRANT USAGE ON SCHEMA public TO admin")
            cur.execute("GRANT CREATE ON SCHEMA public TO admin")
            cur.close()
            conn_setup.close()
            conn = psycopg2.connect(**config_app)

        # 2. Executa o Schema (Tabelas)
        cursor = conn.cursor()
        with open(os.path.join("sql", "create_schema.sql"), encoding="utf-8") as f:
            _executar_script(cursor, f.read())

        conn.commit()
        print("Fase 1 concluída: Tabelas criadas!")

    except Exception as e:
        print(f"Erro crítico: {_mensagem_erro(e)}")
    finally:
        if "conn" in locals() and conn:
            conn.close()


if __name__ == "__main__":
    inicializar_banco()
