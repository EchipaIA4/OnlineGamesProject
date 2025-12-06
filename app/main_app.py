import os
from flask import Flask
from .extensions import db, bcrypt, login_manager, cors
from .model import user_model  # Import models so SQLAlchemy knows about them

# 1. Initialize Flask with explicit folder paths
# We go up one level ('..') to find static and templates
app = Flask(__name__, 
            static_folder='../static', 
            template_folder='../templates')

app.config['SECRET_KEY'] = 'your_super_secret_key_12345'

# 2. Database Config
# Absolute path to ensure DB is created in the project root
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'game_hub.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Init Extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
cors.init_app(app, supports_credentials=True)

# 4. Login Manager Config
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return user_model.User.query.get(int(user_id))

# 5. Register Blueprints
# We import routes here to avoid circular imports (Routes need 'app' context sometimes)
from .routes.main_routes import main_bp
from .routes.auth_routes import auth_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)

# 6. Create Database
# This runs every time the app starts to ensure tables exist
with app.app_context():
    db.create_all()