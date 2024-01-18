$(document).ready(function() {
    var lastRequestTime = 0;
    var throttleDelay = 1000; // 1 second throttle delay

    $('#search-input').on('input', function() {
        var query = $(this).val();
        var currentTime = new Date().getTime();

        if (query.length >= 1) {
            // Check if enough time has passed since the last request
            if (currentTime - lastRequestTime >= throttleDelay) {
                lastRequestTime = currentTime; // Update the last request time
                
                // Replace $.ajax with fetch API call
                fetch(`/applications/search/searchResult/?query=${encodeURIComponent(query)}`)
                    .then(response => response.text())
                    .then(html => {
                        // Insert the returned HTML into the results container
                        var resultsContainer = $('#search-results');
                        resultsContainer.empty();
                        resultsContainer.append(html);
                    })
                    .catch(error => console.error('Error:', error));
            }
        } else {
            $('#search-results').empty();
        }
    });
});

var offset = 0;
var limit = 30;

function loadMoreSongs() {
    offset += limit;
    fetch(`/applications/search/loadMoreSongs/?offset=${offset}&limit=${limit}`)
        .then(response => response.text())
        .then(html => {
            document.querySelector('.extend-more-songs').insertAdjacentHTML('beforeend', html);
            // If no more songs, you can hide the Load More button
            // This assumes the response will be empty if there are no more songs
            if (!html.trim()) {
                document.getElementById('load-more').style.display = 'none';
            }
        })
        .catch(error => console.error('Error loading more songs:', error));
}