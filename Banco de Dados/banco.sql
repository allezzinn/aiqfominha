CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(100),
    ativo BOOLEAN DEFAULT TRUE,
    admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    status VARCHAR(100),
    usuario INTEGER REFERENCES usuarios(id),
    preco NUMERIC(10,2)
);

CREATE TABLE itens_pedido (
    id SERIAL PRIMARY KEY,
    quantidade INTEGER,
    sabor VARCHAR(100),
    tamanho VARCHAR(100),
    preco_unitario NUMERIC(10,2),
    pedido INTEGER REFERENCES pedidos(id)
);
