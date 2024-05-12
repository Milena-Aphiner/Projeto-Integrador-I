from flask import Flask, render_template, redirect, request

app = Flask (__name__)
app.config['SECRET_KEY'] = 'MILENAPHINER'

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/sobrenos')
def sobrenos():
    return render_template('sobrenos.html')


@app.route('/noticias')
def noticias():
    return render_template('noticias.html')


@app.route('/doadores')
def doadores():
    return render_template('doadores.html')


@app.route('/contatos')
def contatos():
    return render_template('contatos.html')


@app.route('/login')
def login():

    nome = request.form.get('nome')
    senha = request.form.get('senha')

    return render_template('login.html')

if __name__== "__main__":
    app.run(debug=True)