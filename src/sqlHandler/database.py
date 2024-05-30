import hashlib
import sqlite3
import os

def connectToDB() -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    """
    Connects to the database and returns a cursor and connection object.
    """
    dbPath = os.getenv('XDG_CONFIG_HOME', default=os.path.expanduser('~/.config')) + '/auralium/auralium.db'
    conn = sqlite3.connect(dbPath)
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
            releaseDate TEXT,
            deleted INTEGER DEFAULT 0
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

