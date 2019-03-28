from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, ForeignKey
from sqlalchemy.orm import backref

from app import db
from app.serializer import Serializer

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/pessoa'
# db = SQLAlchemy(app)


class Pessoa(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    idade = db.Column(db.Integer)
    email = db.Column(db.String(120))
    cpf = db.Column(db.String(20), nullable=False)
    endereco = db.relationship("Endereco",uselist=False, back_populates="pessoa")

    def __repr__(self):
        return '<Pessoa %r>' % self.nome

class Endereco(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    uf = db.Column(db.String(2))
    cidade = db.Column(db.String(30))
    bairro = db.Column(db.String(100))
    rua = db.Column(db.String(50))
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'))
    pessoa = db.relationship("Pessoa", back_populates="endereco", uselist=False)

    def __repr__(self):
        return '<Endereco %r>' % self.nome

