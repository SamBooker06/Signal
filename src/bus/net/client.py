from .endpoint import Endpoint


class Client(Endpoint):
    def __init__(self, ip, port):
        self.connected = False
        super().__init__(ip, port)

    def connect(self):
        try:
            self.socket.connect((self.ip, self.port))
            self.connected = True

        except ConnectionRefusedError:
            raise ConnectionRefusedError("Connection refused.")

    def disconnect(self):
        self.socket.close()
        self.connected = False

    def send(self, message):
        return super().send(self.socket, message)

    def receive(self):
        return super().receive(self.socket)
