from ..endpoint import Endpoint
from ..packet import Packet
from bus.utils.events import ConditionalEvent, Event

from threading import Thread


class Client(Endpoint):
    def __init__(self, ip, port):
        self.connected = False
        self._listen_loop = Thread(target=self._loop, daemon=False)

        self.OnMessage = Event()
        self.OnMessageOfType = ConditionalEvent(
            lambda packet: packet.headers["Request-Type"])
        self.OnConnect = Event()
        self.OnDisconnect = Event()

        super().__init__(ip, port)

    def connect(self):
        try:
            self.socket.connect((self.ip, self.port))
            self.connected = True
            self._listen_loop.start()
            self.OnConnect.fire()

        except ConnectionRefusedError:
            raise ConnectionRefusedError("Connection refused")

    def _loop(self):
        while self.connected:
            try:
                msg = self.receive()
                decoded = Packet.decode(msg)

                self.OnMessage.fire(decoded)
                self.OnMessageOfType.fire(decoded)

            except (ConnectionAbortedError, ConnectionResetError):
                self.OnDisconnect.fire()

    def disconnect(self):
        self.socket.close()
        self.connected = False

    def send(self, message):
        if self.connected:
            return super().send(self.socket, message)

        else:
            raise ConnectionError("No active connection to host")

    def receive(self):
        if self.connected:
            return super().receive(self.socket)

        else:
            raise ConnectionError("No active connection to host")
