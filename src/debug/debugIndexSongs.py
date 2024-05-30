import songDataHandler

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import QThread, pyqtSlot, pyqtSignal

from PyQt6 import uic

import datetime
import time
import os

def formatDate(dateString):
    """
    Converts a date string from one format to another.

    Args:
        dateString (str): The date string to be converted.

    Returns:
        str: The converted date string in the format 'YYYY/MM/DD'.
    """
    if not dateString:
        return None
    if '-' in dateString:
        # Date is in the format "2001-01-30"
        date = datetime.datetime.strptime(dateString, '%Y-%m-%d').date()
    else:
        # Date is in the format "20010130"
        date = datetime.datetime.strptime(dateString, '%Y%m%d').date()
    
    formattedDate = date.strftime('%Y/%m/%d')
    return formattedDate

class IndexSongsThread(QThread):
    updateToErrorsSignal = pyqtSignal(list)
    
    def __init__(self, parent=None, sqlHandler=None):
        self.sqlHandler = sqlHandler
        super().__init__(parent)
    
    def run(self):
        # Setup indexing
        musicDir = os.getenv('XDG_MUSIC_DIR', default=os.path.expanduser('~/Music') + '/auralium')
        songs = os.listdir(musicDir)
        numberOfSongs = len(songs)
        processedSongs = 0
        self.stopFlag = False
        self.submitFlag = False
        self.submitAllFlag = False
        self.errors = []

        # Index songs
        for song in songs:
            if self.stopFlag: break # If the indexing thread is stopped, break the loop
            fullFilePath = os.path.join(musicDir, song)
            self.parent().pathToFileLabel.setText(fullFilePath) # Update the displayed path to the file

            processedSongs += 1
            hash = self.sqlHandler.database.hashFile(fullFilePath)
            if not self.sqlHandler.songs.retrieveBySha256hash(hash):
                songData = songDataHandler.getTag(fullFilePath)
                songData = self.checkValidData(songData)

                if self.parent().metadataCheckBox.isChecked():
                    songDataHandler.modifyTag(
                        filePath=fullFilePath,
                        title=songData.title,
                        artist=songData.artist,
                        releaseDate=songData.year
                    ) # Modify the song's tag
                result = self.sqlHandler.songs.insertSongIntoDB(
                    title=songData.title,
                    filePath=fullFilePath,
                    artist=songData.artist,
                    source='local',
                    releaseDate=songData.year
                ) # Add the song to the database

                if result[0] == 'error':
                    self.errors.append([song, result[1]])

            self.parent().processedSongsLabel.setText(f'Processed {processedSongs}/{numberOfSongs} songs')

        self.updateToErrorsSignal.emit(self.errors)

    def checkValidData(self, songData):
        # Check if the song data is valid
        self.parent().titleInput.setText(songData.title or '')
        self.parent().artistInput.setText(songData.artist or '')
        self.parent().releaseDateInput.setText(formatDate(songData.year) or '')

        # If the song data is valid and submitAllFlag is True, return the song data
        if self.submitAllFlag:
            if all([songData.title, songData.artist, songData.year]):
                return songData

        # Wait for the user to submit
        while not self.submitFlag:
            time.sleep(0.1)
            continue
        self.submitFlag = False # Reset the submitFlag

        # Update the song data with the user input
        songData.title = self.parent().titleInput.text()
        if songData.title == '':
            songData.title = None
        songData.artist = self.parent().artistInput.text()
        if songData.artist == '':
            songData.artist = None
        songData.year = self.parent().releaseDateInput.text()
        if songData.year == '':
            songData.year = None

        # Return the updated song data, if the data is invalid an error will occur later and be shown to the user
        return songData

    def submit(self):
        self.submitFlag = True
    
    def submitAll(self):
        self.submitFlag = True
        self.submitAllFlag = True

    def stop(self):
        self.stopFlag = True
        while self.isRunning():
            pass

class DebugIndexSongsWindow(QWidget):
    def __init__(self, sqlHandler):
        self.sqlHandler = sqlHandler

        super().__init__()
        self.ui = uic.loadUi('debug/debugIndexSongs.ui', self)

        self.indexSongsThread = IndexSongsThread(self, sqlHandler)
        self.indexSongsThread.updateToErrorsSignal.connect(self.updateToErrors)
        self.startIndexing()

        self.ui.submitBtn.clicked.connect(lambda: self.indexSongsThread.submit())
        self.ui.submitAllBtn.clicked.connect(lambda: self.indexSongsThread.submitAll())

        self.show()

    @pyqtSlot(list)
    def updateToErrors(self, errors):
        # Create a new container frame and a new QVBoxLayout
        newContainer = QFrame()
        newLayout = QVBoxLayout(newContainer)

        # Add widgets to the new layout
        if errors:
            label = QLabel(f'Errors: {len(errors)}')
            newLayout.addWidget(label)
            for error in errors:
                label = QLabel(f'{error[0]}: {error[1]}')
                newLayout.addWidget(label)

        # Get the parent of the old container
        parentWidget = self.ui.contentFrame.parentWidget()

        # Find the index of the old container in the parent layout
        parentLayout = parentWidget.layout()
        for i in range(parentLayout.count()):
            layoutItem = parentLayout.itemAt(i)
            if layoutItem.widget() == self.ui.contentFrame:
                # Remove the old container
                oldContainer = layoutItem.widget()
                parentLayout.removeWidget(oldContainer)
                oldContainer.deleteLater()

                # Add the new container
                parentLayout.addWidget(newContainer)
                break

        # Set newContainer as the new content frame
        self.ui.contentFrame = newContainer

    @pyqtSlot()
    def startIndexing(self):
        if not self.indexSongsThread.isRunning():
            self.indexSongsThread.start()

    def closeEvent(self, event):
        self.indexSongsThread.stop()
