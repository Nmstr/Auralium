from flask import Blueprint, render_template, request
import datetime
import json
import os

backendPlaylists = Blueprint('backendPlaylists', __name__, template_folder='templates')

def repairPlaylistNames():
    playlistDir = 'backendProcesses/playlists/playlists'
    for playlist in os.listdir(playlistDir):
        with open(os.path.join(playlistDir, playlist), 'r') as file:
            playlistData = json.load(file)
        
        newFilename = f"{playlistData['name']}.json"
        currentPath = os.path.join(playlistDir, playlist)
        newPath = os.path.join(playlistDir, newFilename)

        if currentPath != newPath:  # Check if renaming is necessary
            os.rename(currentPath, newPath)

@backendPlaylists.route('/retrieveAll/')
def retrieveAll():
    if not os.path.exists('backendProcesses/playlists/playlists'):
        return []
    
    repairPlaylistNames()
    
    allPlaylists = os.listdir('backendProcesses/playlists/playlists')

    # Load the playlist data
    allPlaylistsData = []
    for playlistFile in allPlaylists:
        with open(f'backendProcesses/playlists/playlists/{playlistFile}') as f:
            playlistData = json.load(f)
            allPlaylistsData.append(playlistData)

    # Sort the playlist data based on the 'lastAccess' field
    allPlaylists = sorted(allPlaylistsData, key=lambda x: x['lastAccess'], reverse=True)
    return render_template('allPlaylistsOnSide.html', allPlaylists=allPlaylists)

@backendPlaylists.route('/createPlaylist/')
def createPlaylist():
    if not os.path.exists('backendProcesses/playlists/playlists'):
        os.makedirs('backendProcesses/playlists/playlists')
    i = 0
    while os.path.exists(f'backendProcesses/playlists/playlists/Playlist {i}.json'):
        i += 1

    playlistData = {
        'name': f'Playlist {i}',
        'description': None,
        'image': None,
        'lastAccess':  datetime.datetime.now().timestamp(),
        'songs': [],
        'playlistManifestVersion': '1.0.0'
    }

    with open(f'backendProcesses/playlists/playlists/{playlistData["name"]}.json', 'w') as f:
        json.dump(playlistData, f, indent=4)

    return "Done"

@backendPlaylists.route('/editPlaylistOperation/')
def editPlaylistOperation():
    playlistName = request.args.get('playlistName')
    updatedField = request.args.get('updatedField')
    newValue = request.args.get('newValue')
    if not os.path.exists('backendProcesses/playlists/playlists'):
        return "Error: No playlists found"
    
    if not os.path.exists(f'backendProcesses/playlists/playlists/{playlistName}.json'):
        return f"Error: Playlist not found: {playlistName}"

    with open('backendProcesses/playlists/playlists/' + playlistName + '.json', 'r') as file:
        playlistData = json.load(file)
    
    if updatedField == 'title':
        playlistData['name'] = newValue
    elif updatedField == 'description':
        playlistData['description'] = newValue
    elif updatedField == 'image':
        playlistData['image'] = newValue

    with open('backendProcesses/playlists/playlists/' + playlistName + '.json', 'w') as file:
        json.dump(playlistData, file, indent=4)

    return f"Done: {newValue} in {updatedField} of {playlistName}"