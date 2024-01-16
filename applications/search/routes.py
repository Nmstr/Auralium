from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
import glob
import os
import textdistance

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
    min_score = 0.75
    min_results = 3

    # Define a custom key function
    def match_score(filename):
        return textdistance.jaro_winkler(query, filename)

    # Filter and sort the files based on the match score
    filtered_files = [file for file in allSongs if match_score(os.path.splitext(os.path.basename(file))[0]) >= min_score]

    # Check the number of filtered files
    num_results = len(filtered_files)

    # While the number of results is less than the minimum, lower the match score threshold
    while num_results < min_results:
        min_score -= 0.05  # Lower the match score threshold by 0.05
        filtered_files = [file for file in allSongs if match_score(os.path.splitext(os.path.basename(file))[0]) >= min_score]
        num_results = len(filtered_files)

    # Sort the files based on the match score
    sorted_files = sorted(filtered_files, key=match_score, reverse=True)

    results = ['Result 1', 'Result 2', 'Result 3']
    return jsonify(sorted_files)