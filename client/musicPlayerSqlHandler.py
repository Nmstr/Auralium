import hashlib
import sqlite3
import json
import os

def connectToDB():
    """
    Connects to the database and returns a cursor and connection object.
    """
    conn = sqlite3.connect('musicPlayer.db')
    cursor = conn.cursor()
    return cursor, conn

def hashFile(filePath: str) -> str:
    """
    A function to hash a file using SHA-256.

    Parameters:
    - filePath: str, the path to the file to be hashed

    Returns:
    - str, the SHA-256 hash of the file
    """
    sha256 = hashlib.sha256()
    with open(filePath, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def createDB() -> None:
    """
    Connects to the database, creates tables 'songs', 'playlistSongs', and 'playlists' if not exists with specific fields,
    and commits the changes. Closes the connection at the end.
    """
    try:
        # Connect to db
        cursor, conn = connectToDB()

        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            artist TEXT,
            filePath TEXT NOT NULL UNIQUE,
            sha256hash TEXT,
            source TEXT,
            releaseDate TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            creator TEXT,
            description TEXT,
            imagePath TEXT,
            songs TEXT
        )
        ''')

        conn.commit()
    except Exception:
        raise
    finally:
        # Close connection
        cursor.close()
        conn.close()

def createPlaylist(name: str,
                   creator: str = None,
                   description: str = None,
                   imagePath: str = None
                   ) -> None:
    """
    A function to create a playlist in the database.

    Parameters:
    - name: str, required, the name of the playlist
    - creator: str, optional, the creator of the playlist
    - description: str, optional, the description of the playlist
    - imagePath: str, optional, the image path of the playlist

    Returns:
    - None
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute("""INSERT INTO playlists (name, creator, description, imagePath)
                       VALUES (?, ?, ?, ?)
                       """, (name, creator, description, imagePath)) 
        conn.commit()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()

def addSongToPlaylist(playlistId: int, songId: int, songPosition: int) -> None:
    """
    A function to add a song to a playlist in the database.

    Parameters:
    - playlistId: int, required, the id of the playlist
    - songId: int, required, the id of the song
    - songPosition: int, required, the position of the song in the playlist

    Returns:
    - None
    """
    try:
        # Check if playlist exists
        cursor, conn = connectToDB()
        cursor.execute("SELECT * FROM playlists WHERE id = ?", (playlistId,))
        playlistData = cursor.fetchone()
        if playlistData == None:
            print("Playlist with id {} does not exist.".format(playlistId))
            return

        # Check if song exists
        cursor.execute("SELECT * FROM songs WHERE id = ?", (songId,))
        songData = cursor.fetchone()
        if songData == None:
            print("Song with id {} does not exist.".format(songId))
            return
        

        # Insert the song
        songsInPlaylist = json.loads(playlistData[5])
        if songsInPlaylist == None:
            songsInPlaylist = []
        songsInPlaylist.insert(songPosition, str(songId))
        cursor.execute("UPDATE playlists SET songs = ? WHERE id = ?", (json.dumps(songsInPlaylist), playlistId))

        conn.commit()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()

def insertSong(title: str, 
               filePath: str,
               artist: str = None,
               source: str = None,
               releaseDate: str = None
               ) -> None:
    """
    A function to insert a song into the database.
    
    Parameters:
    - title: str, required, the title of the song
    - filePath: str, required, the file path of the song
    - artist: str, optional, the artist of the song
    - source: str, optional, the source of the song
    - releaseDate: str, optional, the release date of the song (YYYY-MM-DD)
    
    Returns:
    - None if successful
    - Error message if file type is invalid or file not found
    """
    
    # Early returns
    if not title:
        return 'Error: Title is required'
    if not filePath:
        return 'Error: File path is required'
    if not filePath.endswith('.mp3') or filePath.endswith('.wav') or filePath.endswith('.ogg'):
        return 'Error: Invalid file type (must be .mp3, .wav or .ogg)'
    if not os.path.exists(filePath):
        return 'Error: File not found'
    
    # Hash the file
    sha256hash = hashFile(filePath)

    # Connect to db
    cursor, conn = connectToDB()

    # Insert a new song
    try:
        cursor.execute('''
        INSERT INTO Songs (title, artist, filePath, sha256hash, source, releaseDate)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, artist, filePath, sha256hash, source, releaseDate))
    except sqlite3.IntegrityError as e:
        return f'Intergrity Error: {e}'

    # Save (commit) the changes
    conn.commit()

    # Query the database
    #cursor.execute('SELECT * FROM Songs')
    #print(cursor.fetchall())

    # Close the connection when done
    cursor.close()
    conn.close()

def retrieveAllSongs() -> list:
    """
    Retrieve all songs from the database
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute('SELECT * FROM Songs')
        allSongs = cursor.fetchall()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()
    return allSongs

def retrieveAllSongTitles() -> list:
    """
    Retrieve all songs from the database
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute('SELECT title FROM Songs')
        allSongTitles = cursor.fetchall()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()

    return [item[0] for item in allSongTitles]

def retrieveSongByTitle(title: str) -> list:
    """
    Retrieve a song from the database based on the provided title.

    Parameters:
    - title: str, the title of the song to retrieve

    Returns:
    - list: The song retrieved based on the title
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute('SELECT * FROM Songs WHERE title = ?', (title,))
        song = cursor.fetchone()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()
    return song

def retrieveSongByFilePath(filePath: str) -> list:
    try:
        cursor, conn = connectToDB()
        cursor.execute('SELECT * FROM Songs WHERE filePath = ?', (filePath,))
        song = cursor.fetchone()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()
    return song

def retrieveSongBySha256hash(sha256hash: str) -> list:
    try:
        cursor, conn = connectToDB()
        cursor.execute('SELECT * FROM Songs WHERE sha256hash = ?', (sha256hash,))
        song = cursor.fetchone()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()
    return song

def retrieveRandomSong() -> list:
    """
    Retrieve a random song from the database.
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute('SELECT * FROM Songs ORDER BY RANDOM() LIMIT 1')
        song = cursor.fetchone()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()
    return song
