
from pygame import mixer
from glob import glob
import os
import time
import json

def check_valid_extension(filename):
    if filename is None:
        return False
    return os.path.splitext(filename)[-1] in ['.wav','.mp3','.mp4']


class MockChannel:
    def __init__(self, filename):
        self._filename = filename
    
    def play(self):
        print(f"Mock Play {self._filename}")

class MockAudioPlayer:
    def __init__(self):
        self.song = None
        self._filename = None

    def play(self, filename):
        self.load(filename)
        self.song.play()

    def stop(self):
        pass

    def load(self, filename):
        if not check_valid_extension(filename):
            print(f'Invalid file extension')
            return

        if self.song is not None:
            print(f'Using Cached Song.')
        if self._filename is not None:
            print(f'Using Cached Filename is: {self._filename}')
        if self.song is None or filename != self._filename:
            print(f'Loading {filename}.')
            self.song = MockChannel(filename)
            self._filename = filename
            print(f'Success')

class ClientAudioPlayer:
    def __init__(self):
        import zmq
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")
        self._filename = None
        
    def play(self, filename):
        print("Sending Filename to client")
        msg = json.dumps({'filename':filename})
        self.socket.send(msg.encode('utf-8'))
        ack_msg = self.socket.recv()
        print(f'Received: {ack_msg}')

    def stop(self):
        pass
    def load(self, filename):
        self._filename = filename

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


def audio_factory(name):
    if name == 'AudioPlayer':
        print("Loading AudioPlayer")
        return AudioPlayer()
    elif name == 'MockAudioPlayer':
        print("Loading MockPlayer")
        return MockAudioPlayer()
    elif name == 'ClientAudioPlayer':
        print("Loading Client Audio Player")
        return ClientAudioPlayer()
    else:
        print("Unknown Player")
        return None

if __name__ == '__main__':
    player = MockAudioPlayer()
    sound_filename = glob('./static/*.mp3')[0]
    player.play(sound_filename)

    for i in range(10):
        print(f'Killing in {10-i} seconds.')
        time.sleep(1)

    del player




