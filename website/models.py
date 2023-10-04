from . import db
from flask_login import UserMixin


class BusinessUpdates(db.Model):
    update_id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.user_id'))
    date = db.Column(db.DateTime(timezone=False))
    portfolio = db.Column(db.String(200))
    service = db.Column(db.String(100))
    subtopics = db.Column(db.String(100))
    teammates = db.Column(db.String(1000))
    input = db.Column(db.String(10000))
    output = db.Column(db.String(10000))
    update = db.Column(db.String(10000))

class Users(db.Model, UserMixin):
    
    def get_id(self):
        return str(self.user_id)
    
    @property
    def id(self):
        return self.user_id
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    updates = db.relationship('BusinessUpdates')
