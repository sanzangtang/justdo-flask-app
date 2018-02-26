import os
from flask import Flask, flash
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_moment import Moment

# /Users/yukuan/Mega/justdo/app
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,
            template_folder=os.path.join(basedir, 'templates'),
            )

app.config.from_object(Config)

# bootstrap
Bootstrap(app)

# database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# bcrypt
bcrypt = Bcrypt(app)

# login
login_manager = LoginManager(app)
login_manager.login_view = 'bp_user.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'alert alert-danger'

# timestamp
moment = Moment(app)

# make sure all above instances are initilized
# then import blueprint
from app.blueprints.index import bp_index
from app.blueprints.user import bp_user
from app.blueprints.dashboard import bp_dashboard

# register blueprints
app.register_blueprint(bp_index)
app.register_blueprint(bp_user)
app.register_blueprint(bp_dashboard, url_prefix='/dashboard')
