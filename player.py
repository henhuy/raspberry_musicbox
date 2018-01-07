import os
import time
import vlc
# import subprocess

path = os.path.dirname(__file__)
musicfile = os.path.join(path, 'siimon_mathewson_-_04_-_Round__Round.mp3')
p = vlc.MediaPlayer(musicfile)
p.play()
time.sleep(1)
# p.stop()
time.sleep(2)
