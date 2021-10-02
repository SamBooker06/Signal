from ..net_object import NetObject
from .connection import Connection
from threading import Thread
from bus.utils.events import Event


class Host(NetObject):
    def __init__(self, ip, port):
        super().__init__(ip, port)

        self._loop = Thread(target=self._loop, daemon=False)
        self.connections = {}
        self.running = False

        self.OnConnect = Event()
        self.OnDisconnect = Event()

    def run(self, backlog=8):
        self.socket.bind((self.ip, self.port))
        self.socket.listen(backlog)
        self._loop.start()
        self.running = True

    def get_connections(self):
        return [conn for conn in self.connections.values()]

    def _loop(self):
        while self.running:
            sock, info = self.socket.accept()

            conn = Connection(sock)
            key = "{}:{}".format(*info)

            self.OnConnect.fire(conn)
            self.connections[key] = conn

            @conn.OnDisconnect
            def handle_disconnect():
                self.OnDisconnect.fire(conn)
                del self.connections[key]
