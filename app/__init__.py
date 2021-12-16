from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'UM-GRANDE-SEGREDO'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ga_user:q1w2e3r4@localhost/projeto"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app.controller import default
