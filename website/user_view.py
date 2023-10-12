from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import openai
import dotenv
import re
from .models import BusinessUpdates
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from . import db
from datetime import datetime


user_view = Blueprint('user_view', __name__)

dotenv.load_dotenv()


# Get the OpenAI API key from environment variables
api_key = os.getenv("OPEN_AI_API")


# Initialize the OpenAI API client with the API key
openai.api_key = api_key



# Initialize variables for portfolio, service, and GPT-3 response
portfolio = ''
service = ''
gpt_response = ''


# landing page for normal user
@user_view.route('/home', methods=['POST', 'GET'])
@user_view.route('/', methods=['POST', 'GET'])
@user_view.route("/user_form", methods=['POST', 'GET'])
@login_required
def user_form():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))  # Redirect to the login page
    else:
        return render_template('user_form.html', username=current_user.username)


# Define the route for processing the form submission
@user_view.route('/process_form', methods=['POST'])
def process_form():
    input = request.form['work']
    portfolio = request.form['project']
    service = request.form['services']

    # Use the OpenAI API to generate a response based on user input
    prompts = [
        {
            'role': 'system',
            'content': """
            You are a professional business report generator. Your task is to create a detailed business report in the following format, which includes sections for input, output, and a business update. Maintain a high level of professionalism in the language and presentation of the report.

            Please adhere to the specific format provided below:

            INPUT:
            Generate a 3-4 word long name for a response that focuses on the work done this week. Be concise.

            OUTPUT:
            Generate a concise one-line response that focuses on the outcome of the work done this week. Highlight aspects such as efficiency gains, reduced efforts, time savings, or other relevant results.

            BUSINESS UPDATE:
            Generate a succinct one-line statement that focuses on the updates related to the business from the generated output. Discuss how efficiency is improved, efforts are reduced, or any other pertinent updates that align with the organization's goals and objectives.
            """
        },
        {
            'role': 'user',
            'content': f"{input}"
        }
    ]

    # Use the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompts,
        temperature=0.0  # Adjust as needed
    )

    # Extract the GPT-3 response
    gpt_response = response.choices[0].message.content
    # gpt_response= input+ " "+ portfolio+ " "+service

    # Store the response and other session data
    session['submission'] = gpt_response
    session['gpt_response'] = gpt_response
    session['portfolio'] = portfolio
    session['service'] = service
    session['sub_project']= request.form['sub_project']
    session['team']= request.form['team']
    session['date'] = request.form['selected_date']
    session['progress'] = request.form['progress']

    # Redirect to the submission editing page
    return redirect(url_for('user_view.submission_output_editable'))

# Define the route for the submission editing page
@login_required
@user_view.route('/submission_output_editable')
def submission_output_editable():
    text = session.get('gpt_response', '')

    input_pattern = r'INPUT:(.*?)OUTPUT:'
    output_pattern = r'OUTPUT:(.*?)BUSINESS UPDATE:'
    business_update_pattern = r'BUSINESS UPDATE:(.*)'

    # Use re.DOTALL to match across multiple lines
    input_match = re.search(input_pattern, text, re.DOTALL)
    output_match = re.search(output_pattern, text, re.DOTALL)
    business_update_match = re.search(business_update_pattern, text, re.DOTALL)

    # Extract the matched content
    input_section = input_match.group(1).strip() if input_match else ""
    output_section = output_match.group(1).strip() if output_match else ""
    business_update_section = business_update_match.group(1).strip() if business_update_match else ""

    return render_template('submission_output_editable.html', submission=session.get('submission', ''), username=current_user.username, input=input_section, output=output_section, business_update=business_update_section)

# Define the route for updating the submission
@login_required
@user_view.route('/update_submission', methods=['POST'])
def update_submission():
    text = session.get('submission', '')
    portfolio = session.get('portfolio', '')
    service = session.get('service', '')
    input_data = request.form.get('input')
    output_data = request.form.get('output')
    business_update = request.form.get('bu')

    input_pattern = r'INPUT:(.*?)OUTPUT:'
    output_pattern = r'OUTPUT:(.*?)BUSINESS UPDATE:'
    business_update_pattern = r'BUSINESS UPDATE:(.*)'

    # Use re.DOTALL to match across multiple lines
    input_match = re.search(input_pattern, text, re.DOTALL)
    output_match = re.search(output_pattern, text, re.DOTALL)
    business_update_match = re.search(business_update_pattern, text, re.DOTALL)

    # Extract the matched content
    input_section = input_match.group(1).strip() if input_match else ""
    output_section = output_match.group(1).strip() if output_match else ""
    business_update_section = business_update_match.group(1).strip() if business_update_match else ""

    
    # Assuming the following form fields are present: 'input', 'output', 'bu', 'portfolio', 'service'

   
    date_str = session.get('date', '')
    date = datetime.strptime(date_str, '%Y-%m-%d') #refactoring data fromat as SQLite DateTime type only accepts Python datetime
    sub_project = session.get('sub_project', '')
    teammates = session.get('team', '')

    

    try:
        # Create a new BusinessUpdates instance
        update_entry = BusinessUpdates(
            user_id=current_user.user_id,
            date = date,
            portfolio=portfolio,
            service=service,
            subtopics=sub_project,
            teammates=teammates,
            input=input_section,
            output=output_section,
            update=business_update_section
        )

        # Add the instance to the session and commit the changes
        db.session.add(update_entry)
        db.session.commit()

        # Clear the session data
        session.pop('user_id', None)
        # Additional session pops if needed
        flash("Update successful",category='success')

        return redirect(url_for('auth.logout'))

    except SQLAlchemyError as e:
            # Handle exceptions (print, log, or handle appropriately)
            flash("Update failed",category='error')
            db.session.rollback()

            # You might want to add a flash message or redirect to an error page
            return redirect(url_for('auth.logout'))


