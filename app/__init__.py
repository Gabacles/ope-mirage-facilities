from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'UM-GRANDE-SEGREDO'
app.config['SQLALCHEMY_DATABASE_URL'] = "postgres://wjgwbdgthglagt:43e39ae1536b5ad5ffd17e89f592f047cd629a4a1717e5eaae306df45cf74cfd@ec2-34-193-235-32.compute-1.amazonaws.com:5432/d8igr0ggfc4kuv"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app.controller import default
