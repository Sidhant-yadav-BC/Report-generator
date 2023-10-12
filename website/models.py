from . import db
from flask_login import UserMixin


class BusinessUpdates(db.Model):
    update_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=False))
    username= db.Column(db.String(200), nullable= False)
    user_input=db.Column(db.String(10000))
    user_output=db.Column(db.String(10000))
    service = db.Column(db.String(100))
    portfolio = db.Column(db.String(200))
    teammates = db.Column(db.String(1000), default=None)
    progress = db.Column(db.String(100))
    ai_input = db.Column(db.String(10000))
    ai_output = db.Column(db.String(10000))
    business_update=db.Column(db.String(10000))

class Users(db.Model, UserMixin):
    
    def get_id(self):
        return str(self.user_id)
    
    @property
    def id(self):
        return self.user_id
    
    user_id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False, default='user', server_default='user')
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
