from whoosh.qparser import MultifieldParser, FuzzyTermPlugin, WildcardPlugin
from whoosh.index import create_in, open_dir
from whoosh.writing import AsyncWriter
from whoosh.fields import Schema, TEXT

import sqlHandler

import os

class SearchEngine():
    def __init__(self, sqlHandler):
        self.sqlHandler = sqlHandler
        cacheDir = os.getenv('XDG_CACHE_HOME', default=os.path.expanduser('~/.cache') + '/auralium')
        self.indexDir = cacheDir + '/searchIndex'

    def createIndex(self):
        """
        Creates an index for the search engine.
        """
        if not os.path.exists(self.indexDir):
            os.mkdir(self.indexDir)

        # Define the schema and create the index
        schema = Schema(id=TEXT(stored=True), title=TEXT(stored=True), artist=TEXT(stored=True))
        create_in(self.indexDir, schema)

    def addToIndex(self):
        """
        Adds all songs from the database to the search index.
        """
        allSongs = sqlHandler.songs.retrieveAll()
        allSongs = [song[:3] for song in allSongs]
        index = open_dir(self.indexDir) # Open index

        # Add songs to index
        with AsyncWriter(index) as writer:
            for song_id, title, artist in allSongs:
                writer.add_document(id=str(song_id), title=title, artist=artist)

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
            
            return [self.sqlHandler.songs.retrieveById(hit["id"]) for hit in results]