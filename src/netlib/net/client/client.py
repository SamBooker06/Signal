from ..endpoint import Endpoint
from ..packet import Packet
from netlib.utils.events import ConditionalEvent, Event

from threading import Thread


class Client(Endpoint):
    """Client object used to connect to server.
    """

    def __init__(self, ip: str, port: int) -> None:
        """Client object used to connect to server.

        Args:
            ip (str): The ip of the server.
            port (int): The port to connect to on the server.
        """
        self.connected = False
        self._listen_loop = Thread(target=self._loop, daemon=False)

        self.OnSignal = Event()
        self.OnSignalOfType = ConditionalEvent(
            lambda packet: packet.headers["Request-Type"])
        self.OnConnect = Event()
        self.OnDisconnect = Event()

        super().__init__(ip, port)

    def connect(self) -> None:
        """Connects the client to the server.

        Raises:
            ConnectionRefusedError: Raised if the server refuses connection for any reason.
        """
        try:
            self.socket.connect((self.ip, self.port))
            self.connected = True

            # Ensures successfully connected
            self.send(Packet({
                "handshake": "hello"
            }, request_type="__handshake"))

            self.receive()

            self._listen_loop.start()
            self.OnConnect.fire()

        except ConnectionRefusedError:
            raise ConnectionRefusedError("Connection refused")

    def _loop(self):
        try:
            while self.connected:
                try:
                    msg = self.receive()
                    decoded = Packet.decode(msg)

                    self.OnSignal.fire(decoded)
                    self.OnSignalOfType.fire(decoded)

                except (ConnectionAbortedError, ConnectionResetError):
                    self.OnDisconnect.fire()

        except OSError as e:
            if not self.connected:
                pass

    def disconnect(self) -> None:
        """Disconnect the client from the server. Calls OnDisconnect
        """

        self.connected = False
        self.socket.close()
        self.OnDisconnect.fire()

    def send(self, message, *, force=False) -> None:
        """Sends a packet to the server.

        Args:
            message (Packet): The packet to send to the host.
            force (bool, optional): Forcefully send the packet, even if the connection is not verified as active. Defaults to False.

        Raises:
            ConnectionError: No active connection to host and not set as forced-send.
        """
        if self.connected or force:
            return super().send(self.socket, message)

        else:
            raise ConnectionError("No active connection to host")

    def receive(self, *, force=False) -> Packet:
        """Receive the next packet. Recommended to use OnSignal or OnSignalOfType instead.

        Args:
            force (bool, optional): Forcefully receive packet, even if the connection is not verified as active. Defaults to False.

        Raises:
            ConnectionError: No active connection to server and not set as forced-send.

        Returns:
            Packet: The packet that was received.
        """
        if self.connected or force:
            return super().receive(self.socket)

        else:
            raise ConnectionError("No active connection to host")
