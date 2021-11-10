from socket import socket

from netlib.net.signal import Signal


class TCPStream:
	BUFFER = 1024

	def send(self, socket: socket, signal: Signal) -> None:
		e_signal = signal.encode()

		socket.send(e_signal)

	def receive(self, socket: socket) -> Signal:
		e_signal = b""
		e_chunk = b""

		while b"\r" not in e_chunk:
			e_chunk = socket.recv(self.BUFFER)

			e_signal += e_chunk

		signal = Signal.decode(e_signal)

		return signal
