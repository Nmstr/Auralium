from whoosh.qparser import MultifieldParser, FuzzyTermPlugin, WildcardPlugin
from whoosh.index import create_in, open_dir
from whoosh.writing import AsyncWriter
from whoosh.fields import Schema, TEXT

import os

class SearchEngine():
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        cacheDir = os.getenv('XDG_CACHE_HOME', default=os.path.expanduser('~/.cache') + '/auralium')
        self.indexDir = cacheDir + '/searchIndex'

    def createIndex(self, *, force: bool = False):
        """
        Creates an index for the search engine.

        Parameters:
            force (bool, optional): If set to True, the index directory will be recreated even if it already exists. Defaults to False.

        Returns:
            None
        """
        if not os.path.exists(self.indexDir) or force:
            os.makedirs(self.indexDir, exist_ok=True)
            # Define the schema and create the index
            schema = Schema(id=TEXT(stored=True),
                            title=TEXT(stored=True),
                            artist=TEXT(stored=True),
                            itemType=TEXT(stored=True))
            create_in(self.indexDir, schema)

            self.addToIndex()

    def addToIndex(self):
        """
        Adds all songs and artists from the database to the search index.
        """
        index = open_dir(self.indexDir) # Open index

        allSongs = self.mainWindow.sqlHandler.songs.retrieveAll()
        allSongs = [song[:3] for song in allSongs]
        # Add songs to index
        with AsyncWriter(index) as writer:
            for songId, title, artist in allSongs:
                writer.add_document(id=str(songId), title=title, artist=artist, itemType="song")
        
        allArtists = self.mainWindow.sqlHandler.artists.retrieveAll()
        allArtists = [artist[:2] for artist in allArtists]
        # Add artists to index
        with AsyncWriter(index) as writer:
            for artist_id, artist in allArtists:
                writer.add_document(id=str(artist_id), artist=artist, itemType="artist")

    def search(self, queryStr: str, autoFuzzy: bool = True, limit: int = 20):
        """
        Searches the index for songs matching the given query string.

        Args:
            queryStr (str): The search query string.
            autoFuzzy (bool, optional): Whether to automatically add a fuzzy search operator (~) to the query string. Defaults to True.
            limit (int, optional): The maximum number of search results to return. Defaults to 20.

        Returns:
            list: A list of dictionaries representing the songs that match the search query. Each dictionary contains the song's ID, title, artist, and other metadata.
        """
        queryStr = queryStr.strip()
        if not queryStr.endswith("~") and autoFuzzy:
            queryStr += "~"

        index = open_dir(self.indexDir)
        with index.searcher() as searcher:
            parser = MultifieldParser(["title", "artist"], schema=index.schema)
            parser.add_plugin(FuzzyTermPlugin())
            parser.add_plugin(WildcardPlugin())

            query = parser.parse(queryStr)
            results = searcher.search(query, limit=limit)

            result = []
            for hit in results:
                if hit["itemType"] == "song":
                    result.append({'itemType': 'song', 'data': self.mainWindow.sqlHandler.songs.retrieveById(hit["id"])})
                elif hit["itemType"] == "artist":
                    result.append({'itemType': 'artist', 'data': self.mainWindow.sqlHandler.artists.retrieve(hit["id"])})

            return result