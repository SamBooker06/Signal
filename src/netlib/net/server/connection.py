from threading import Thread
from netlib.net.packet import Packet
from netlib.utils.events import Event, ConditionalEvent
from ..endpoint import Endpoint
from uuid import uuid4


class Connection(Endpoint):
    def __init__(self, socket):
        ip, port = socket.getsockname()

        self._running = False
        self._message_loop = Thread(target=self._loop, daemon=False)

        self.OnMessage = Event()
        self.OnMessageOfType = ConditionalEvent(
            lambda packet: packet.headers["Request-Type"])
        self.OnDisconnect = Event()
        self.UUID = uuid4().hex

        super().__init__(ip, port)

        self.socket = socket
        self._message_loop.start()

    def send(self, message: Packet) -> None:
        """Send a packet to the connected client

        Args:
            message (Packet): The packet to send
        """

        return super().send(self.socket, message)

    def receive(self):
        """Do not use. Internal use only
        """
        return super().receive(self.socket)

    def _loop(self):
        handshake = self.receive()
        self.send(Packet({
            "handshake": "world"
        }, request_type="__handshake"))

        while self._running:
            try:
                msg = self.receive()
                packet = Packet.decode(msg)
                self.OnMessage.fire(packet)
                self.OnMessageOfType.fire(packet)

            except (ConnectionAbortedError, ConnectionResetError):
                self.OnDisconnect.fire()
                self._running = False
