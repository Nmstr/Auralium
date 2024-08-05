from audioplayer import AudioPlayer
import time

# Usage
player = AudioPlayer("mysound.wav")
player.play()
print("Current volume:", player.volume)
player.volume = 0.05
print("Current volume:", player.volume)
time.sleep(5)
print("Current position:", player.position)
print("Current volume:", player.volume)
player.pause()
time.sleep(2)
print("Current position:", player.position)
player.volume = 0.025
print("Current volume:", player.volume)
player.play()
print("Current position:", player.position)
time.sleep(5)
player.volume = 0.05
player.position = 30
print("Current position:", player.position)
time.sleep(5)
print("Current position:", player.position)
player.stop()
