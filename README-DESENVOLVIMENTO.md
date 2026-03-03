# README de Desenvolvimento — Inteligência Competitiva e Monitoramento de Preços

Documento de planejamento e roadmap do projeto de portfólio em Engenharia de Dados. Use este arquivo como guia até as etapas finais.

---

## 1. Visão geral do projeto

**Objetivo:** Infraestrutura de dados que simula o ecossistema de um grande varejista, com foco em histórico de preços, versionamento temporal (SCD Type 2), pipeline idempotente, backfill e observabilidade.

**Escopo principal:**

- ~1.000.000 de registros de histórico de preços (dados sintéticos com Faker).
- PostgreSQL como banco de dados.
- Airflow para orquestração dos pipelines.
- Docker para ambiente reproduzível.
- CI/CD (ex.: GitHub Actions) com testes e lint (Ruff, Mypy).
- Observabilidade: tabelas de metadados (linhagem, tempo de execução, volumetria).

**Entregas de valor:** consultas otimizadas (índices, window functions, CTEs) para anomalias de preço e participação de mercado (share of voice), com resposta em milissegundos.

---

## 2. Stack e ferramentas

| Área                | Ferramenta                  | Papel no projeto                                                 |
| ------------------- | --------------------------- | ---------------------------------------------------------------- |
| Banco de dados      | PostgreSQL                  | Armazenamento relacional, SCD Type 2, índices compostos/cobertos |
| Linguagem           | Python                      | Pipeline de ingestão, geração de dados (Faker), testes           |
| Dados sintéticos    | Faker                       | Geração de preços, produtos, períodos realistas                  |
| Orquestração        | Apache Airflow              | DAGs, agendamento, retries, dependências entre tarefas           |
| Ambiente            | Docker / Docker Compose     | Postgres + Airflow + app em containers                           |
| Qualidade de código | Ruff                        | Linter e formatação                                              |
| Tipagem estática    | Mypy                        | Verificação de tipos                                             |
| Testes              | pytest                      | Testes unitários (idempotência, integridade SCD2, metadados)     |
| CI/CD               | GitHub Actions (ou similar) | Rodar Ruff, Mypy e testes a cada push/PR                         |

---

## 3. Roadmap até as etapas finais

As fases abaixo são sugestões de ordem; você pode ajustar conforme o tempo e a prioridade.

### Fase 0 — Ambiente e qualidade de código (base)

**Objetivo:** Projeto rodando localmente com lint e tipagem desde o início.

- [x] Configurar repositório (estrutura de pastas, `.gitignore`).
- [x] Definir dependências: `requirements.txt` e/ou `pyproject.toml` (Faker, psycopg2 ou asyncpg, etc.).
- [x] Configurar **Ruff** (linter + formatter) e **Mypy** (strict ou próximo).
- [x] **pre-commit** com hooks para Ruff e Mypy (ver abaixo).
- [x] Documentar comandos: como instalar, rodar lint e type-check.

---

### Fase 1 — Banco de dados e modelagem

**Objetivo:** Schema no PostgreSQL com SCD Type 2 para preços e tabelas de suporte.

- [ ] Desenhar modelo de dados: dimensões (ex.: produto, loja, concorrente) e fato de preços.
- [ ] Implementar tabela de preços com SCD Type 2 (chave substituta, `valid_from`, `valid_to`, `is_current`).
- [ ] Criar tabelas de metadados (linhagem: origem, job_id, execução; métricas: duração, volumetria).
- [ ] Scripts de DDL versionados (migrations ou SQL puro).
- [ ] Documentar decisões: por que SCD Type 2, convenção de nomes.

**Documentação:**

- [PostgreSQL — Official Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL — Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [Slowly Changing Dimensions (Kimball) — conceitos](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-2/)
- [SCD Type 2 — exemplo prático](https://en.wikipedia.org/wiki/Slowly_changing_dimension#Type_2:_Add_new_row)

---

### Fase 2 — Geração de dados e ingestão idempotente

**Objetivo:** Pipeline que gera dados sintéticos e carrega no PostgreSQL de forma idempotente.

- [ ] Módulo de geração com **Faker**: preços, produtos, datas, identificadores (locale pt_BR onde fizer sentido).
- [ ] Regras de negócio para “mudança de preço” (frequência, faixas) para alimentar SCD Type 2.
- [ ] Lógica de ingestão idempotente: mesmo período/job não duplica nem corrompe dados (chaves, `valid_from`/`valid_to`).
- [ ] Estratégia de **backfill**: carregar períodos passados sem quebrar a linha do tempo já existente.
- [ ] Gravar metadados em cada carga (job_id, início/fim, quantidade de linhas, status).

**Documentação:**

- [Faker (Python) — Documentation](https://faker.readthedocs.io/)
- [Faker — Providers](https://faker.readthedocs.io/en/stable/providers.html)
- [psycopg2 — Documentation](https://www.psycopg.org/docs/)
- [Idempotency — conceito em pipelines](https://en.wikipedia.org/wiki/Idempotence#Computer_science_meaning)

---

### Fase 3 — Orquestração com Airflow

**Objetivo:** Cargas e backfills disparados por DAGs, com retries e agendamento.

- [ ] Subir **Airflow** em Docker (imagem oficial ou Docker Compose).
- [ ] DAG de ingestão: geração de dados + carga no Postgres (idempotente).
- [ ] Parâmetros do DAG: período (data início/fim), tipo de execução (incremental vs backfill).
- [ ] DAG ou tarefas para backfill (ex.: range de datas).
- [ ] Documentar: quando cada DAG roda, variáveis e conexões usadas.

**Documentação:**

- [Apache Airflow — Documentation](https://airflow.apache.org/docs/)
- [Airflow — Quick Start](https://airflow.apache.org/docs/apache-airflow/stable/quick-start.html)
- [Airflow — Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [Airflow — Concepts (DAGs, Tasks)](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html)

---

### Fase 4 — Docker e ambiente completo

**Objetivo:** Qualquer pessoa (ou o CI) conseguir rodar o ambiente com um comando.

- [ ] **Dockerfile** para a aplicação de ingestão (se fizer sentido).
- [ ] **Docker Compose**: serviços para PostgreSQL, Airflow (e app se necessário).
- [ ] Variáveis de ambiente para conexão (DB host, user, password, port).
- [ ] Instruções no README: `docker compose up`, como acessar Airflow e o banco.
- [ ] Volume persistente para dados do Postgres.

**Documentação:**

- [Docker — Documentation](https://docs.docker.com/)
- [Docker Compose — Documentation](https://docs.docker.com/compose/)
- [Docker Compose — Compose file reference](https://docs.docker.com/compose/compose-file/)

---

### Fase 5 — SQL avançado e performance

**Objetivo:** Consultas otimizadas para análises de negócio e demonstração de domínio em SQL.

- [ ] Índices compostos e cobertos nas tabelas de preços e metadados (alinhados às consultas).
- [ ] Consultas com **window functions** (LEAD, LAG) para detecção de anomalias de preço.
- [ ] **CTEs** para cálculos em etapas (ex.: share of voice, agregados por período).
- [ ] Documentar queries: objetivo, filtros principais e ganho com índices (opcional: EXPLAIN ANALYZE).
- [ ] Scripts ou módulo para executar e (opcional) validar resultados das principais queries.

**Documentação:**

- [PostgreSQL — Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html)
- [PostgreSQL — WITH (CTEs)](https://www.postgresql.org/docs/current/queries-with.html)
- [PostgreSQL — Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [PostgreSQL — EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)

---

### Fase 6 — Testes automatizados

**Objetivo:** Testes unitários que garantam idempotência, integridade do SCD2 e metadados.

- [ ] Configurar **pytest** (e talvez pytest-cov para cobertura).
- [ ] Testes de idempotência: rodar a mesma carga duas vezes e verificar que não há duplicidade/inconsistência.
- [ ] Testes de integridade SCD Type 2: uma única chave natural não tem duas linhas com `is_current = true` no mesmo momento; `valid_from`/`valid_to` consistentes.
- [ ] Testes de metadados: após uma carga, existem registros de linhagem/volumetria esperados.
- [ ] Documentar como rodar: `pytest`, `pytest -v`, `pytest --cov`.

**Documentação:**

- [pytest — Documentation](https://docs.pytest.org/)
- [pytest — Quick Start](https://docs.pytest.org/en/stable/getting-started.html)
- [pytest-cov — Coverage plugin](https://pytest-cov.readthedocs.io/)

---

### Fase 7 — CI/CD

**Objetivo:** Lint, type-check e testes rodando automaticamente a cada push/PR.

- [ ] Workflow (ex.: **GitHub Actions**): job que instala dependências, roda Ruff, Mypy e pytest.
- [ ] Definir branch (ex.: `main`) e eventos (push, pull_request).
- [ ] Badge de status no README (opcional).
- [ ] Garantir que o ambiente do CI use a mesma versão de Python do projeto (e, se possível, Postgres para testes de integração).

**Documentação:**

- [GitHub Actions — Documentation](https://docs.github.com/en/actions)
- [GitHub Actions — Quickstart](https://docs.github.com/en/actions/quickstart)
- [GitHub Actions — Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

---

### Fase 8 — Observabilidade e documentação final

**Objetivo:** Metadados úteis e README que explique o projeto para recrutadores e entrevistadores.

- [ ] Revisar tabelas de metadados: linhagem, tempo de execução, volumetria por job/período.
- [ ] Exemplos de consultas que respondem: “qual foi a última carga?”, “quantos registros foram processados?”
- [ ] README principal: objetivo, arquitetura (diagrama em texto ou imagem), como rodar (Docker, Airflow, testes).
- [ ] Seção “Decisões”: por que SCD Type 2, idempotência, backfill, observabilidade.
- [ ] Links para este README de desenvolvimento e para documentações oficiais usadas no projeto.

---

## 4. Links rápidos por tema

| Tema                   | Links                                                                                                                                                                                                                                                             |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PostgreSQL**         | [Docs](https://www.postgresql.org/docs/) · [Tutorial](https://www.postgresql.org/docs/current/tutorial.html) · [Indexes](https://www.postgresql.org/docs/current/indexes.html) · [Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html) |
| **Airflow**            | [Docs](https://airflow.apache.org/docs/) · [Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) · [Concepts](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html)                           |
| **Docker**             | [Docs](https://docs.docker.com/) · [Compose](https://docs.docker.com/compose/)                                                                                                                                                                                    |
| **Python (qualidade)** | [Ruff](https://docs.astral.sh/ruff/) · [Mypy](https://mypy.readthedocs.io/) · [pre-commit](https://pre-commit.com/)                                                                                                                                               |
| **Testes**             | [pytest](https://docs.pytest.org/) · [pytest-cov](https://pytest-cov.readthedocs.io/)                                                                                                                                                                             |
| **CI/CD**              | [GitHub Actions](https://docs.github.com/en/actions)                                                                                                                                                                                                              |
| **Dados**              | [Faker](https://faker.readthedocs.io/) · [psycopg2](https://www.psycopg.org/docs/)                                                                                                                                                                                |
| **Modelagem**          | [SCD Type 2 (Kimball)](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-2/)                                                                                                    |

---

## 5. Ordem sugerida de execução

```
Fase 0 (Ruff, Mypy) → Fase 1 (Postgres, SCD2) → Fase 2 (Faker, ingestão idempotente + backfill)
       ↓
Fase 3 (Airflow) → Fase 4 (Docker Compose) → Fase 5 (SQL avançado) → Fase 6 (pytest) → Fase 7 (CI/CD) → Fase 8 (docs e observabilidade)
```

Você pode paralelizar depois: por exemplo, começar testes (Fase 6) assim que a ingestão (Fase 2) estiver estável, e ir evoluindo o CI (Fase 7) junto.

---

_Este documento é apenas planejamento; não contém implementação. Use os links para aprofundar em cada etapa._
