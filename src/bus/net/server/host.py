from ..net_object import NetObject
from .connection import Connection
from threading import Thread
from utils.events import Event


class Host(NetObject):
    def __init__(self, ip, port):
        super().__init__(ip, port)

        self._loop = Thread(target=self._loop, daemon=False)
        self.connections = {}
        self.running = False

        self.OnConnect = Event()
        self.OnDisconnect = Event()

    def run(self):
        self._loop.start()
        self.running = True

    def _loop(self):
        while self.running:
            sock, info = self.socket.accept()

            conn = Connection(sock)
            self.OnConnect.fire(conn)
