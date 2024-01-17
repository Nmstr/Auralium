// player.js

const { copyFileSync } = require("original-fs");

const audioPlayer = document.getElementById('audioPlayer');
const prevButton = document.getElementById('prev');
const nextButton = document.getElementById('next');

let allSongs = [];

fetch('/applications/search/listAllSongs/')
  .then(response => response.json())
  .then(data => {
    allSongs = data;
    // Start with the first track
    playTrack(currentTrackIndex);
  });
let currentTrackIndex = 0;

function playSong(songName) {
    const index = allSongs.indexOf(songName);
    if (index === -1) {
        console.log(allSongs)
        console.log('Song not found');
        console.log(songName);
        return; // Song not found
    }
    playTrack(index);
}

function playTrack(index) {
    if (index < 0 || index >= allSongs.length) {
        return; // Index out of range
    }
    currentTrackIndex = index;
    audioPlayer.src = allSongs[currentTrackIndex];
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
    playTrack((currentTrackIndex + 1) % allSongs.length);
}

// Start with the first track
//playTrack(currentTrackIndex);