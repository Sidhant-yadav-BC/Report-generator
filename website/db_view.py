from flask import Blueprint, request
from flask import render_template, flash, redirect, url_for
from .models import Projects, Portfolios
from . import db


db_view = Blueprint('db_view', __name__)

@db_view.route('/populate_portfolios', methods = ['POST', 'GET'])
def populate_portfolios():
    if request.method == 'POST':
        portfolio_name = request.form.get('portfolio')
        
        new_portfolios = Portfolios(name= portfolio_name)
        db.session.add(new_portfolios)
        db.session.commit()
        flash("Entry added to portfolios table", category='success')
        return redirect(url_for('db_view.populate_portfolios'))
    
    return render_template('populate_portfolios.html')

@db_view.route('/populate_projects', methods=['POST', 'GET'])
def populate_projects():
    if request.method == 'POST':
        portfolio_name = request.form.get('portfolio')
        portfolio = Portfolios.query.filter_by(name=portfolio_name).first()
        
        
        project_name = request.form.get('project_name')
        project_description = request.form.get('project_description')
        
        new_projects = Projects(portfolio_id= portfolio.id, name= project_name, description= project_description)
        db.session.add(new_projects)
        db.session.commit()
        flash("Entry added to projects table", category='success')
    return render_template('populate_projects.html')
    