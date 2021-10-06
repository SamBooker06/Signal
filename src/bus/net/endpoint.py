from bus.utils.events import Event
from .net_object import NetObject
from .packet import Packet


class Endpoint(NetObject):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    # Sends message of bytes to endpoint

    def send(self, sock, message):
        assert type(message) is Packet, "Invalid message type ({}). Must be type Packet".format(
            type(message))

        sock.send(message.encode())

    def receive(self, sock):
        message = sock.recv(1024)

        return message
