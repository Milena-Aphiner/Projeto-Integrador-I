from flask import Flask, app, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'MILENAPHINER'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/milen/Documents/MeusProjetos/Projeto-Integrador-I/projeto-integrador-I/instance/my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
   
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    senha = db.Column(db.String(64), nullable=False)

@login_manager.user_loader
def get(id):
    return User.query.get(int(id))


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        user = User.query.filter_by(nome=nome).first()
        if user and user.senha == senha:
            login_user(user)
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('usuario'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')
    return render_template('login.html')

@app.route('/usuario')
@login_required
def usuario():
    return render_template('usuario.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('homepage'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        new_user = User(nome=request.form['nome'],
                        senha=request.form['senha'])
        print(request.form)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html')


def get_db_connection():
    conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'])
    conn.row_factory = sqlite3.Row
    return conn

def create_user_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, nome TEXT NOT NULL, senha TEXT NOT NULL)')
    conn.commit()
    conn.close()



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)