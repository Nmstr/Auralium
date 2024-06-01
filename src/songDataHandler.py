from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QPixmap

from mutagen.id3 import ID3, TIT2, TPE1, TDRC
from mutagen.mp3 import MP3
from tinytag import TinyTag as tinyTag
from PIL import Image

import pickle
import io
import os

class SongDataHandler:
    def __init__(self, sqlHandler):
        self.sqlHandler = sqlHandler

    def getTag(self, filePath: str) -> tinyTag:
        """
        A function to get the tag of the specified file path.
        
        Parameters:
        - filePath: str, the path to the file
        
        Returns:
        - tinyTag, the tag of the file
        """
        tag = tinyTag.get(filePath, image=True)
        return tag

    def modifyTag(self, filePath: str, title: str, artist: str, releaseDate: str) -> None:
        """
        A function to modify the tag of the specified file path.
        
        Parameters:
        - filePath: str, the path to the file
        - title: (optional) str, the new title
        - artist: (optional) str, the new artist
        - releaseDate: (optional) str, the new release date
        """
        audio = MP3(filePath, ID3=ID3) # Load the MP3 file

        if title:
            audio.tags.add(TIT2(encoding=3, text=title))
        if artist:
            audio.tags.add(TPE1(encoding=3, text=artist))
        if releaseDate:
            audio.tags.add(TDRC(encoding=3, text=releaseDate))

        audio.save() # Save the MP3 file

    def getImgData(self, filePath: str, *, resolution: tuple = (150, 150)) -> bytes:
        """
        Retrieves image data from the specified file path and returns it as bytes. Supports custom resolution.
        
        Parameters:
        - filePath: str, the path to the file
        - resolution: tuple, optional, default is (150, 150). The resolution for the image
        
        Returns:
        - bytes, the image data
        """

        # Create the cache directory if it doesn't exist
        cacheDir = os.getenv('XDG_CACHE_HOME', default=os.path.expanduser('~/.cache') + '/auralium/coverCache/')
        cachePath = cacheDir + os.path.basename(filePath) + str(resolution) + '.cache'
        if not os.path.exists(cacheDir):
            os.makedirs(cacheDir)

        # Check if the image data is cached
        if os.path.exists(cachePath):
            with open(cachePath, 'rb') as f:
                imgData = pickle.load(f)
        else:
            # Load the image
            tag = tinyTag.get(filePath, image=True)
            imgData = tag.get_image()

            # Resize and save the image to a buffer in PNG format
            img = Image.open(io.BytesIO(imgData)).resize(resolution).convert('RGB')
            with io.BytesIO() as buffered:
                img.save(buffered, format='PNG')
                imgData = buffered.getvalue()

            # Cache the image data
            with open(cachePath, 'wb') as f:
                pickle.dump(imgData, f)
        
        return imgData

    def setSongImage(self, songTitle: str, graphicsView: QGraphicsScene, resolution: list = [150, 150]) -> None:
        """
        A function that sets the image of a song in a graphics view.

        Parameters:
        - songTitle: str, the title of the song to set the image for
        - graphicsView: the graphics view where the image will be set
        - resolution: list, the resolution of the image
        
        Returns:
        - None
        """
        graphicsScene = QGraphicsScene()
        pixmap = QPixmap()
        songData = self.sqlHandler.songs.retrieveByTitle(songTitle)
        if songData:
            if songData[3]:
                pixmap.loadFromData(self.getImgData(self.sqlHandler.songs.retrieveByTitle(songTitle)[3], resolution=resolution))
        graphicsScene.addPixmap(pixmap)
        graphicsView.setScene(graphicsScene)