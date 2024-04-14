import hashlib
import sqlite3
import os

def connectToDB():
    """
    Connects to the database and returns a cursor and connection object.
    """
    conn = sqlite3.connect('musicPlayer.db')
    cursor = conn.cursor()
    return cursor, conn

def hashFile(filePath):
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
    Connects to the database, creates a table 'Songs' if not exists with specific fields,
    and commits the changes. Closes the connection at the end.
    """
    try:
        # Connect to db
        cursor, conn = connectToDB()

        # Create table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Songs (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            artist TEXT,
            album TEXT,
            filePath TEXT NOT NULL UNIQUE,
            sha256hash TEXT,
            source TEXT
        )
        ''')

        conn.commit()
    except Exception:
        raise
    finally:
        # Close connection
        cursor.close()
        conn.close()

def insertSong(title: str, 
               filePath: str,
               artist: str = None,
               album: str = None,
               source: str = None):
    """
    A function to insert a song into the database.
    
    Parameters:
    - title: str, required, the title of the song
    - filePath: str, required, the file path of the song
    - artist: str, optional, the artist of the song
    - album: str, optional, the album of the song
    - source: str, optional, the source of the song
    
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
        cursor.execute("""
        INSERT INTO Songs (title, artist, album, filePath, sha256hash, source)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (title, artist, album, filePath, sha256hash, source))
    except sqlite3.IntegrityError as e:
        return f'Intergrity Error: {e}'

    # Save (commit) the changes
    conn.commit()

    # Query the database
    cursor.execute('SELECT * FROM Songs')
    print(cursor.fetchall())

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
