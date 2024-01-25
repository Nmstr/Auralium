from flask import Blueprint, request, render_template
import datetime
import json
import os

playlistsBackendApplication = Blueprint('playlistsBackendApplication', __name__, template_folder='templates')

@playlistsBackendApplication.route('/playlistView/')
def playlistView():
    playlistName = request.args.get('playlistName')
    if not os.path.exists('backendProcesses/playlists/playlists'):
        return "Error: No playlists found"
    
    if not os.path.exists(f'backendProcesses/playlists/playlists/{playlistName}.json'):
        return "Error: Playlist not found"

    # Load the playlist data
    with open(f'backendProcesses/playlists/playlists/{playlistName}.json') as f:
        playlistData = json.load(f)
        
    # Update the 'lastAccess' field
    playlistData['lastAccess'] = datetime.datetime.now().timestamp()
    with open(f'backendProcesses/playlists/playlists/{playlistName}.json', 'w') as f:
        json.dump(playlistData, f)

    return render_template('playlistView.html', playlistData=playlistData)

@playlistsBackendApplication.route('/editPlaylist/')
def editPlaylist():
    playlistName = request.args.get('playlistName')
    if not os.path.exists('backendProcesses/playlists/playlists'):
        return "Error: No playlists found"
    
    if not os.path.exists(f'backendProcesses/playlists/playlists/{playlistName}.json'):
        return "Error: Playlist not found"

    # Load the playlist data
    with open(f'backendProcesses/playlists/playlists/{playlistName}.json') as f:
        playlistData = json.load(f)

    return render_template('playlistEdit.html', playlistData=playlistData)