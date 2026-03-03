# Documentação Ruff

[Ruff](https://docs.astral.sh/ruff/) é um **linter** e **formatador** de Python extremamente rápido.

---

## O que é linter? E formatter?

### Linter

Um **linter** analisa o código em busca de **problemas**: erros de lógica, más práticas, código morto, imports não usados, variáveis indefinidas, possíveis bugs (ex.: comparação com literal), violações de estilo que podem indicar erro (ex.: identação inconsistente). Ele **não** reescreve o código por conta própria para “ficar bonito”; ele **reporta** violações e, quando a regra permite, pode **sugerir ou aplicar correções** (ex.: remover import não usado).

- **Exemplos de regras:** “variável não usada”, “import não utilizado”, “use `x is None` em vez de `x == None`”.
- No Ruff, o linter é acionado pelo comando **`ruff check`**.

### Formatter

Um **formatter** (formatador) **reescreve** o código para um **estilo consistente**: espaços, quebras de linha, aspas, indentação, colocação de vírgulas e parênteses. Ele não procura bugs; só padroniza a aparência. Assim, todo mundo no projeto (e o próprio linter) trabalha com o mesmo padrão visual.

- **Exemplos:** “quebrar linha em 88 caracteres”, “usar aspas duplas”, “um espaço após a vírgula”.
- No Ruff, o formatador é acionado pelo comando **`ruff format`**.

### Resumo

|               | Linter                                            | Formatter                                   |
| ------------- | ------------------------------------------------- | ------------------------------------------- |
| **Foco**      | Erros, bugs, más práticas, consistência semântica | Aparência e estilo (espaços, linhas, aspas) |
| **Ruff**      | `ruff check`                                      | `ruff format`                               |
| **Substitui** | Flake8, isort, pyupgrade, autoflake, etc.         | Black                                       |

O Ruff faz **as duas coisas**: um único binário para lint e formatação, com configuração unificada e execução muito rápida.

---

## O que o Ruff pode fazer (além do básico)

- **Lint** com centenas de regras (pycodestyle, Pyflakes, isort, pyupgrade, flake8-bugbear, flake8-simplify e muitas outras), com correções automáticas (safe e unsafe).
- **Formatar** código no estilo Black (substituto direto do Black, com opções como tipo de aspas e indentação).
- **Formatar trechos de código dentro de docstrings** (opcional).
- **Explicar regras:** `ruff rule <código>` mostra a descrição da regra; útil para entender cada aviso.
- **Configuração em um lugar:** `pyproject.toml` ou `ruff.toml` para linter e formatter.
- **Supressões:** comentários `noqa`, blocos `# ruff: disable`/`enable`, e ignores por arquivo ou por regra.
- **Saída em JSON** para integração com editores e CI.
- **Modo watch:** relintar ao salvar (`ruff check --watch`).

Documentação oficial do linter: <https://docs.astral.sh/ruff/linter/>  
Documentação do formatter: <https://docs.astral.sh/ruff/formatter/>

---

## Comandos

### Linter (`ruff check`)

```bash
ruff check                          # Lint no diretório atual
ruff check path/to/code/             # Lint em um caminho (recursivo)
ruff check path/to/file.py           # Lint em um arquivo
ruff check --fix                     # Aplica correções seguras
ruff check --fix --unsafe-fixes      # Aplica também correções “unsafe”
ruff check --watch                   # Re-executa ao detectar mudanças
ruff check --diff                    # Mostra diff do que seria corrigido (sem escrever)
ruff check --output-format json      # Saída em JSON (para editores/CI)
ruff check --select E,F              # Só regras E (pycodestyle) e F (Pyflakes)
ruff check --ignore F401             # Ignora a regra F401
ruff check --extend-select B         # Adiciona regras B (bugbear) ao que já está ativo
ruff check --help                    # Lista todas as opções
```

### Formatter (`ruff format`)

```bash
ruff format                          # Formata todos os .py no diretório atual
ruff format path/to/code/             # Formata um diretório (recursivo)
ruff format path/to/file.py           # Formata um arquivo
ruff format --check                  # Só verifica; não altera arquivos (útil no CI)
ruff format --check --diff            # Mostra diff do que seria formatado
ruff format --help                    # Lista todas as opções
```

### Regras

```bash
ruff rule <CODE>                     # Explica a regra (ex.: ruff rule E501)
ruff rule --all                      # Lista todas as regras disponíveis
ruff rule E                          # Lista regras que começam com E
```

### Configuração

```bash
ruff config                          # Mostra onde o Ruff está lendo a config e o resultado
```

---

## Documentação oficial (links)

| Recurso                         | URL                                          |
| ------------------------------- | -------------------------------------------- |
| **The Ruff Linter**             | <https://docs.astral.sh/ruff/linter/>        |
| **The Ruff Formatter**          | <https://docs.astral.sh/ruff/formatter/>     |
| **Configuring Ruff**            | <https://docs.astral.sh/ruff/configuration/> |
| **Rules** (lista de regras)     | <https://docs.astral.sh/ruff/rules/>         |
| **Settings** (opções de config) | <https://docs.astral.sh/ruff/settings/>      |
| **Overview**                    | <https://docs.astral.sh/ruff/>               |

---

## Configuração

Ruff lê configuração de **`pyproject.toml`** (seção `[tool.ruff]` e `[tool.ruff.lint]` / `[tool.ruff.format]`) ou de **`ruff.toml`**.  
Consulte [Configuring Ruff](https://docs.astral.sh/ruff/configuration/) para a lista completa de opções.
