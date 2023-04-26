from sys import argv
import model


def get_objects(input):
    module = __import__(input.split('.')[0])
    data = dir(module)
    end = data.index('__builtins__')
    objs = [getattr(module, obj) for obj in data[:end]]
    return objs


def get_attributes(inst):
    start = dir(inst).index('__weakref__')
    attrs = dir(inst)[start+1:]
    return attrs


def gen_form(objs):
    data_frase = '''
    <label for="VAR_NAME">SHOW_NAME:</label>
    <input type="text" id="VAR_NAME" name="VAR_NAME"><br><br>'''
    data_texto = '''
    <label for="VAR_NAME">SHOW_NAME:</label><br>
    <textarea id="VAR_NAME" name="VAR_NAME" rows="4" cols="50"></textarea><br><br>'''
    data_data = '''
    <label for="VAR_NAME">SHOW_NAME:</label>
    <input type="date" id="VAR_NAME" name="VAR_NAME"><br><br>'''
    data_html = {
        model.Frase: data_frase,
        model.Texto: data_texto,
        model.Data: data_data,
    }

    for inst in objs:
        content = '<form method="POST" action="/processar_formulario">'
        for attr in get_attributes(inst()):
            obj = getattr(inst, attr)
            field = data_html[type(obj)]
            field = field.replace('VAR_NAME', attr)
            if obj.verboso:
                field = field.replace('SHOW_NAME', obj.verboso.title())
            else:
                label = attr.replace('_', ' ').title()
                field = field.replace('SHOW_NAME', label)
            content += field
        content += '\n\t<input type="submit" value="Enviar">\n</form>'

        for obj in objs:
            with open(f'{obj.__name__.lower()}.html', 'w') as form_arq:
                form_arq.write(content)

def create_conn_db(objs):
    data_sql = {
        model.Frase: 'VARCHAR(255)',
        model.Texto: 'TEXT',
        model.Data: 'DATE',
    }
    content = ''
    for inst in objs:
        content += f'''
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder='./')

@app.route('/')
def formulario():
    return render_template('{inst.__name__.lower()}.html')

@app.route('/processar_formulario', methods=['POST'])
def processar_formulario():
    conn = sqlite3.connect('formularios.db')\n
    '''
        for attr in get_attributes(inst()):
            obj = getattr(inst, attr)
            content += f'''
    {attr} = request.form['{attr}']'''
        content += f'''
    conn.execute(\'''CREATE TABLE IF NOT EXISTS {inst.__name__.lower()}
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        '''
        cols = list()
        for item in get_attributes(inst()):
            cols.append(item)
            key = type(getattr(inst, item))
            content += f'''
        {item} {data_sql[key]},'''
        content = content[:-1] + ");\'\'\')"
        cols = ', '.join(cols)
        content += f'''
    conn.execute("INSERT INTO {inst.__name__.lower()} ({cols}) VALUES (?, ?, ?)", 
                  ({cols}))
    
    conn.commit()
    conn.close()

    return 'Dados salvos com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)
    '''

    for obj in objs:
        with open(f'{obj.__name__.lower()}.py', 'w') as app_arq:
            app_arq.write(content)


def main():
    input = argv[1]
    objs = get_objects(input)
    gen_form(objs)
    create_conn_db(objs)


if __name__ == '__main__':
    main()
