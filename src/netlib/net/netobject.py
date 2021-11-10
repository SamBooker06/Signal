from socket import socket, AF_INET, SOCK_STREAM


class NetObject:
	def __init__(self, ip, port):
		self.socket = socket(AF_INET, SOCK_STREAM)
		self.info = (ip, port)


