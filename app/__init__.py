from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# toolbar = DebugToolbarExtension(app)

# The user will be redirected if he was not logged in to the user account
login.login_view = 'login'

from app import routes, models, icon_routes
