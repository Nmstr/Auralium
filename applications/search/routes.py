from flask import Blueprint, render_template, session, redirect, url_for

searchApp = Blueprint('searchApp', __name__, template_folder='templates')

@searchApp.route('/search/')
def searchRoute():
    if 'loggedin' in session:
        return render_template('search.html')
    return redirect(url_for('login'))