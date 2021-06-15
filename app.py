from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config.update(
    ADMIN=os.environ.get('ADMIN'),
    DB_USER=os.environ.get('DB_USER'),
    PASSWORD=os.environ.get('PASSWORD'),
    SERVER_IP=os.environ.get('SERVER_IP'),
    MAILGUN_URL=os.getenv("MAILGUN_URL"),
    MAILGUN_API=os.getenv("MAILGUN_API")
)


@app.route("/")
def home():
    return render_template("home.html")


from controllers.alerts import alert_blueprint
from controllers.stores import store_blueprint
from controllers.users import user_blueprint

app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix="/users")

if __name__ == "__main__":
    app.run(debug=True)

