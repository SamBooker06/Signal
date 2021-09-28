from ..endpoint import Endpoint


class Connection(Endpoint):
    def __init__(self, socket):
        ip, port = socket.getpeername()
        super().__init__(ip, port)

        self.socket = socket

    def send(self, message):
        return super().send(self.socket, message)

    def receive(self):
        return super().receive(self.socket)
