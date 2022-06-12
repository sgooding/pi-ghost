import zmq
import pygame
import json

from audioplayer import audio_factory

class AudioPlayerServer:
    def __init__(self):
        self._player = None

    def set_player(self, player):
        self._player = player

    def connect(self):
        context = zmq.Context()
        self._socket = context.socket(zmq.REP)
        self._socket.bind("tcp://*:5555")

    def run(self):
        self.connect()

        print(f'Listening for messages.')
        while True:
            msg = self._socket.recv().decode('utf-8')
            self._socket.send(b"ack")

            cmd = json.loads(msg)
            print(f'Received: {cmd}')

            if ('audioplayer' in cmd
               and cmd['audioplayer'] != type(self._player) ):

                self.set_player(audio_factory(cmd['audioplayer']))
            self._player.play(cmd['filename'])

if __name__ == '__main__':

    server = AudioPlayerServer()

    from audioplayer import MockAudioPlayer
    server.set_player(MockAudioPlayer())

    server.run()