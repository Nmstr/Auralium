from mutagen.id3 import ID3, TIT2, TPE1, TDRC
from mutagen.mp3 import MP3
from tinytag import TinyTag as tinyTag
from PIL import Image

import os


def getTag(filePath: str) -> tinyTag:
    """
    A function to get the tag of the specified file path.
    
    Parameters:
    - filePath: str, the path to the file
    
    Returns:
    - tinyTag, the tag of the file
    """
    tag = tinyTag.get(filePath, image=True)
    return tag

def modifyTag(filePath: str, title: str, artist: str, releaseDate: str) -> None:
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

def getImgData(file_path: str, resolution: list = [150, 150]) -> bytes:
    """
    Retrieves image data from the specified file path and returns it as bytes. Supports custom resolution.
    
    Parameters:
    - file_path: str, the path to the file
    - resolution: list, optional, default is [150, 150]. The resolution for the image
    
    Returns:
    - bytes, the image data
    """
    cacheDir = os.getenv('XDG_CACHE_HOME', default=os.path.expanduser('~/.cache') + '/auralium')
    baseName = os.path.splitext(os.path.basename(file_path))[0]
    imgPath = f'{cacheDir}/covers/{baseName}-{resolution[0]}x{resolution[1]}.png'
    if not os.path.exists(os.path.dirname(imgPath)):
        os.makedirs(os.path.dirname(imgPath))

    if os.path.exists(imgPath):
        with open(imgPath, 'rb') as f:
            return f.read()

    try:
        tag = tinyTag.get(file_path, image=True)
        imgData = tag.get_image()

        with open(imgPath, 'wb') as f:
            f.write(imgData)

        img = Image.open(imgPath)
        img = img.resize(resolution)
        img.save(imgPath)

        with open(imgPath, 'rb') as f:
            return f.read()
    except Exception as e:
        defaultImgPath = 'assets/defaultCover.png'
        if not os.path.exists(defaultImgPath):
            with open(defaultImgPath, 'wb') as f:
                f.write(Image.open('assets/defaultCover.png').resize(resolution).tobytes())

        return open(defaultImgPath, 'rb').read()
