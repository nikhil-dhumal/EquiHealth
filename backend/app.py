from flask import Flask
from api.base import api_base

app = Flask(__name__)
app.register_blueprint(api_base)

if __name__ == "__main__":
    app.run(debug=True)