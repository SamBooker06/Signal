from socket import socket, AF_INET, SOCK_STREAM

from .signal import Signal
from .tcpstream import TCPStream
from ..utils.parallel import Parallel
from ..utils.events import ConditionalEvent, Event

class Client(TCPStream):
	def __init__(self, ip, port):
		self.socket = socket(AF_INET, SOCK_STREAM)
		self.active = False
		self.info = (ip, port)

		self.OnConnect = Event()
		self.OnDisconnect = Event()
		self.OnSignal = ConditionalEvent(lambda s: [s.route, "/"], default="/")

		self._event_loop = Parallel(self._loop)


	def send(self, signal):
		success = False

		try:
			super().send(self.socket, signal)
			success = True

		finally:
			return success


	def connect(self):
		self.socket.connect(self.info)
		self.active = True
		self._event_loop.start()

		self.OnConnect.fire()


	def disconnect(self):
		self.send(Signal({}, "/__disconnect"))

		self._event_loop.cancel()
		self.socket.close()

		self.active = False
		self.OnDisconnect.fire()


	def _loop(self):
		while self.active:
			signal = self.receive(self.socket)

			if signal.route == "/__disconnect":
				self.active = False

			else:
				self.OnSignal.fire(signal)

		self.OnDisconnect.fire()
		self.socket.close()
