CREATE DATABASE IF NOT EXISTS crud_db;
USE crud_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    acao VARCHAR(50) NOT NULL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

DELIMITER $$

CREATE TRIGGER IF NOT EXISTS after_insert_usuario
AFTER INSERT ON usuarios
FOR EACH ROW
BEGIN
    INSERT INTO logs (usuario_id, acao) VALUES (NEW.id, 'Inserção');
END $$

CREATE TRIGGER IF NOT EXISTS after_delete_usuario
AFTER DELETE ON usuarios
FOR EACH ROW
BEGIN
    INSERT INTO logs (usuario_id, acao) VALUES (OLD.id, 'Remoção');
END $$

CREATE PROCEDURE IF NOT EXISTS atualizar_usuario(IN user_id INT, IN novo_nome VARCHAR(100))
BEGIN
    UPDATE usuarios SET nome = novo_nome WHERE id = user_id;
    INSERT INTO logs (usuario_id, acao) VALUES (user_id, 'Atualização');
END $$

CREATE PROCEDURE IF NOT EXISTS buscar_usuario(IN user_email VARCHAR(100))
BEGIN
    SELECT * FROM usuarios WHERE email = user_email;
END $$

DELIMITER ;

INSERT INTO usuarios (nome, email, senha) VALUES 
('Hector', 'hector@email.com', 'senha123'),
('Maria', 'maria@email.com', 'senha456');

CALL atualizar_usuario(1, 'Hector Santos');
CALL buscar_usuario('maria@email.com');

SELECT * FROM logs;
SELECT * FROM usuarios;
