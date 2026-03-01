# Documentação SQL com SQLite3

Guia para estudo de SQL usando SQLite3: categorias da linguagem, schema de exemplo e comandos com saídas simuladas.

---

## 1. O que é SQL e categorias da linguagem

**SQL** (Structured Query Language) é a linguagem padrão para definir e manipular dados em bancos relacionais. Ela se divide em categorias conforme a função dos comandos:

| Sigla   | Nome                         | Função                                               | Exemplos                      |
| ------- | ---------------------------- | ---------------------------------------------------- | ----------------------------- |
| **DDL** | Data Definition Language     | Definir e alterar estrutura (tabelas, índices, etc.) | `CREATE`, `ALTER`, `DROP`     |
| **DML** | Data Manipulation Language   | Inserir, atualizar e deletar dados                   | `INSERT`, `UPDATE`, `DELETE`  |
| **DQL** | Data Query Language          | Consultar dados                                      | `SELECT`                      |
| **DCL** | Data Control Language        | Controle de acesso (menos usado no SQLite)           | `GRANT`, `REVOKE`             |
| **TCL** | Transaction Control Language | Controle de transações                               | `BEGIN`, `COMMIT`, `ROLLBACK` |

No estudo do dia a dia, o foco costuma ser **DDL**, **DML** e **DQL**.

---

## 2. Banco de dados fictício: schema

Vamos usar um modelo simples de **loja**: clientes, produtos e pedidos.

### 2.1 Diagrama das tabelas

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    clientes     │       │     pedidos     │       │    produtos     │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │───┐   │ id (PK)         │       │ id (PK)         │
│ nome            │   │   │ cliente_id (FK) │◄──────│ nome            │
│ email           │   └──►│ data_pedido     │       │ preco           │
│ telefone        │       │ total           │       │ categoria       │
│ cidade          │       └────────┬────────┘       └────────┬────────┘
│ data_cadastro   │                │                         │
└─────────────────┘                │       ┌─────────────────┴───────┐
                                   │       │      itens_pedido       │
                                   │       ├─────────────────────────┤
                                   └──────►│ pedido_id (FK)          │
                                           │ produto_id (FK)         │
                                           │ quantidade              │
                                           │ preco_unitario          │
                                           └─────────────────────────┘
```

### 2.2 DDL – Criação do schema (CREATE TABLE)

```sql
-- Tabela de clientes
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT,
    cidade TEXT,
    data_cadastro TEXT
);

-- Tabela de produtos
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    categoria TEXT
);

-- Tabela de pedidos (referencia clientes)
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    data_pedido TEXT NOT NULL,
    total REAL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Tabela de itens do pedido (relaciona pedidos e produtos)
CREATE TABLE itens_pedido (
    pedido_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    PRIMARY KEY (pedido_id, produto_id),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);
```

### 2.3 Dados de exemplo (para simulação)

**clientes**

| id  | nome         | email           | telefone        | cidade         | data_cadastro |
| --- | ------------ | --------------- | --------------- | -------------- | ------------- |
| 1   | Ana Silva    | ana@email.com   | (11) 99999-0001 | São Paulo      | 2023-01-15    |
| 2   | Bruno Santos | bruno@email.com | (21) 98888-0002 | Rio de Janeiro | 2023-02-20    |
| 3   | Carla Lima   | carla@email.com | (31) 97777-0003 | Belo Horizonte | 2023-03-10    |

**produtos**

| id  | nome            | preco   | categoria   |
| --- | --------------- | ------- | ----------- |
| 1   | Notebook Pro    | 4500.00 | Eletrônicos |
| 2   | Mouse Wireless  | 89.90   | Eletrônicos |
| 3   | Camiseta Básica | 49.90   | Roupas      |
| 4   | Livro SQL       | 79.00   | Livros      |

**pedidos**

| id  | cliente_id | data_pedido | total   |
| --- | ---------- | ----------- | ------- |
| 1   | 1          | 2024-01-05  | 4589.90 |
| 2   | 2          | 2024-01-06  | 128.90  |
| 3   | 1          | 2024-01-10  | 49.90   |

**itens_pedido**

| pedido_id | produto_id | quantidade | preco_unitario |
| --------- | ---------- | ---------- | -------------- |
| 1         | 1          | 1          | 4500.00        |
| 1         | 2          | 1          | 89.90          |
| 2         | 2          | 1          | 89.90          |
| 2         | 4          | 1          | 79.00          |
| 3         | 3          | 1          | 49.90          |

---

## 3. DDL – Definição de estrutura

### 3.1 CREATE TABLE

Já mostrado acima. Resumo: define tabelas, colunas, tipos, `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`.

### 3.2 ALTER TABLE – adicionar coluna

```sql
ALTER TABLE clientes ADD COLUMN uf TEXT;
```

_Não retorna linhas; a estrutura da tabela é alterada._

### 3.3 DROP TABLE – remover tabela

```sql
-- Cuidado: apaga a tabela e os dados!
DROP TABLE IF EXISTS itens_pedido;
DROP TABLE IF EXISTS pedidos;
```

---

## 4. DML – Manipulação de dados

### 4.1 INSERT – inserir linhas

```sql
INSERT INTO clientes (nome, email, telefone, cidade, data_cadastro)
VALUES ('Diego Oliveira', 'diego@email.com', '(11) 96666-0004', 'Curitiba', '2024-01-01');
```

_Uma linha inserida. Para conferir:_

```sql
SELECT * FROM clientes WHERE nome = 'Diego Oliveira';
```

**Saída simulada:**

```
id  nome             email           telefone        cidade   data_cadastro
--  ---------------- --------------- --------------- -------- -------------
4   Diego Oliveira   diego@email.com (11) 96666-0004 Curitiba 2024-01-01
```

Inserir várias linhas de uma vez:

```sql
INSERT INTO produtos (nome, preco, categoria) VALUES
    ('Teclado Mecânico', 350.00, 'Eletrônicos'),
    ('Webcam HD', 220.00, 'Eletrônicos');
```

### 4.2 UPDATE – atualizar linhas

```sql
UPDATE produtos SET preco = 84.90 WHERE id = 4;
```

_Altera o preço do produto com id 4. Para conferir:_

```sql
SELECT id, nome, preco FROM produtos WHERE id = 4;
```

**Saída simulada:**

```
id  nome       preco
--  ---------- ------
4   Livro SQL  84.90
```

Atualizar mais de uma coluna:

```sql
UPDATE clientes SET cidade = 'Campinas', telefone = '(19) 95555-0000' WHERE id = 1;
```

### 4.3 DELETE – remover linhas

```sql
DELETE FROM itens_pedido WHERE pedido_id = 3 AND produto_id = 3;
```

_Remove o item do pedido 3. Para conferir:_

```sql
SELECT * FROM itens_pedido WHERE pedido_id = 3;
```

**Saída simulada:** _(nenhuma linha – tabela vazia para esse pedido)_

```
(empty)
```

---

## 5. DQL – Consultas (SELECT)

### 5.1 SELECT simples – todas as colunas

```sql
SELECT * FROM clientes;
```

**Saída simulada:**

```
id  nome           email             telefone         cidade          data_cadastro
--  -------------- ----------------- ---------------- --------------- -------------
1   Ana Silva      ana@email.com     (11) 99999-0001  São Paulo       2023-01-15
2   Bruno Santos   bruno@email.com   (21) 98888-0002  Rio de Janeiro  2023-02-20
3   Carla Lima     carla@email.com   (31) 97777-0003  Belo Horizonte  2023-03-10
```

### 5.2 SELECT com colunas específicas

```sql
SELECT nome, cidade, email FROM clientes;
```

**Saída simulada:**

```
nome           cidade          email
-------------- --------------- -----------------
Ana Silva      São Paulo       ana@email.com
Bruno Santos   Rio de Janeiro  bruno@email.com
Carla Lima     Belo Horizonte  carla@email.com
```

### 5.3 WHERE – filtrar linhas

```sql
SELECT nome, preco FROM produtos WHERE categoria = 'Eletrônicos';
```

**Saída simulada:**

```
nome             preco
---------------- -------
Notebook Pro     4500.00
Mouse Wireless   89.90
```

### 5.4 ORDER BY – ordenar

```sql
SELECT nome, preco FROM produtos ORDER BY preco DESC;
```

**Saída simulada:**

```
nome             preco
---------------- -------
Notebook Pro     4500.00
Mouse Wireless    89.90
Camiseta Básica   49.90
Livro SQL         79.00
```

### 5.5 LIMIT e OFFSET – paginação

```sql
SELECT id, nome FROM clientes ORDER BY id LIMIT 2 OFFSET 1;
```

**Saída simulada:**

```
id  nome
--  --------------
2   Bruno Santos
3   Carla Lima
```

### 5.6 Funções de agregação

```sql
SELECT
    COUNT(*) AS total_clientes,
    COUNT(cidade) AS com_cidade,
    SUM(total) AS soma_pedidos,
    AVG(total) AS media_pedido,
    MIN(preco) AS menor_preco,
    MAX(preco) AS maior_preco
FROM clientes, pedidos, produtos;
```

_Em um banco real você usaria JOINs; aqui é só para ilustrar as funções._

**Saída simulada (conceitual):**

```
total_clientes  com_cidade  soma_pedidos  media_pedido  menor_preco  maior_preco
--------------  ----------  ------------  ------------  -----------  -----------
12              12          4768.70       1589.57       49.90        4500.00
```

Exemplo mais realista:

```sql
SELECT COUNT(*) AS total_pedidos, SUM(total) AS faturamento FROM pedidos;
```

**Saída simulada:**

```
total_pedidos  faturamento
-------------  -----------
3              4768.70
```

### 5.7 GROUP BY – agrupar resultados

```sql
SELECT categoria, COUNT(*) AS qtd, AVG(preco) AS preco_medio
FROM produtos
GROUP BY categoria;
```

**Saída simulada:**

```
categoria    qtd  preco_medio
-----------  ---  -----------
Eletrônicos  2    2294.95
Roupas       1    49.90
Livros       1    79.00
```

### 5.8 HAVING – filtrar grupos

```sql
SELECT categoria, COUNT(*) AS qtd
FROM produtos
GROUP BY categoria
HAVING COUNT(*) >= 2;
```

**Saída simulada:**

```
categoria    qtd
-----------  ---
Eletrônicos  2
```

### 5.9 JOIN – juntar tabelas

**INNER JOIN** (apenas linhas que existem nas duas tabelas):

```sql
SELECT p.id, p.data_pedido, c.nome AS cliente, p.total
FROM pedidos p
INNER JOIN clientes c ON p.cliente_id = c.id;
```

**Saída simulada:**

```
id  data_pedido  cliente       total
--  -----------  ------------- -------
1   2024-01-05   Ana Silva     4589.90
2   2024-01-06   Bruno Santos  128.90
3   2024-01-10   Ana Silva    49.90
```

**JOIN com várias tabelas** (pedidos + itens + produtos):

```sql
SELECT
    ped.id AS pedido_id,
    c.nome AS cliente,
    pr.nome AS produto,
    i.quantidade,
    i.preco_unitario,
    (i.quantidade * i.preco_unitario) AS subtotal
FROM pedidos ped
INNER JOIN clientes c ON ped.cliente_id = c.id
INNER JOIN itens_pedido i ON i.pedido_id = ped.id
INNER JOIN produtos pr ON pr.id = i.produto_id
ORDER BY ped.id, pr.nome;
```

**Saída simulada:**

```
pedido_id  cliente       produto          quantidade  preco_unitario  subtotal
---------  ------------- ---------------- ----------- --------------- --------
1          Ana Silva     Mouse Wireless   1           89.90           89.90
1          Ana Silva     Notebook Pro     1           4500.00         4500.00
2          Bruno Santos  Livro SQL        1           79.00           79.00
2          Bruno Santos  Mouse Wireless   1           89.90           89.90
3          Ana Silva     Camiseta Básica  1           49.90           49.90
```

**LEFT JOIN** (mantém todas as linhas da tabela à esquerda):

```sql
SELECT c.nome, p.id AS pedido_id, p.total
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id;
```

**Saída simulada:** _(Carla não tem pedido; pedido_id e total ficam NULL)_

```
nome           pedido_id  total
-------------- ---------- -------
Ana Silva      1          4589.90
Ana Silva      3          49.90
Bruno Santos   2          128.90
Carla Lima     (NULL)     (NULL)
```

### 5.10 Subconsultas (subqueries)

```sql
SELECT nome, preco FROM produtos
WHERE preco > (SELECT AVG(preco) FROM produtos);
```

**Saída simulada:**

```
nome           preco
-------------- -------
Notebook Pro   4500.00
```

### 5.11 LIKE – busca por padrão

```sql
SELECT * FROM clientes WHERE nome LIKE '%Silva%';
```

**Saída simulada:**

```
id  nome        email           telefone         cidade     data_cadastro
--  ----------- --------------- ----------------  ---------  -------------
1   Ana Silva   ana@email.com   (11) 99999-0001   São Paulo  2023-01-15
```

- `%` = qualquer sequência de caracteres
- `_` = um único caractere

### 5.12 IN e BETWEEN

```sql
SELECT * FROM produtos WHERE categoria IN ('Eletrônicos', 'Livros');
SELECT * FROM produtos WHERE preco BETWEEN 50 AND 500;
```

---

## 6. TCL – Transações (SQLite)

Agrupar várias operações em uma transação garante que todas sejam aplicadas ou nenhuma:

```sql
BEGIN TRANSACTION;
INSERT INTO pedidos (cliente_id, data_pedido, total) VALUES (2, '2024-02-01', 350.00);
INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
VALUES (4, 1, 1, 350.00);
COMMIT;
```

Se algo der errado, use `ROLLBACK;` para desfazer desde o último `BEGIN`.

---

## 7. Resumo rápido por categoria

| Categoria | Comandos                               | Uso                                       |
| --------- | -------------------------------------- | ----------------------------------------- |
| **DDL**   | CREATE, ALTER, DROP                    | Criar/alterar/remover tabelas e estrutura |
| **DML**   | INSERT, UPDATE, DELETE                 | Inserir, atualizar e apagar dados         |
| **DQL**   | SELECT (+ WHERE, JOIN, GROUP BY, etc.) | Consultar dados                           |
| **TCL**   | BEGIN, COMMIT, ROLLBACK                | Controlar transações                      |

---

## 8. Usando no Python (sqlite3)

```python
import sqlite3

conn = sqlite3.connect("pratica.db")
conn.row_factory = sqlite3.Row  # opcional: linhas como dicionário

cur = conn.cursor()
cur.execute("SELECT nome, cidade FROM clientes LIMIT 3")
for row in cur:
    print(dict(row))

conn.close()
```

Para estudo puro de SQL, use o **DB Browser for SQLite** ou o próprio Python com o banco gerado por `database.py`.
