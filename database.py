import os

import psycopg2


def inicializar_banco() -> None:
    # 1. Configurações da conexão
    config = {
        "host": "localhost",
        "database": "pratica",
        "user": "admin",
        "password": "admin",
    }

    conn = None
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        # 2. Caminho para o arquivo SQL
        caminho_sql = os.path.join("sql", "create_schema.sql")

        # 3. Lê e executa o script SQL
        if os.path.exists(caminho_sql):
            with open(caminho_sql, encoding="utf-8") as f:
                sql_script = f.read()

            cursor.execute(sql_script)
            conn.commit()
            print("Fase 1 concluída: Tabelas de Negócio e Metadados criadas!")
        else:
            print(f"Erro: Arquivo {caminho_sql} não encontrado.")

    except Exception as e:
        print(f"Erro ao conectar ou criar tabelas: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    inicializar_banco()
