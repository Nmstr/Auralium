function submitEditPlaylistForm() {
    // Get the updated values
    if (arguments[0] == 'title') {
        var newValue = document.getElementById('newPlaylistTitleInput').value;
    } else if (arguments[0] == 'description') {
        var newValue = document.getElementById('newPlaylistDescriptionInput').value;
    } else if (arguments[0] == 'image') {
        var newValue = document.getElementById('newPlaylistImageInput').value;
    }
    var playlistName = "{{ playlistData['name'] }}";

    // Send the request
    fetch(`/backendProcesses/playlists/editPlaylistOperation/?playlistName=${playlistName}&updatedField=${arguments[0]}&newValue=${newValue}`)
        .then(response => {
            reloadPlaylists();
       });
}