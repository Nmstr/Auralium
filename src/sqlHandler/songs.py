from .database import connectToDB, hashFile
import sqlite3
import os

def insertSongIntoDB(title: str, 
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
        return 'error', 'Error: Title is required'
    if not filePath:
        return 'error', 'Error: File path is required'
    if not filePath.endswith('.mp3') or filePath.endswith('.wav') or filePath.endswith('.ogg'):
        return 'error', 'Error: Invalid file type (must be .mp3, .wav or .ogg)'
    if not os.path.exists(filePath):
        return 'error', 'Error: File not found'
    if retrieveByPath(filePath):
        return 'error', 'Error: File path already found in database'
    
    sha256hash = hashFile(filePath) # Hash the file

    cursor, conn = connectToDB()

    # Insert a new song
    try:
        cursor.execute('''
        INSERT INTO Songs (title, artist, filePath, sha256hash, source, releaseDate)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, artist, filePath, sha256hash, source, releaseDate))
    except sqlite3.IntegrityError as e:
        return f'Intergrity Error: {e}'

    conn.commit()

    # Close the connection when done
    cursor.close()
    conn.close()

    return 'success', 'Song inserted successfully'

def markAsDeleted(id: int) -> None:
    """
    A function to mark a song as deleted in the database.

    Parameters:
    - id: int, required, the id of the song to mark as deleted

    Returns:
    - None
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute('UPDATE songs SET deleted = 1 WHERE id = ?', (id,))
        conn.commit()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()

def retrieveAll() -> list:
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

def retrieveByTitle(title: str) -> list:
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

def retrieveBySha256hash(sha256hash: str) -> list:
    """
    Retrieves a song from the database based on the provided SHA-256 hash.

    Parameters:
    - sha256hash: str, the SHA-256 hash of the song to retrieve

    Returns:
    - list: The song retrieved based on the SHA-256 hash
    """
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

def retrieveById(id: int) -> list:
    """
    Retrieve a song from the database based on the provided ID.

    Parameters:
    - id: int, the ID of the song to retrieve

    Returns:
    - list: The song retrieved based on the ID
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute('SELECT * FROM songs WHERE id = ?', (id,))
        song = cursor.fetchone()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()
    return song

def retrieveByPath(filePath: str) -> list:
    """
    Retrieve a song from the database based on the provided file path.

    Parameters:
    - filePath: str, the file path of the song to retrieve

    Returns:
    - list: The song retrieved based on the file path
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute('SELECT * FROM songs WHERE filePath = ?', (filePath,))
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
        cursor.execute('SELECT * FROM songs WHERE deleted = 0 ORDER BY RANDOM() LIMIT 1')
        song = cursor.fetchone()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()
    return song
