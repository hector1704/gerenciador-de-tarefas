from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DATABASE_DIR = os.path.join(os.getcwd(), 'db')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'tarefas.db')

os.makedirs(DATABASE_DIR, exist_ok=True)

if not os.path.exists(DATABASE_PATH):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            data TEXT NOT NULL,
            hora TEXT NOT NULL,
            concluida INTEGER NOT NULL DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarefa_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            texto TEXT NOT NULL,
            FOREIGN KEY (tarefa_id) REFERENCES tarefas(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detalhes/<int:id>')
def detalhes(id):
    return render_template('detalhes.html', id=id)

@app.route('/api/tarefas', methods=['GET'])
def listar_tarefas():
    conn = get_db()
    tarefas = conn.execute('SELECT * FROM tarefas ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in tarefas])

@app.route('/api/tarefa/<int:id>', methods=['GET'])
def obter_tarefa(id):
    conn = get_db()
    tarefa = conn.execute('SELECT * FROM tarefas WHERE id = ?', (id,)).fetchone()
    conn.close()
    if tarefa:
        return jsonify(dict(tarefa))
    return jsonify({'erro': 'Tarefa não encontrada'}), 404

@app.route('/api/tarefa', methods=['POST'])
def criar_tarefa():
    data = request.json
    conn = get_db()
    conn.execute('INSERT INTO tarefas (titulo, descricao, data, hora, concluida) VALUES (?, ?, ?, ?, ?)',
                 (data['titulo'], data['descricao'], data['data'], data['hora'], 0))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Tarefa criada com sucesso'})

@app.route('/api/tarefa/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    data = request.json
    conn = get_db()
    conn.execute('UPDATE tarefas SET titulo = ?, descricao = ?, data = ?, hora = ? WHERE id = ?',
                 (data['titulo'], data['descricao'], data['data'], data['hora'], id))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Tarefa atualizada com sucesso'})

@app.route('/api/tarefa/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    conn = get_db()
    conn.execute('DELETE FROM tarefas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Tarefa deletada com sucesso'})

@app.route('/api/tarefa/<int:id>/concluir', methods=['PATCH'])
def concluir_tarefa(id):
    conn = get_db()
    conn.execute('UPDATE tarefas SET concluida = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Tarefa concluída'})

@app.route('/api/tarefa/<int:id>/comentarios', methods=['GET'])
def listar_comentarios(id):
    conn = get_db()
    comentarios = conn.execute('SELECT * FROM comentarios WHERE tarefa_id = ? ORDER BY id DESC', (id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in comentarios])

@app.route('/api/tarefa/<int:id>/comentarios', methods=['POST'])
def adicionar_comentario(id):
    data = request.json
    conn = get_db()
    conn.execute('INSERT INTO comentarios (tarefa_id, nome, texto) VALUES (?, ?, ?)',
                 (id, data['nome'], data['texto']))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Comentário adicionado'})

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
