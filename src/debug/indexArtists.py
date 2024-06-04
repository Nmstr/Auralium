from PyQt6.QtCore import QThread

class IndexArtistsThread(QThread):
    def __init__(self, debugWindow=None, sqlHandler=None):
        self.debugWindow = debugWindow
        self.sqlHandler = sqlHandler
        super().__init__(debugWindow)
    
    def run(self) -> None:
        self.stopFlag = False
        newArtists = 0
        oldArtists = 0

        # Add all artists to the database
        allArtists = self.sqlHandler.artists.retrieveAllFromSongs()
        for artist in allArtists:
            if self.stopFlag: break # If the indexing thread is stopped, break the loop
            if not self.sqlHandler.artists.retrieveByName(artist):
                self.sqlHandler.artists.create(artist)
                newArtists += 1
            else:
                oldArtists += 1
            self.debugWindow.artistIndexLabel.setText(f'Total artists: {len(allArtists)}\nArtists left: {len(allArtists) - (newArtists + oldArtists)}\nNew artists: {newArtists}\nOld artists: {oldArtists}')
        
        self.debugWindow.artistIndexLabel.setText(f'Total artists: {len(allArtists)}\nNew artists: {newArtists}\nOld artists: {oldArtists}')
        
    def stop(self):
        self.stopFlag = True
        while self.isRunning():
            pass
