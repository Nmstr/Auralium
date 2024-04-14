import difflib
import sqlite3
import hashlib
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

def retrieveSimilarSongs(inputQuery: str) -> list:
    """
    Retrieve similar songs based on the inputQuery provided.
    Connects to the SQLite database, executes a query to select similar strings, calculates similarity,
    and prints the 50 most similar strings. Finally, closes the database connection.

    Parameters:
    - inputQuery: str, the input string to search for

    Returns:
    - None if successful
    """

    if not inputQuery.strip():
        # Return an empty list if the input query is empty or only contains whitespace
        return []
    
    similarSongs = []    
    try:
        # Connect to the SQLite database
        cursor, conn = connectToDB()
        
        # Query to select similar strings using case-insensitive LIKE
        query = """
        SELECT title
        FROM Songs
        WHERE title LIKE ?
        LIMIT 50;
        """
        
        # Use a case-insensitive pattern for matching
        pattern = f"%{inputQuery.lower()}%"
        
        # Execute the query with parameter substitution to prevent SQL injection
        cursor.execute(query, (pattern,))
        results = cursor.fetchall()
        
        # Calculate similarity and sort the results
        similarSongs = sorted(results, key=lambda x: difflib.SequenceMatcher(None, x[0].lower(), inputQuery.lower()).ratio(), reverse=True)

    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Close the cursor and connection safely if they were successfully created
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return similarSongs[:50]

#createDB()
#print(insertSong("Hier sind die Onkelz", "new/music/Böhse Onkelz - Hier sind die Onkelz.mp3", source="local"))
#print(insertSong("Ohrgasmus", "new/music/DJ Robin - Ohrgasmus.mp3", source="local"))
#print(insertSong("Major Fans", "new/music/Major Conspiracy - Major Fans.mp3", source="local"))
#print(insertSong("Numb - Aftershock Remix", "new/music/Harris & Ford, DJ Gollum - Numb - Aftershock Remix.mp3", source="local"))
#print(insertSong("Body Moving", "new/music/Eliza Rose, Calvin Harris - Body Moving.mp3", source="local"))
#for song in os.listdir("new/music"):
#    print(insertSong(song, f"new/music/{song}", source="local"))

#print(retrieveSimilarSongs("Böhse Onkelz - H"))

#print(insertSong("Song Title", "new/music/Böhse Onkelz - Hier sind die Onkelz.mp3", source="local"))
#print(insertSong("Song Title", "new/music/Böhse Onkelz - Hier sind die Onkelz.mp3", source="local"))
#print(insertSong("Song Title", "new/music/Böhse Onkelz - Hier sind die Onkelz.mp3", source="local"))
