# Documentação Mypy

[Mypy](https://mypy.readthedocs.io/en/stable/) é um **verificador de tipos estático** para Python. Ele analisa o código **sem executá-lo** e avisa quando variáveis e funções são usadas de forma incompatível com as anotações de tipo (**type hints**, [PEP 484](https://peps.python.org/pep-0484/)).

---

## O que é verificação de tipos estática?

Em Python, erros de tipo (ex.: somar `str` com `int`) só aparecem em **tempo de execução**. Um **type checker estático** como o Mypy lê o código e os **type hints** que você adiciona e detecta esses problemas **antes de rodar o programa**.

- **Exemplo:** `number = input("...")` → `number` é `str`. Se você fizer `number + 1`, o Mypy avisa: operando `str` e `int` não suportado.
- As anotações de tipo são como comentários para o Mypy: **não mudam o comportamento** do programa e o interpretador Python pode rodar o código mesmo com erros reportados pelo Mypy.
- Mypy suporta **tipagem gradual**: você pode ir adicionando tipos aos poucos e deixar partes do código sem tipo quando quiser.

---

## O que o Mypy oferece

- Verificação estática com base em type hints (funções, variáveis, retornos, genéricos, `Optional`, etc.).
- Sistema de tipos rico: inferência, unions, `Callable`, `Protocol`, generics, `Literal`, `TypedDict`, etc.
- Modo **strict** e opções por módulo para aumentar ou relaxar a rigidez.
- Arquivos **stub** (`.pyi`) para bibliotecas sem tipos.
- **Mypy daemon** (`dmypy`) para rodadas incrementais mais rápidas.
- Configuração via arquivo ou `pyproject.toml`.

Documentação oficial: <https://mypy.readthedocs.io/en/stable/index.html>

---

## Comandos

```bash
mypy                          # Verifica o diretório/arquivo atual (conforme config)
mypy path/to/file.py          # Verifica um arquivo
mypy path/to/package/         # Verifica um pacote
mypy --strict path/to/file.py # Modo strict (mais rigoroso)
mypy --no-incremental         # Desativa modo incremental (útil para CI)
mypy --show-error-codes       # Mostra código do erro (ex.: [arg-type])
mypy --help                   # Lista todas as opções
```

### Daemon (verificações mais rápidas em projetos grandes)

```bash
dmypy run -- path/to/code/    # Roda mypy via daemon (incremental)
dmypy run -- --strict .        # Com opções adicionais
dmypy status                  # Status do daemon
dmypy stop                    # Para o daemon
```

---

## Configuração

O Mypy pode ser configurado por:

- **`mypy.ini`** ou **`.mypy.ini`** (formato INI)
- **`pyproject.toml`** (seção `[tool.mypy]`)
- **`setup.cfg`** (seção `[mypy]`)
- Comentários inline no código: `# type: ignore[code]`

Opções comuns:

| Opção                    | Efeito                                      |
| ------------------------ | ------------------------------------------- |
| `python_version`         | Versão do Python alvo (ex.: `3.10`)         |
| `strict`                 | Ativa várias checagens rigorosas de uma vez |
| `disallow_untyped_defs`  | Exige anotações em funções                  |
| `warn_return_any`        | Avisa se função anotada retorna `Any`       |
| `ignore_missing_imports` | Ignora imports de módulos sem stubs         |

Exemplo em `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true

[[tool.mypy.overrides]]
module = "third_party.*"
ignore_missing_imports = true
```

Para a lista completa: [The mypy configuration file](https://mypy.readthedocs.io/en/stable/config_file.html).

---

## Silenciando erros

- **Na linha:** `x = coisa()  # type: ignore[return-value]`
- **No arquivo:** na primeira linha, `# mypy: ignore-errors` ou por código: `# type: ignore`
- **Por código de erro:** em config, `[[tool.mypy.overrides]]` com `disable_error_code = ["..."]`

Detalhes: [Error codes](https://mypy.readthedocs.io/en/stable/error_codes.html) e [Suppressing errors](https://mypy.readthedocs.io/en/stable/config_file.html#suppressing-errors).

---

## Documentação oficial (links)

| Recurso                         | URL                                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------------ |
| **Welcome / índice**            | <https://mypy.readthedocs.io/en/stable/index.html>                                   |
| **Getting started**             | <https://mypy.readthedocs.io/en/stable/getting_started.html>                         |
| **Type hints cheat sheet**      | <https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html>                         |
| **The mypy command line**       | <https://mypy.readthedocs.io/en/stable/command_line.html>                            |
| **The mypy configuration file** | <https://mypy.readthedocs.io/en/stable/config_file.html>                             |
| **Using pyproject.toml**        | <https://mypy.readthedocs.io/en/stable/config_file.html#using-a-pyproject-toml-file> |
| **Error codes**                 | <https://mypy.readthedocs.io/en/stable/error_codes.html>                             |
| **Common issues and solutions** | <https://mypy.readthedocs.io/en/stable/common_issues.html>                           |
