from distr_bank.auth.routes.tokens import bp as tokens
from flask import Flask

app = Flask(__name__)
app.register_blueprint(tokens)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
