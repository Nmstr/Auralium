from .database import connectToDB
import json

def create(
        name: str,
        creator: str = None,
        description: str = None,
        imagePath: str = None
        ) -> int:
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

    return cursor.lastrowid

def delete(playlistId: int) -> None:
    """
    A function to delete a playlist from the database.

    Parameters:
    - playlistId: int, required, the id of the playlist

    Returns:
    - None
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute("DELETE FROM playlists WHERE id = ?", (playlistId,))
        conn.commit()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()

def retrieve(playlistId: int) -> list:
    """
    A function to retrieve a playlist from the database.

    Parameters:
    - playlistId: int, required, the id of the playlist

    Returns:
    - list: The playlist retrieved
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute("SELECT * FROM playlists WHERE id = ?", (playlistId,))
        playlist = cursor.fetchone()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()
    return playlist

def retrieveAll() -> list:
    """
    Retrieve all playlists from the database
    """
    try:
        cursor, conn = connectToDB()
        cursor.execute('SELECT * FROM playlists')
        allPlaylists = cursor.fetchall()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()
    return allPlaylists

def addSong(playlistId: int, songId: int, songPosition: int) -> None:
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
        songsInPlaylist = []
        if playlistData[5] is not None:
            songsInPlaylist = json.loads(playlistData[5])
        songsInPlaylist.insert(songPosition, str(songId))
        cursor.execute("UPDATE playlists SET songs = ? WHERE id = ?", (json.dumps(songsInPlaylist), playlistId))

        conn.commit()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()

def removeSong(playlistId: int, songPosition: int) -> None:
    """
    A function to remove a song from a playlist in the database.

    Parameters:
    - playlistId: int, required, the id of the playlist
    - songPosition: int, required, the position of the song in the playlist

    Returns:
    - None
    """
    try:
        cursor, conn = connectToDB()
        songsInPlaylist = json.loads(cursor.execute("SELECT songs FROM playlists WHERE id = ?", (playlistId,)).fetchone()[0])
        songsInPlaylist.pop(songPosition)
        cursor.execute("UPDATE playlists SET songs = ? WHERE id = ?", (json.dumps(songsInPlaylist), playlistId))
        conn.commit()
    except Exception:
        raise
    finally:
        cursor.close()
        conn.close()

def moveSong(playlistId: int, songPosition: int, destinationPosition: int) -> None:
    """
    A function to move a song in a playlist in the database.

    Parameters:
    - playlistId: int, required, the id of the playlist
    - songPosition: int, required, the position of the song in the playlist
    - destinationPosition: int, required, the destination position of the song in the playlist

    Returns:
    - None
    """
    try:
        cursor, conn = connectToDB()
        songsInPlaylist = json.loads(cursor.execute("SELECT songs FROM playlists WHERE id = ?", (playlistId,)).fetchone()[0])
        song = songsInPlaylist.pop(songPosition)
        songsInPlaylist.insert(destinationPosition, song)
        cursor.execute("UPDATE playlists SET songs = ? WHERE id = ?", (json.dumps(songsInPlaylist), playlistId))
        conn.commit()
    except Exception:
        raise
    finally:
        cursor.close()
