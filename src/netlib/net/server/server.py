from typing import List

from netlib.net.packet import Packet

from ..net_object import NetObject
from .connection import Connection
from socket import gethostbyname, gethostname
from threading import Thread
from netlib.utils.events import Event


class Server(NetObject):
    """Server object used to manage clients
    """

    def __init__(self, ip: str, port: int) -> None:
        """Server object used to manage clients

        Args:
            ip (str): The ip of the host machine
            port (int): The port to handle packets
        """

        super().__init__(ip, port)

        self._loop = Thread(target=self._loop, daemon=False)
        self.connections = {}
        self.running = False

        self.OnConnect = Event()
        self.OnDisconnect = Event()
        self.OnRun = Event()
        self.OnClose = Event()

    def run(self, backlog: int = 8) -> None:
        """Used to run event loop and listen to connections

        Args:
            backlog (int, optional): The max amount of connections to listen to. Defaults to 8.
        """
        self.socket.bind((self.ip, self.port))
        self.socket.listen(backlog)
        self.running = True
        self._loop.start()
        self.OnRun.fire()

    def get_connections(self) -> List[Connection]:
        """Returns a list of all active connections

        Returns:
            List[Connection]: A list of all active connections
        """
        return [conn for conn in self.connections.values()]

    def send_to_all(self, packet: Packet) -> None:
        """Send a packet to all active connection.

        Args:
            packet (Packet): The packet to send.
        """

        for conn in self.connections.values():
            if conn.connected:
                conn.send(packet)

    def send_to_all_except(self, packet: Packet, *exclusions: List[Connection]) -> None:
        """Send a packet to all active connections except those in exclusions.

        Args:
            packet (Packet): The packet to send.
            exclusions (List<Connection>): The connections to exclude.
        """

        for conn in self.connections.values():
            if conn not in exclusions and conn.connected:
                conn.send(packet)

    @staticmethod
    def get_machine_info() -> str:
        """Returns the local machine's host name

        Returns:
            str: The local machine's host name
        """
        return gethostbyname(gethostname())

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

                conn.connected = False

        self.OnClose.fire()
