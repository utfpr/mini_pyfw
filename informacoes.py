
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder='./')

@app.route('/')
def formulario():
    return render_template('informacoes.html')

@app.route('/processar_formulario', methods=['POST'])
def processar_formulario():
    conn = sqlite3.connect('formularios.db')

    
    bio = request.form['bio']
    nome = request.form['nome']
    ultima_atualizacao = request.form['ultima_atualizacao']
    conn.execute('''CREATE TABLE IF NOT EXISTS informacoes
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        bio TEXT,
        nome VARCHAR(255),
        ultima_atualizacao DATE);''')
    conn.execute("INSERT INTO informacoes (bio, nome, ultima_atualizacao) VALUES (?, ?, ?)", 
                  (bio, nome, ultima_atualizacao))
    
    conn.commit()
    conn.close()

    return 'Dados salvos com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)
    