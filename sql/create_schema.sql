-- 1. Dimensão: Produtos
CREATE TABLE IF NOT EXISTS produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    categoria VARCHAR(50)
);

-- 2. Dimensão: Lojas (Meus pontos de venda)
CREATE TABLE IF NOT EXISTS lojas (
    id SERIAL PRIMARY KEY,
    nome_loja VARCHAR(100) NOT NULL,
    cidade VARCHAR(50),
    ativo BOOLEAN DEFAULT TRUE
);

-- 3. Dimensão: Concorrentes (Para comparar)
CREATE TABLE IF NOT EXISTS concorrentes (
    id SERIAL PRIMARY KEY,
    nome_concorrente VARCHAR(100) NOT NULL,
    url_site VARCHAR(255)
);

-- 4. Tabela Fato: Histórico de Preços
CREATE TABLE IF NOT EXISTS historico_precos (
    id_historico SERIAL PRIMARY KEY,
    produto_id INT REFERENCES produtos(id),
    loja_id INT REFERENCES lojas(id),             -- Se for um preço meu 
    concorrente_id INT REFERENCES concorrentes(id), -- Se for preço de concorrente
    preco_venda DECIMAL(10, 2) NOT NULL,
    
    -- Controle de SCD Type 2
    data_inicio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_fim TIMESTAMP,
    versao INT DEFAULT 1,
    esta_ativo BOOLEAN DEFAULT TRUE,
    origem_dado VARCHAR(50) -- Ex: 'scraping_amazon', 'manual', 'api_interna'
);

-- Tabela de Metadados (Linhagem e Auditoria)
CREATE TABLE IF NOT EXISTS metadados_execucao (
    job_id SERIAL PRIMARY KEY,
    nome_script VARCHAR(100) NOT NULL,
    data_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_fim TIMESTAMP,
    status VARCHAR(20),       -- Ex: 'SUCESSO', 'ERRO'
    linhas_afetadas INT,      -- Volumetria
    duracao_segundos DECIMAL(10, 2) -- Métrica de performance
);