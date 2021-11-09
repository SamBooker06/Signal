from typing import List

from ..net_object import NetObject
from .connection import Connection
from socket import gethostbyname, gethostname
from threading import Thread
from netlib.utils.events import Event


class Host(NetObject):
    """Host object used to manage clients
    """

    def __init__(self, ip: str, port: int) -> None:
        """Host object used to manage clients

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
                del self.connections[key]

        self.OnClose.fire()
