const audioPlayer = document.getElementById('audioPlayer');
const songQueue = []; // Initialize an empty array for the song queue
let currentSongIndex = 0; // Keep track of the current song

// Function to set the source of the audio player and play it
function setSong(source) {
    audioPlayer.src = source;
    audioPlayer.play();
}

// Function to queue a new song
function queueSong(source) {
    songQueue.push(source);
}

// Function to play the next song in the queue
function skipForward() {
    if (currentSongIndex < songQueue.length - 1) {
        currentSongIndex++;
        setSong(songQueue[currentSongIndex]);
    } else {
        // Handle the end of the queue, perhaps by looping or stopping
        console.log("Reached the end of the queue.");
    }
}

// Function to go back to the previous song
function skipBackward() {
    if (currentSongIndex > 0) {
        currentSongIndex--;
        setSong(songQueue[currentSongIndex]);
    } else {
        // Handle if there is no previous song
        console.log("This is the first song in the queue.");
    }
}
