from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import textdistance
import glob
import os

searchApp = Blueprint('searchApp', __name__, template_folder='templates')

@searchApp.route('/search/')
def search():
    if 'loggedin' in session:
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 30))  # Default limit is 100
        allSongsFull = glob.glob(os.path.join('static', 'music') + "/*.mp3")
        paginatedSongs = allSongsFull[offset:offset + limit]
        return render_template('search.html', allSongsFull=paginatedSongs, os=os)
    return redirect(url_for('login'))

@searchApp.route('/loadMoreSongs/')
def load_more_songs():
    if 'loggedin' in session:
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 30))  # Default limit is 100
        allSongsFull = glob.glob(os.path.join('static', 'music') + "/*.mp3")
        paginatedSongs = allSongsFull[offset:offset + limit]
        return render_template('songsPartial.html', songs=paginatedSongs, os=os)
    return '', 401  # Unauthorized access

@searchApp.route('/play/')
def play():
    if 'loggedin' in session:
        #song_name = request.args.get('song_name')
        #return render_template('play.html', song_name=song_name, os=os)
        return 'Hello World'
    return redirect(url_for('login'))

@searchApp.route('/getSongImage/')
def getSongImage():
    if 'loggedin' in session:
        songName = request.args.get('songName')
        
        # Get the cover
        try:
            audio = MP3(songName)
            if 'APIC:' in audio:
                cover = audio['APIC:'].data
                return cover
            else:
                id3 = ID3(songName)
                if id3 and id3.getall('APIC'):
                    cover = id3.getall('APIC')[0].data
                    return cover
        except:
            with open('static/noCover.png', 'rb') as file:
                return file.read()

        with open('static/defaultSongCover.jpg', 'rb') as file:
            return file.read()

    return redirect(url_for('login'))

@searchApp.route('/searchResult', methods=['GET'])
def searchResult():
    query = request.args.get('query')
    allSongsFull = glob.glob(os.path.join('static', 'music') + "/*.mp3")
    allSongs = [os.path.splitext(os.path.basename(file))[0] for file in allSongsFull]

    # Define the minimum match score and minimum number of results
    minScore = 0.75
    minResults = 3

    # Define a custom key function
    def matchScore(filename):
        return textdistance.jaro_winkler(query, filename)

    # Filter
    filteredSongs = [file for file in allSongs if matchScore(os.path.splitext(os.path.basename(file))[0]) >= minScore]

    # While the number of results is less than the minimum, lower the match score threshold
    numResults = len(filteredSongs)
    while numResults < minResults:
        minScore -= 0.05 
        filteredSongs = [file for file in allSongs if matchScore(file) >= minScore]
        numResults = len(filteredSongs)

    # Sort the files based on the match score
    sortedSongs = sorted(filteredSongs, key=matchScore, reverse=True)

    return jsonify(sortedSongs)