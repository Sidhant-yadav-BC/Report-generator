from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path 

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    global engine
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'be9e39b38e2d79879653c4ad97888531'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .user_view import user_view
    from .admin_view import admin_view
    from .auth import auth
    from .models import Users
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    app.register_blueprint(user_view, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin_view, url_prefix='/')
    
    create_database(app)

    return app

def create_database(app):
    if not path.exists('website/'+ DB_NAME):
        with app.app_context():
            db.create_all()
  