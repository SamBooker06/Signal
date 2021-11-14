from typing import List
from socket import gethostbyname, gethostname

from ...utils.parallel import Parallel
from ...utils.events import Event
from ..netobject import NetObject
from ..signal import Signal
from .connection import Connection

class Server(NetObject):
	@property
	def connections(self) -> List[Connection]:
		return [conn for conn in self._connections if conn.active]

	def __init__(self, ip: str, port: int):
		super().__init__(ip, port)
		self.running = False
		self._connections = []

		self.OnRun = Event()
		self.OnExit = Event()
		self.OnConnection = Event()
		self.OnDisconnection = Event()

		self._event_loop = Parallel(self._loop)


	@staticmethod
	def get_host_machine() -> str:
		return gethostbyname(gethostname())


	def _loop(self):
		self.running = True

		while self.running:
			try:
				sock, _ = self.socket.accept()

				conn = Connection(sock)
				conn.OnDisconnect.connect(lambda: self.OnDisconnection.fire(conn))

				self._connections.append(conn)

				self.OnConnection.fire(conn)

			except ConnectionResetError:
				pass


	def run(self, backlog: int=8) -> None:
		self.socket.bind(self.info)
		self.socket.listen(backlog)

		self._event_loop.start()
		self.OnRun.fire()


	def send_to_all(self, signal: Signal) -> None:
		for conn in self.connections:
			conn.send(signal)

	def sent_to_all_except(self, signal: Signal, *blacklist: List[Connection]) -> None:
		for conn in self.connections:
			if conn not in blacklist:
				conn.send(signal)


	def exit(self) -> None:
		self.running = False
		self._event_loop.cancel()
		self.socket.close()

		self.OnExit.fire()
