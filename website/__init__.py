from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from sqlalchemy import inspect

db = SQLAlchemy()
DB_NAME = 'report_generator'
DB_PASSWORD = 'Kings92!'
DB_USERNAME = 'postgres'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'be9e39b38e2d79879653c4ad97888531'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import Users, BusinessUpdates   
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    with app.app_context():
        create_database(app)

    return app

def create_database(app):
    with app.app_context():
        if not inspect(db.engine).has_table('users') or not inspect(db.engine).has_table('business_updates'):
            db.create_all()
            print('Created database and tables')