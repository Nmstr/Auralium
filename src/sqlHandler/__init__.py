from . import playlists as _playlists
from . import database as _database
from . import songs as _songs

class SqlHandler:
    def __init__(self):
        self.songs = _songs
        self.playlists = _playlists
        self.database = _database

sqlHandler = SqlHandler()