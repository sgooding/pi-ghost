import zmq
import pygame
import json

from audioplayer import audio_factory

class AudioPlayerServer:
    def __init__(self):
        self._player = None
        self._buffer = dict()
        self._selected_player = None

    def set_player(self, player:str):
        self._selected_player = player

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

            filename = cmd['filename']
            if filename not in self._buffer:
                self._buffer[filename] = audio_factory(self._selected_player)
            self._buffer[filename].play(filename)

if __name__ == '__main__':

    server = AudioPlayerServer()

    server.set_player('MockAudioPlayer')

    server.run()