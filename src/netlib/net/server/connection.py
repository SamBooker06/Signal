from socket import socket
from uuid import uuid4

from ...utils.events import ConditionalEvent, Event
from ...utils.parallel import Parallel
from ..tcpstream import TCPStream
from ..signal import Signal

class Connection(TCPStream):
	def __init__(self, socket: socket):
		self.OnSignal = ConditionalEvent(lambda s: [s.route, "/"], default="/")
		self.OnDisconnect = Event()

		self.socket = socket
		self.info = "{}".format(*socket.getsockname())
		self.active = True

		self.UUID = uuid4()

		self._event_loop = Parallel(self._loop)
		self._event_loop.start()

	def send(self, signal: Signal) -> bool:
		success = False

		try:
			super().send(self.socket, signal)

			success = True

		finally:
			return success

	def disconnect(self) -> None:
		disc_signal = Signal({}, "/__disconnect")

		self.send(disc_signal)
		self._event_loop.cancel()
		self.active = False
		self.socket.close()

	def _loop(self):
		while self.active:
			signal = self.receive(self.socket)

			if signal.route == "/__disconnect":
				self.active = False

			else:
				self.OnSignal.fire(signal)

		self.socket.close()
		self.OnDisconnect.fire()
