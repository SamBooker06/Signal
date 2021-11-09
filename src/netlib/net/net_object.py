from socket import socket, AF_INET, SOCK_STREAM
from ipaddress import ip_address


class NetObject:
    def __init__(self, ip, port):
        self.socket = socket(AF_INET, SOCK_STREAM)

        assert type(port) == int, "Port must be number"

        try:
            assert type(ip) == str, "IP address must be string"
            ip_address(ip)

        except (ValueError, AssertionError):
            raise ValueError("Invalid IP address")

        self.ip = ip
        self.port = port
