from flask import Blueprint, render_template, session, redirect, url_for, request

songViewApp = Blueprint('songViewApp', __name__, template_folder='templates')

@songViewApp.route('/songView/')
def view():
    if 'loggedin' in session:
        songName = request.args.get('songName')
        return render_template('songView.html', songName=songName)
    return redirect(url_for('login'))
