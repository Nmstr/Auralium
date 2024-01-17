from flask import Flask, render_template, request, send_file, session, redirect, url_for
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from psycopg2 import extras
import psycopg2
import smtplib
import argon2
import random
import string
import shutil
import json
import os
import re

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Dynamically load in applications
applications = []
for dir in os.listdir('applications'):
    if os.path.exists(os.path.join('applications', dir, 'manifest.json')):
        with open(os.path.join('applications', dir, 'manifest.json')) as f:
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

# Dynamically load in backend applications
backendApplications = []
for dir in os.listdir('backendApplications'):
    if os.path.exists(os.path.join('backendApplications', dir, 'manifest.json')):
        with open(os.path.join('backendApplications', dir, 'manifest.json')) as f:
            data = json.load(f)
        # Load the modules
        module = __import__(f'backendApplications.{dir}.routes', fromlist=[dir])
        blueprint = getattr(module, data["blueprint"])
        app.jinja_loader.searchpath.append(os.path.join('backendApplications', dir, 'templates'))
        app.register_blueprint(blueprint, url_prefix=f'/backendApplications/{data["application"]}')
        
        # Load in applications for sidebar
        backendApplications.append(data)

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
    profilePic = '/accounts/default/profile-picture.png' # Default pfp
    if 'loggedin' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE uid = %s', (session['uid'],))
        account = cursor.fetchone()
        conn.close()
        if account:
            profilePic = f'accounts/{session["id"]}-{session["username"]}/profile-picture.png'
    return dict(apps=applications, profilePic = profilePic)

@app.route('/pfp/')
def serveProfilePicture():
    if 'loggedin' in session:
        filepath = f'accounts/{session["id"]}-{session["username"]}/profile-picture.png'
        if os.path.exists(filepath):
            return send_file(filepath)
        else:
            shutil.copy('accounts/default/profile-picture.png', f'{filepath}')
            return send_file(filepath)
    else:
        filepath = 'accounts/default/profile-picture.png'
        return send_file(filepath)

@app.route('/')
def index():
    print(session)
    if 'loggedin' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

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
        print(account)

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
                session['uid'] = account['uid']
                session['id'] = account['user_id']
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
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        conn.close()

        if not os.path.exists(f'accounts/{account[0]}-{account[1]}'):
            os.makedirs(f'accounts/{account[0]}-{account[1]}')
            shutil.copy('accounts/default/profile-picture.png', f'accounts/{account[0]}-{account[1]}/profile-picture.png')
        else:
            if not os.path.exists(f'accounts/{account[0]}-{account[1]}/profile-picture.png'):
                shutil.copy('accounts/default/profile-picture.png', f'accounts/{account[0]}-{account[1]}/profile-picture.png')
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/logout/')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('uid', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

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
    app.run(host='127.0.0.1', port=5000, debug=True)