from distr_bank.routes.accounts import bp as accounts
from flask import Flask

app = Flask(__name__)
app.register_blueprint(accounts)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
