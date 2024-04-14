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

def getImgData(file_path: str, resolution: list = [150, 150]) -> bytes:
    """
    Retrieves image data from the specified file path and returns it as bytes. Supports custom resolution.
    
    Parameters:
    - file_path: str, the path to the file
    - resolution: list, optional, default is [150, 150]. The resolution for the image
    
    Returns:
    - bytes, the image data
    """
    baseName = os.path.splitext(os.path.basename(file_path))[0]
    imgPath = f'covers/{baseName}-{resolution[0]}x{resolution[1]}.png'

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
    except Exception:
        defaultImgPath = 'covers/default.png'
        if not os.path.exists(defaultImgPath):
            with open(defaultImgPath, 'wb') as f:
                f.write(Image.open('covers/default.png').resize(resolution).tobytes())

        return open(defaultImgPath, 'rb').read()
