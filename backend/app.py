from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from extensions import db
from config import Config
from api.base import api_base
from api.hospitals import api_hospitals
from api.complaints import api_complaints

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

from models import Hospital, Category

app.register_blueprint(api_base)
app.register_blueprint(api_hospitals)
app.register_blueprint(api_complaints)

if __name__ == "__main__":
    app.run(debug=True)