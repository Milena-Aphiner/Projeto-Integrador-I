from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
import sqlite3

app = Flask(__name__)

app.config['DATABASE'] = 'my_database.db' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'


def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_user_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, nome TEXT NOT NULL, senha TEXT NOT NULL)')
    conn.commit()
    conn.close()


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senha = db.Column(db.String(100))
    nome = db.Column(db.String(1000))

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

