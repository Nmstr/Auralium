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
    print(allSongs)

    # Define the minimum match score and minimum number of results
    minScore = 0.75
    minResults = 3

    # Define a custom key function
    def match_score(filename):
        return textdistance.jaro_winkler(query, filename)

    # Filter and sort the files based on the match score
    filteredSongs = [file for file in allSongs if match_score(os.path.splitext(os.path.basename(file))[0]) >= minScore]

    # Check the number of filtered files
    numResults = len(filteredSongs)

    # While the number of results is less than the minimum, lower the match score threshold
    while numResults < minResults:
        minScore -= 0.05  # Lower the match score threshold by 0.05
        filteredSongs = [file for file in allSongs if match_score(file) >= minScore]
        numResults = len(filteredSongs)  # Update the number of results
        print(f"Number of results: {numResults} {minScore}")  # Now prints the correct number of results

    # Sort the files based on the match score
    sortedFiles = sorted(filteredSongs, key=match_score, reverse=True)
    print(filteredSongs)
    print(sortedFiles)

    return jsonify(sortedFiles)