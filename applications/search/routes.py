from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
import textdistance
import glob
import os

searchApp = Blueprint('searchApp', __name__, template_folder='templates')

@searchApp.route('/search/')
def searchRoute():
    if 'loggedin' in session:
        return render_template('search.html')
    return redirect(url_for('login'))

@searchApp.route('/searchResult', methods=['GET'])
def search():
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