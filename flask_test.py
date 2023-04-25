from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder='./')

# Rota para exibir o formulário HTML
@app.route('/')
def formulario():
    return render_template('form.html')

# Rota para processar os dados do formulário HTML
@app.route('/processar_formulario', methods=['POST'])
def processar_formulario():
    # Obtenha os valores dos campos do formulário
    nome_completo = request.form['nome_completo']
    biografia = request.form['biografia']
    data_atualizacao = request.form['data_atualizacao']

    # Estabeleça uma conexão com o banco de dados
    conn = sqlite3.connect('formulario.db')

    conn.execute('''CREATE TABLE IF NOT EXISTS formulario
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT,
        biografia TEXT,
        data_atualizacao DATE);''')

    # Insira os dados no banco
    conn.execute("INSERT INTO formulario (nome_completo, biografia, data_atualizacao) VALUES (?, ?, ?)", 
                 (nome_completo, biografia, data_atualizacao))
    conn.commit()

    # Encerre a conexão com o banco
    conn.close()

    # Exiba uma mensagem de sucesso
    return 'Dados salvos com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)