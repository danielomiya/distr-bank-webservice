from flask import Flask
from distr_bank.accounts.routes.movements import bp as movements


app = Flask(__name__)
app.register_blueprint(movements)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
