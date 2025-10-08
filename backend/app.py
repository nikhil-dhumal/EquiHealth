from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
from api.base import api_base

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db) 

from models import Hospital, Category

app.register_blueprint(api_base)

if __name__ == "__main__":
    app.run(debug=True)