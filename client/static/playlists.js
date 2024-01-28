function submitEditPlaylistForm() {
    // Get the updated values
    if (arguments[0] == 'title') {
        var newValue = document.getElementById('newPlaylistTitleInput').value;
    } else if (arguments[0] == 'description') {
        var newValue = document.getElementById('newPlaylistDescriptionInput').value;
    } else if (arguments[0] == 'image') {
        var newValue = document.getElementById('newPlaylistImageInput').value;
    }

    // Send the request
    fetch(`/backendProcesses/playlists/editPlaylistOperation/?playlistName=${playlistName}&updatedField=${arguments[0]}&newValue=${newValue}`)
        .then(response => {
            reloadPlaylists();
       });
}

function createPlaylist() {
    fetch('/backendProcesses/playlists/createPlaylist/')
        .then(response => {
            reloadPlaylists();
        });
}