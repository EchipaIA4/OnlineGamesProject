import os
from flask import Flask
from .extensions import db, bcrypt, login_manager, cors
from .model import user_model
from .routes.main_routes import main_bp
from .routes.auth_routes import auth_bp

# initialize Flask with explicit folder paths
app = Flask(__name__, 
            static_folder='../static', 
            template_folder='../templates')

app.config['SECRET_KEY'] = 'your_super_secret_key_12345'

# database config
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'game_hub.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
cors.init_app(app, supports_credentials=True)

# login manager config
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return user_model.User.query.get(int(user_id))

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)

# create database
# runs every time the app starts to ensure tables exist
with app.app_context():
    db.create_all()