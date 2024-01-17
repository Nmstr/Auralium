// player.js

const audioPlayer = document.getElementById('audioPlayer');
const prevButton = document.getElementById('prev');
const nextButton = document.getElementById('next');

let playlist = [
    '/static/music/cro.mp3',
    '/static/music/Tream, treamiboii - SUMMER OF MY LIFE.mp3',
    // Add as many songs as you like
];
let currentTrackIndex = 0;

function playTrack(index) {
    if (index < 0 || index >= playlist.length) {
        return; // Index out of range
    }
    currentTrackIndex = index;
    audioPlayer.src = playlist[currentTrackIndex];
    audioPlayer.play();
}

audioPlayer.addEventListener('ended', function() {
    // Play next track when current one ends
    nextTrack();
});

prevButton.addEventListener('click', function() {
    // Go to previous track
    playTrack(currentTrackIndex - 1);
});

nextButton.addEventListener('click', function() {
    // Go to next track
    nextTrack();
});

function nextTrack() {
    // Play next track or loop back to start
    playTrack((currentTrackIndex + 1) % playlist.length);
}

// Start with the first track
playTrack(currentTrackIndex);