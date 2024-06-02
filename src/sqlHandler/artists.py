from .database import connectToDB

def create(
        name: str,
        description: str = None
        ) -> None:
    """
    Create a new artist in the database.

    Parameters:
    - name: str, required, the name of the artist
    - description: str, optional, the description of the artist

    Returns:
    - None
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute("""INSERT INTO artists (name, description)
                       VALUES (?, ?)
                       """, (name, description)) 
        conn.commit()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()

def retrieve(artistId: int) -> list:
    """
    Retrieve an artist from the database.

    Parameters:
    - artistId: int, required, the id of the artist

    Returns:
    - list: The artist retrieved
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute("SELECT * FROM artists WHERE id = ?", (artistId,))
        artist = cursor.fetchone()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()
    return artist

def retrieveByName(name: str) -> list:
    """
    Retrieve an artist from the database.

    Parameters:
    - name: str, required, the name of the artist

    Returns:
    - list: The artist retrieved
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute("SELECT * FROM artists WHERE name = ?", (name,))
        artist = cursor.fetchone()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()
    return artist

def retrieveAll() -> list:
    """
    Retrieve all artists from the database

    Parameters:
    - None

    Returns:
    - list: The list of artists retrieved
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute('SELECT * FROM artists')
        allArtists = cursor.fetchall()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()
    return allArtists

def retrieveAllFromSongs() -> list:
    """
    Retrieve all artists from the database based on the songs table

    Parameters:
    - None

    Returns:
    - list: The list of artists retrieved
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute("SELECT artist FROM songs")
        allRows = cursor.fetchall()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()

    uniqueArtists = set()

    for row in allRows: # Iterate through the results, splitting the artist field and adding to the set
        artist = row[0].split('/')
        uniqueArtists.update(artist)

    distinctArtists = list(uniqueArtists)
    return distinctArtists
