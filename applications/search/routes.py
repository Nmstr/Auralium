from flask import Blueprint, render_template

searchApp = Blueprint('searchApp', __name__, template_folder='templates')

@searchApp.route('/search/')
def searchRoute():
    return render_template('search.html')