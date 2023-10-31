from . import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship


class BusinessUpdates(db.Model):
    id = db.Column(db.Integer ,primary_key=True)
    date = db.Column(db.DateTime(timezone=False))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_input = db.Column(db.String(10000))
    user_output = db.Column(db.String(10000))
    blockers = db.Column(db.String(), default = "")
    kpi = db.Column(db.String(500), default = "")
    service = db.Column(db.String(100))
    
    # Foreign key references to Projects and Portfolios
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'))
    
    teammates = db.Column(db.String(1000), default="")
    progress = db.Column(db.String(100))
    ai_input = db.Column(db.String(10000))
    ai_output = db.Column(db.String(10000))
    business_update = db.Column(db.String(10000))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('Users')
    portfolio = relationship('Portfolios')

class Portfolios(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    name = db.Column(db.String(100), nullable = False)
    
    business_updates = db.relationship('BusinessUpdates')
    projects = db.relationship('Projects')

    
class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))  # You can adjust the length as needed
    
    business_updates = db.relationship('BusinessUpdates')

class Users(db.Model, UserMixin):
    
    def get_id(self):
        return str(self.id)
    
    # @property
    # def id(self):
    # return self.id
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False, default='user', server_default='user')
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    business_updates = db.relationship('BusinessUpdates')