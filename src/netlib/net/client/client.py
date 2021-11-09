from ..endpoint import Endpoint
from ..packet import Packet
from netlib.utils.events import ConditionalEvent, Event

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
            self._listen_loop.start()
            self.OnConnect.fire()

        except ConnectionRefusedError:
            raise ConnectionRefusedError("Connection refused")

    def _loop(self):
        # Ensures successfully connected
        self.send(Packet({
            "handshake": "hello"
        }, request_type="__handshake"), force=True)

        self.receive(force=True)
        self.connected = True

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

    def send(self, message, *, force=False):
        if self.connected or force:
            return super().send(self.socket, message)

        else:
            raise ConnectionError("No active connection to host")

    def receive(self, *, force=False):
        if self.connected or force:
            return super().receive(self.socket)

        else:
            raise ConnectionError("No active connection to host")
