from flask import Blueprint, render_template, session, redirect, url_for, request
from urllib.parse import quote
import eyed3
import os

songViewApp = Blueprint('songViewApp', __name__, template_folder='templates')

@songViewApp.route('/songView/')
def view():
    if 'loggedin' in session:
        songName = request.args.get('songName')
        # Get the metadata
        audio_file = eyed3.load(songName)
        songInfo = {}
        if audio_file.tag is not None:
            songInfo['title'] = audio_file.tag.title
            songInfo['artist'] = audio_file.tag.artist
            songInfo['album'] = audio_file.tag.album
            songInfo['genre'] = audio_file.tag.genre
            songInfo['duration_secs'] = audio_file.info.time_secs
            songInfo['duration_long'] = f'{int(audio_file.info.time_secs // 60)}:{str(int(audio_file.info.time_secs % 60)).zfill(2)}'

        if songInfo['title'] is None:
            songInfo['title'] = 'Unknown'
        if songInfo['artist'] is None:
            songInfo['artist'] = 'Unknown'
        if songInfo['album'] is None:
            songInfo['album'] = 'Unknown'
        if songInfo['genre'] is None:
            songInfo['genre'] = 'Unknown'
        if songInfo['duration_secs'] is None:
            songInfo['duration_secs'] = 'Unknown'
        if songInfo['duration_long'] is None:
            songInfo['duration_long'] = 'Unknown'

        return render_template('songView.html', songName=songName, songInfo=songInfo, os=os, quote=quote)
    return redirect(url_for('login'))
