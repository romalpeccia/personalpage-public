from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config, STRIPE_API_KEY, DEBUG
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message
#initialize any classes from extensions
app = Flask(__name__)
import stripe

app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
mail = Mail(app)
stripe.api_key = STRIPE_API_KEY


from app import routes, models