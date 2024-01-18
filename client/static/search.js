$(document).ready(function() {
    $('#search-input').on('input', function() {
        var query = $(this).val();
        if (query.length >= 1) {
            $.ajax({
                url: '/applications/search/searchResult/',
                data: {query: query},
                success: function(results) {
                    var resultsContainer = $('#search-results');
                    resultsContainer.empty();
                    results.forEach(function(result) {
                        resultsContainer.append('<p>' + result + '</p>');
                    });
                }
            });
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