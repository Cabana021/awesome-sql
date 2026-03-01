# Documentação Faker (Python)

O **Faker** é uma biblioteca Python que gera dados fictícios (nomes, emails, datas, endereços, etc.) para testes, protótipos e bancos de dados de exemplo.

## Instalação

```bash
pip install Faker
```

## Uso básico

```python
from faker import Faker

fake = Faker()

# Dados em inglês (padrão)
fake.name()      # Ex: 'John Smith'
fake.email()     # Ex: 'john@example.com'
fake.address()   # Ex: '123 Main St, City, ST 12345'
```

### Locale em português (Brasil)

```python
fake = Faker("pt_BR")

fake.name()       # Ex: 'Maria Silva'
fake.email()      # Ex: 'maria.silva@email.com'
fake.city()       # Ex: 'São Paulo'
fake.street_name()  # Ex: 'Rua das Flores'
```

## Principais provedores (o que você pode gerar)

### Pessoa
| Método | Exemplo |
|--------|--------|
| `fake.name()` | Nome completo |
| `fake.first_name()` | Primeiro nome |
| `fake.last_name()` | Sobrenome |
| `fake.email()` | E-mail |
| `fake.phone_number()` | Telefone |
| `fake.date_of_birth()` | Data de nascimento |
| `fake.cpf()` | CPF (pt_BR) |

### Endereço
| Método | Exemplo |
|--------|--------|
| `fake.address()` | Endereço completo |
| `fake.street_address()` | Rua e número |
| `fake.city()` | Cidade |
| `fake.state()` | Estado |
| `fake.postcode()` | CEP |
| `fake.country()` | País |

### Data e hora
| Método | Exemplo |
|--------|--------|
| `fake.date()` | Data aleatória |
| `fake.date_this_year()` | Data no ano atual |
| `fake.date_this_decade()` | Data nesta década |
| `fake.time()` | Hora |
| `fake.date_time()` | Data e hora |

### Texto e negócio
| Método | Exemplo |
|--------|--------|
| `fake.word()` | Uma palavra |
| `fake.sentence()` | Uma frase |
| `fake.paragraph()` | Um parágrafo |
| `fake.catch_phrase()` | Frase de efeito / nome de produto |
| `fake.company()` | Nome de empresa |
| `fake.job()` | Cargo / profissão |

### Números
| Método | Exemplo |
|--------|--------|
| `fake.random_int(min=0, max=100)` | Inteiro entre min e max |
| `fake.random_number(digits=5)` | Número com N dígitos |
| `fake.random_digit()` | Um dígito (0–9) |
| `fake.latitude()` | Latitude |
| `fake.longitude()` | Longitude |

### Outros
| Método | Exemplo |
|--------|--------|
| `fake.uuid4()` | UUID |
| `fake.url()` | URL |
| `fake.user_name()` | Nome de usuário |
| `fake.password()` | Senha |
| `fake.boolean()` | True ou False |
| `fake.random_element([a, b, c])` | Um elemento da lista |

## Locales disponíveis

Você pode usar outros idiomas/regiões:

```python
Faker("en_US")   # Inglês EUA
Faker("pt_BR")   # Português Brasil
Faker("es_ES")   # Espanhol
Faker("de_DE")   # Alemão
Faker("fr_FR")   # Francês
```

[Lista completa de locales](https://faker.readthedocs.io/en/stable/locales.html)

## Uso com banco de dados (exemplo)

```python
from faker import Faker
import sqlite3

fake = Faker("pt_BR")
conn = sqlite3.connect("meu_banco.db")

for _ in range(10):
    conn.execute(
        "INSERT INTO usuarios (nome, email) VALUES (?, ?)",
        (fake.name(), fake.email())
    )
conn.commit()
conn.close()
```

## Dicas

1. **Reproduzibilidade**: use `Faker.seed(123)` para obter os mesmos dados em toda execução.
2. **Performance**: criar um único objeto `Faker()` e reutilizá-lo é mais eficiente.
3. **Customização**: é possível criar **providers** próprios para dados específicos do seu domínio.

## Referência oficial

- [Faker — faker 30.8.0 documentation](https://faker.readthedocs.io/)
