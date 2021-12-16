from app import db
from datetime import date
from sqlalchemy import Date, Enum


class User(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(11), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    logradouro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)

    def __init__(self, nome, cpf, email, telefone, cep, logradouro, cidade):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.cep = cep
        self.logradouro = logradouro
        self.cidade = cidade


class Cardapio(db.Model):
    __tablename__ = 'cardapio'
    id_produto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produto = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    def __init__(self, nome_produto, quantidade):
        self.nome_produto = nome_produto
        self.quantidade = quantidade


class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey(
        'clientes.id_cliente'), nullable=False)
    status_pedido = db.Column(Enum('aberto', 'atendido', 'cancelado'))
    data = db.Column(Date, default=date.today())

    def __init__(self, id_cliente):
        self.id_cliente = id_cliente
        self.status_pedido = 'aberto'


class ItensPedido(db.Model):
    __tablename__ = 'itens_pedido'
    id_itens_pedi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey(
        'pedidos.id_pedido'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey(
        'cardapio.id_produto'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    def __init__(self, id_pedido, id_produto, quantidade):
        self.id_pedido = id_pedido
        self.id_produto = id_produto
        self.quantidade = quantidade
