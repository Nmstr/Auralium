from . import playlists as _playlists
from . import database as _database
from . import artists as _artists
from . import songs as _songs

class SqlHandler:
    def __init__(self):
        self.playlists = _playlists
        self.database = _database
        self.artists = _artists
        self.songs = _songs
