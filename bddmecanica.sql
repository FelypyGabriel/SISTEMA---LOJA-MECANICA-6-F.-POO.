CREATE DATABASE IF NOT EXISTS dbMecanica;
USE dbMecanica;
DROP TABLE IF EXISTS peca_ordem;
DROP TABLE IF EXISTS ordem_servico;
DROP TABLE IF EXISTS peca;
DROP TABLE IF EXISTS VEICULO;
DROP TABLE IF EXISTS MECANICO;
DROP TABLE IF EXISTS Cliente;


CREATE TABLE Cliente (
  id_cliente INT PRIMARY KEY,
  nome VARCHAR(100),
  telefone VARCHAR(20),
  email VARCHAR(100),
  endereco VARCHAR(150)
);

CREATE TABLE VEICULO (
  id_veiculo INT PRIMARY KEY,
  placa VARCHAR(10) UNIQUE,
  marca VARCHAR(50),
  modelo VARCHAR(50),
  ano INT,
  id_cliente INT,
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);

CREATE TABLE MECANICO (
  id_mecanico INT PRIMARY KEY,
  nome VARCHAR(100),
  especialidade VARCHAR(50),
  telefone VARCHAR(20)
);

CREATE TABLE ordem_servico (
  id_ordem INT PRIMARY KEY,
  data_entrada DATE,
  data_saida DATE,
  descricao_servico TEXT,
  valor_total DECIMAL(10,2),
  id_veiculo INT,
  id_mecanico INT,
  FOREIGN KEY (id_veiculo) REFERENCES VEICULO(id_veiculo),
  FOREIGN KEY (id_mecanico) REFERENCES MECANICO(id_mecanico)
);

CREATE TABLE peca (
  id_peca INT PRIMARY KEY,
  nome VARCHAR(100),
  fabricante VARCHAR(100),
  preco_unitario DECIMAL(10,2),
  estoque INT
);

CREATE TABLE peca_ordem (
  id_ordem INT,
  id_peca INT,
  quantidade INT,
  PRIMARY KEY (id_ordem, id_peca),
  FOREIGN KEY (id_ordem) REFERENCES ordem_servico(id_ordem),
  FOREIGN KEY (id_peca) REFERENCES peca(id_peca)
);

-- Inserções

INSERT INTO Cliente VALUES
(1, 'João Silva', '9999-1234', 'joao@gmail.com', 'Rua A, 100'),
(2, 'Maria Souza', '9888-4321', 'maria@gmail.com', 'Rua B, 200'),
(3, 'Carlos Lima', '9777-5678', 'carlos@gmail.com', 'Rua C, 300'),
(4, 'Ana Paula', '9666-7890', 'ana@gmail.com', 'Rua D, 400'),
(5, 'Lucas Mendes', '9555-3456', 'lucas@gmail.com', 'Rua E, 500');

SELECT * FROM Cliente;

INSERT INTO VEICULO VALUES
(1, 'ABC-1234', 'Fiat', 'Uno', 2012, 1),
(2, 'DEF-5678', 'Ford', 'Ka', 2015, 2),
(3, 'GHI-9012', 'VW', 'Gol', 2018, 3),
(4, 'JKL-3456', 'Chevrolet', 'Onix', 2020, 4),
(5, 'MNO-7890', 'Hyundai', 'HB20', 2021, 5);

SELECT * FROM VEICULO;

INSERT INTO MECANICO VALUES
(1, 'Pedro Gomes', 'Motor', '99999-1111'),
(2, 'Fernanda Dias', 'Elétrica', '99999-2222'),
(3, 'Ricardo Almeida', 'Freios', '99999-3333'),
(4, 'Lucas Rocha', 'Suspensão', '99999-4444'),
(5, 'Juliana Nunes', 'Injeção', '99999-5555');

INSERT INTO ordem_servico VALUES
(1, '2025-05-01', '2025-05-03', 'Troca de óleo e filtro', 150.00, 1, 1),
(2, '2025-05-02', NULL, 'Revisão elétrica', NULL, 2, 2),
(3, '2025-05-04', NULL, 'Reparo nos freios', NULL, 3, 3),
(4, '2025-05-05', '2025-05-06', 'Alinhamento e balanceamento', 120.00, 4, 4),
(5, '2025-05-07', NULL, 'Diagnóstico injeção eletrônica', NULL, 5, 5);

INSERT INTO peca VALUES
(1, 'Filtro de óleo', 'Bosch', 25.00, 20),
(2, 'Lâmpada Farol', 'Philips', 15.00, 30),
(3, 'Pastilha de freio', 'Cobreq', 80.00, 15),
(4, 'Amortecedor', 'Monroe', 200.00, 10),
(5, 'Sensor de injeção', 'Delphi', 180.00, 5);

INSERT INTO peca_ordem VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 1),
(4, 4, 2),
(5, 5, 1);

-- Consultas
SHOW TABLES;
SELECT * FROM Clientes;
SELECT 
  c.nome AS cliente,
  v.placa,
  os.descricao_servico
FROM ordem_servico os
JOIN veiculo v ON os.id_veiculo = v.id_veiculo
JOIN cliente c ON v.id_cliente = c.id_cliente;
