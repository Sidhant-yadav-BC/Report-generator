# admin_view.py

from flask import Blueprint,redirect, url_for, render_template, request, session, render_template_string, send_file
from flask_login import login_required, current_user
from .models import BusinessUpdates
from . import db
from docx import Document
import io
import pandas as pd
import tempfile
import os

admin_view = Blueprint('admin_view', __name__)

@admin_view.route('/admin_landing')
@login_required
def admin_landing():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))  # Redirect to the login page
    return render_template('admin_landing.html')

@login_required
@admin_view.route('/portfolio_details', methods=['GET', 'POST'])
def portfolio_details():
    todate = request.form['toDate']
    session['todate'] = todate
    fromdate = request.form['fromDate']
    session['fromdate'] = fromdate
    portfolio = request.form['project']
    session['portfolio'] = portfolio
    service = request.form['services']
    session['service'] = service

    portfolio_details = ""

    
    if portfolio == 'all':
        updates = BusinessUpdates.query.filter(
            BusinessUpdates.date.between(fromdate, todate),
            BusinessUpdates.service.like(service)
        ).all()
    else:
        updates = BusinessUpdates.query.filter(
            BusinessUpdates.date.between(fromdate, todate),
            BusinessUpdates.portfolio.like(portfolio),
            BusinessUpdates.service.like(service)
        ).all()

    list1 = list(set(update.portfolio for update in updates))

    for x in list1:
        portfolio_details += f"\n{x}\n"
        for update in updates:
            if x == update.portfolio:
                portfolio_details += f"""
                    {update.input}
                    - {update.output}
                """

    return render_template_string(render_template('portfolio_details.html', portfolio_details=portfolio_details))

@login_required
@admin_view.route('/updated_portfolio_details', methods=['GET', 'POST'])
def update_portfolio_details():
    portfolio_details = request.form.get('portfolio-textarea')
    session["portfolio-textarea"] = portfolio_details

    return render_template_string(render_template('updated_portfolio_details.html', portfolio_details=portfolio_details))

@login_required
@admin_view.route('/download_portfolio_docx', methods=['POST'])
def download_portfolio_docx():
    portfolio_details = session.get('portfolio-textarea', '')

    doc = Document()
    doc.add_heading('Portfolio Details', level=0)
    doc.add_paragraph(portfolio_details)

    temp_docx_file = io.BytesIO()
    doc.save(temp_docx_file)
    temp_docx_file.seek(0)

    return send_file(
        temp_docx_file,
        as_attachment=True,
        download_name='portfolio_details.docx',
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

@login_required
@admin_view.route('/excel', methods=['POST'])
def index():
    todate = request.form['toDate']
    session['todate'] = todate
    fromdate = request.form['fromDate']
    session['fromdate'] = fromdate
    portfolio = request.form['project']
    session['portfolio'] = portfolio
    service = request.form['services']
    session['service'] = service

    query = ''
    df = ''

    if portfolio == 'all':
        updates = BusinessUpdates.query.filter(
            BusinessUpdates.date.between(fromdate, todate),
            BusinessUpdates.service.like(service)
        ).all()
    else:
        updates = BusinessUpdates.query.filter(
            BusinessUpdates.date.between(fromdate, todate),
            BusinessUpdates.portfolio.like(portfolio),
            BusinessUpdates.service.like(service)
        ).all()

    df = pd.DataFrame([{
        'date': update.date,
        'portfolio': update.portfolio,
        'service': update.service,
        'input': update.input,
        'output': update.output
    } for update in updates])

    table_html = df.to_html(classes='table table-bordered table-striped', index=False)

    return render_template('report.html', table_html=table_html)

@login_required
@admin_view.route('/download_xlsx', methods=['GET', 'POST'])
def download_xlsx():
    portfolio = session.get('portfolio', '')
    service = session.get('service', '')
    fromdate = session.get('fromdate', '')
    todate = session.get('todate', '')

    query = ''
    df = ''

    if portfolio == 'all':
        updates = BusinessUpdates.query.filter(
            BusinessUpdates.date.between(fromdate, todate),
            BusinessUpdates.service.like(service)
        ).all()
    else:
        updates = BusinessUpdates.query.filter(
            BusinessUpdates.date.between(fromdate, todate),
            BusinessUpdates.portfolio.like(portfolio),
            BusinessUpdates.service.like(service)
        ).all()

    df = pd.DataFrame([{
        'date': update.date,
        'portfolio': update.portfolio,
        'service': update.service,
        'input': update.input,
        'output': update.output
    } for update in updates])

    temp_dir = tempfile.mkdtemp()

    xlsx_file_path = os.path.join(temp_dir, 'data.xlsx')
    with pd.ExcelWriter(xlsx_file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)

    return send_file(xlsx_file_path, as_attachment=True, download_name='data.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

