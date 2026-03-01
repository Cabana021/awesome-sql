# Prática SQL

Projeto para **estudo de SQL** usando SQLite. Inclui um script que gera um banco de dados com dados fictícios (Faker) e documentação para consulta durante os estudos.

## Objetivo

Servir de ambiente local para praticar consultas SQL, entender DDL/DML/DQL e explorar SQLite sem depender de servidor externo.

## Estrutura do projeto

```
Prática SQL/
├── database.py          # Cria o banco SQLite e popula com dados fictícios
├── query.sql            # Arquivo para suas consultas SQL
├── pratica.db           # Banco SQLite (gerado ao rodar database.py)
├── requirements.txt     # Dependências Python (Faker)
├── docs/
│   ├── documentacao_sql.md    # Guia de SQL com SQLite (DDL, DML, DQL, exemplos)
│   └── documentacao_faker.md  # Referência da biblioteca Faker
└── README.md
```

## Como usar

1. **Instalar dependências**

   ```bash
   pip install -r requirements.txt
   ```

2. **Gerar o banco de dados**

   ```bash
   python database.py
   ```

   Isso cria `pratica.db` com as tabelas **clientes** e **produtos** preenchidas com dados em português (Faker pt_BR).

3. **Praticar SQL**

   - Use um cliente SQLite (ex.: [DB Browser for SQLite](https://sqlitebrowser.org/)) abrindo `pratica.db`, ou
   - Execute consultas em Python com o módulo `sqlite3`, ou
   - Escreva e rode suas queries em `query.sql` no editor/ferramenta de sua preferência.

## Documentação (docs/)

| Arquivo | Conteúdo |
|--------|----------|
| [documentacao_sql.md](docs/documentacao_sql.md) | SQL com SQLite: DDL, DML, DQL, TCL; schema fictício (clientes, produtos, pedidos); exemplos de comandos com saídas simuladas; JOINs, agregações, subconsultas. |
| [documentacao_faker.md](docs/documentacao_faker.md) | Uso da biblioteca Faker: instalação, locale pt_BR, principais métodos (pessoa, endereço, data, texto, números) e dicas. |

## Código principal

- **database.py**: conecta em `pratica.db`, cria as tabelas `clientes` e `produtos`, e insere registros gerados pelo Faker. Execute pelo terminal para (re)criar o banco.

## Links úteis para estudo

### SQL e SQLite

- [SQLite Documentation](https://www.sqlite.org/docs.html) — documentação oficial do SQLite
- [SQLite Tutorial](https://www.sqlitetutorial.net/) — tutoriais de SQL para SQLite
- [sqlite3 — DB-API 2.0 interface for SQLite](https://docs.python.org/3/library/sqlite3.html) — módulo padrão Python

### Banco de dados e design

- [Database Design Tutorial](https://www.lucidchart.com/pages/database-diagram-database-design) — conceitos de modelagem e diagramas
- [Normalização (Wikipedia)](https://pt.wikipedia.org/wiki/Normaliza%C3%A7%C3%A3o_(bases_de_dados)) — formas normais e boas práticas
- [DB-Engines Ranking](https://db-engines.com/en/ranking) — comparação de SGBDs

### Prática e exercícios

- [SQLBolt](https://sqlbolt.com/) — exercícios interativos de SQL
- [SQL Fiddle](http://sqlfiddle.com/) — testar SQL online (vários motores)
- [W3Schools SQL](https://www.w3schools.com/sql/) — referência e exemplos básicos

### Extras

- [DB Browser for SQLite](https://sqlitebrowser.org/) — interface gráfica para SQLite
- [Faker Documentation](https://faker.readthedocs.io/) — documentação oficial do Faker (Python)
