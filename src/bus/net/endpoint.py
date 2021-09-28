from .net_object import NetObject


class Endpoint(NetObject):
    # Sends message of bytes to endpoint
    def send(self, sock, message):
        sock.send(message)

    def receive(self, sock):
        message = sock.recv(1024)

        return message
