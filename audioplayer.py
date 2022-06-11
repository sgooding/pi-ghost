
from pygame import mixer
from glob import glob
import os
import time

def check_valid_extension(filename):
    if filename is None:
        return False
    return os.path.splitext(filename)[-1] in ['.wav','.mp3','.mp4']

class AudioPlayer:
    def __init__(self):
        mixer.init()
        self.song = None
        self._filename = None

    def play(self, filename):
        mixer.stop()
        self.load(filename)
        self.song.play()

    def stop(self):
        mixer.stop()

    def load(self,filename):
        if not check_valid_extension(filename):
            print(f'Invalid file extension')
            return

        if self.song is not None:
            print(f'Using Cached Song.')
        if self._filename is not None:
            print(f'Using Cached Filename is: {self._filename}')
        if self.song is None or filename != self._filename:
            print(f'Loading {filename}.')
            self.song = mixer.Sound(filename)
            self._filename = filename
            print(f'Success')



    def __del__(self):
        mixer.stop()

if __name__ == '__main__':
    player = AudioPlayer()
    song = glob('./static/*.mp3')[0]
    player.play(song)

    for i in range(10):
        print(f'Killing in {10-i} seconds.')
        time.sleep(1)

    del player




