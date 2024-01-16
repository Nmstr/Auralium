from flask import Blueprint, render_template

homeApp = Blueprint('homeApp', __name__, template_folder='templates')

@homeApp.route('/home/')
def homeRoute():
    return render_template('home.html')