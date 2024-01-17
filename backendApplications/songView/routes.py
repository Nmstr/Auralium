from flask import Blueprint, render_template, session, redirect, url_for

songViewApp = Blueprint('songViewApp', __name__, template_folder='templates')

@songViewApp.route('/songView/')
def view():
    if 'loggedin' in session:
        #song_name = request.args.get('song_name')
        #return render_template('play.html', song_name=song_name, os=os)
        return 'Hello World'
    return redirect(url_for('login'))
