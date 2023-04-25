
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder='./')

@app.route('/')
def formulario():
    return render_template('form.html')

@app.route('/processar_formulario', methods=['POST'])
def processar_formulario():
    conn = sqlite3.connect('formularios.db')

    bio = request.form['bio']
    nome = request.form['nome']
    ultima_atualizacao = request.form['ultima_atualizacao']
    