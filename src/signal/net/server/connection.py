from threading import Thread
from bus.net.packet import Packet
from bus.utils.events import Event
from ..endpoint import Endpoint


class Connection(Endpoint):
    def __init__(self, socket):
        ip, port = socket.getsockname()

        self._running = False
        self._message_loop = Thread(target=self._loop, daemon=False)

        self.OnMessage = Event()
        self.OnDisconnect = Event()

        super().__init__(ip, port)

        self.socket = socket
        self._message_loop.start()

    def send(self, message):
        return super().send(self.socket, message)

    def receive(self):
        return super().receive(self.socket)

    def _loop(self):
        self._running = True

        while self._running:
            try:
                msg = self.receive()
                packet = Packet.decode(msg)
                self.OnMessage.fire(packet)

            except (ConnectionAbortedError, ConnectionResetError):
                self.OnDisconnect.fire()
                self._running = False
