from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import textdistance
import glob
import os

searchApp = Blueprint('searchApp', __name__, template_folder='templates')

@searchApp.route('/search/')
def search():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 30))  # Default limit is 100
    allSongsFull = glob.glob(os.path.join('static', 'music') + "/*.mp3")
    paginatedSongs = allSongsFull[offset:offset + limit]
    return render_template('search.html', allSongsFull=paginatedSongs, os=os)

@searchApp.route('/loadMoreSongs/')
def loadMoreSongs():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 30))  # Default limit is 100
    allSongsFull = glob.glob(os.path.join('static', 'music') + "/*.mp3")
    paginatedSongs = allSongsFull[offset:offset + limit]
    return render_template('songsPartial.html', songs=paginatedSongs, os=os)

@searchApp.route('/getSongImage/')
def getSongImage():
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

@searchApp.route('/searchResult/', methods=['GET'])
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
    firstSong = f'static/music/{sortedSongs[0]}.mp3'
    relevantSongs = [f'static/music/{song}.mp3' for song in sortedSongs[1:5]]
    otherSongs = [f'static/music/{song}.mp3' for song in sortedSongs[5:]]

    return render_template('searchResult.html', sortedSongs=sortedSongs, firstSong=firstSong, relevantSongs=relevantSongs, otherSongs=otherSongs, os=os)

@searchApp.route('/listAllSongs/')
def listAllSongs():
    musicDir = 'static/music/'
    songs = [f"static/music/{filename}" for filename in os.listdir(musicDir) if filename.endswith('.mp3')]
    return jsonify(songs)