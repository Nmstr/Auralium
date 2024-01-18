from flask import Blueprint, render_template, session, redirect, url_for

homeApp = Blueprint('homeApp', __name__, template_folder='templates')

@homeApp.route('/home/')
def homeRoute():
    return render_template('home.html')