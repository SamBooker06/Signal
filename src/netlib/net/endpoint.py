from types import TracebackType
from netlib.utils.events import Event
from .net_object import NetObject
from .packet import Packet


class Endpoint(NetObject):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    # Sends message of bytes to endpoint

    def send(self, sock, message):
        assert type(message) is Packet, "Invalid message type ({}). Must be type Packet".format(
            type(message))

        sock.send(message.encode() + b"\r")

    def receive(self, sock):
        looping = True
        message = b""

        while looping:
            chunk: bytes = sock.recv(1024)
            if chunk[:-2:-1] == b"\r":
                looping = False

            if b"\r" in chunk:
                chunk = chunk.split(b"\r")[0]

            message += chunk

        return message
