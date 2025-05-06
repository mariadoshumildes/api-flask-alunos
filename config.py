# app.py
from flask import Flask, request, jsonify
import pymysql
from config import DB_CONFIG

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        db=DB_CONFIG['database'],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    matricula = data.get('matricula')
    senha = data.get('senha')

    if not all([nome, email, matricula, senha]):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO aluno (nome, email, matricula, senha) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nome, email, matricula, senha))
            conn.commit()
    return jsonify({'message': 'Aluno cadastrado com sucesso!'}), 201

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT nome, email, matricula FROM aluno")
            alunos = cursor.fetchall()
    return jsonify(alunos), 200

if __name__ == '__main__':
    app.run(debug=True)
