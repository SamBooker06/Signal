from socket import socket, AF_INET, SOCK_STREAM
from ipaddress import ip_address


class Endpoint:
    def __init__(self, ip, port):
        self.socket = socket(AF_INET, SOCK_STREAM)

        assert type(port) == int, "Port must be number"

        try:
            ip_address(ip)

        except ValueError:
            raise ValueError("Invalid IP address")

        self.ip = ip
        self.port = port

    # Sends message of bytes to endpoint

    def send(self, sock, message):
        sock.send(message)

    def receive(self, sock):
        message = sock.recv(1024)

        return message
