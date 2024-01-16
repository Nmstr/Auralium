from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from psycopg2 import extras
import psycopg2
import smtplib
import argon2
import random
import string
import json
import os
import re

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Dynamically load in applications
applications = []
for dir in os.listdir('applications'):
    if os.path.exists(os.path.join('applications', dir, 'register.json')):
        with open(os.path.join('applications', dir, 'register.json')) as f:
            data = json.load(f)
        # Load the modules
        module = __import__(f'applications.{dir}.routes', fromlist=[dir])
        blueprint = getattr(module, data["blueprint"])
        app.jinja_loader.searchpath.append(os.path.join('applications', dir, 'templates'))
        app.register_blueprint(blueprint, url_prefix=f'/applications/{data["application"]}')
        
        # Load in applications for sidebar
        applications.append(data)
# Sort applications
applications = sorted(applications, key=lambda x: x['priority'])


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='musicdb',
                            user = os.getenv('DB_USERNAME'),
                            password = os.getenv('DB_PASSWORD')
                            )
    return conn

@app.context_processor
def inject_var():
    return dict(apps=applications)

@app.route('/')
def index():
    # Render the template and pass the graph filename to it
    print(session)
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Initialize message variable
    msg = ''
    
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=extras.DictCursor)

        # Execute the SQL query to fetch account with given username
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))

        # Fetch one record and return the result
        account = cursor.fetchone()

        # If account exists in accounts table in our database
        if account:
            try:
                # Verify the password with the stored hash
                argon2.PasswordHasher().verify(account['password'], password)
            except argon2.exceptions.VerifyMismatchError:
                # If passwords do not match, return an error message
                msg = 'Incorrect username/password!'
                return render_template('login.html', msg=msg)

            # Check if the account is verified
            if account['verified'] == True:
                # If verified, log the user in and redirect to home page
                session['loggedin'] = True
                session['id'] = account['uid']
                session['username'] = account['username']
                return redirect(url_for('index'))
            else:
                # If not verified, return a message asking to verify the account
                msg = 'Please verify your account before logging in!'
        else:
            # If account does not exist, return an error message
            msg = 'Incorrect username/password!'
        
        # Close the database connection
        conn.close()

    # Render the login page with the message
    return render_template('login.html', msg=msg)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=extras.DictCursor)
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # Check for errors
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Generate UID
            uid = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(32))
            # Hash the password
            hash = argon2.PasswordHasher().hash(password)

            cursor.execute('INSERT INTO accounts (username, password, email, created_on, last_login, uid) VALUES (%s, %s, %s, %s, %s, %s)', (username, hash, email, datetime.now(), datetime.now(), uid))
            conn.commit()
            # Send verification email
            sendVerificationEmail(email, uid)
            
        msg = 'You have successfully registered! Please check your email to verify your account.'
        conn.close()
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

def sendVerificationEmail(email, uid):
    selfReference = os.getenv('SELF_REFERENCE')
    mail_content = '''Hello,
    Please click on the following link to verify your account:
    http://{}/verify/{}'''.format(selfReference, uid)

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = 'short.creator.noreply@gmail.com'
    message['To'] = email
    message['Subject'] = 'Account Verification'   
    message.attach(MIMEText(mail_content, 'plain'))

    #use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587)

    #enable security
    session.starttls()

    #login with mail_id and password
    session.login('short.creator.noreply@gmail.com', os.getenv('MAIL_PASSWORD'))

    text = message.as_string()
    session.sendmail('short.creator.noreply@gmail.com', email, text)
    session.quit()

@app.route('/verify/<uid>', methods=['GET'])
def verify(uid):
    # Connect to db
    conn = get_db_connection()
    # Create a cursor object
    cursor = conn.cursor(cursor_factory=extras.DictCursor)

    # Check if uid exists in the database
    cursor.execute('SELECT * FROM accounts WHERE uid = %s', (uid,))
    account = cursor.fetchone()

    if account:
        # If the account exists, remove the uid and set the account as verified
        cursor.execute('UPDATE accounts SET verified = TRUE WHERE username = %s', (account['username'],))
        conn.commit()
        msg = 'Your account has been verified! You can now log in.'
    else:
        # If the uid does not exist in the database
        msg = 'Invalid verification link or your account is already verified.'

    conn.close()

    return render_template('login.html', msg=msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)