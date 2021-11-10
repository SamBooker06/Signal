from json import dumps, loads
from base64 import b64encode, b64decode

class Signal:
	def __init__(self, payload: dict, route="/"):
		assert type(payload) is dict, "Payload must be dictionary"
		assert type(route) is str, "Route must be a string"

		assert "route" not in payload, "Invalid payload keys"

		self.payload = payload
		self.route = route


	def encode(self):
		dump = dumps(self.payload)

		encoded_dump = b64encode(dump.encode("utf-8"))
		encoded_route = b64encode(self.route.encode("utf-8"))

		e_signal = encoded_route + b"--" + encoded_dump + b"\r"

		return e_signal


	@staticmethod
	def decode(b64: bytes):
		target = b64.split(b"\r")[0]

		e_route, e_dump = target.split(b"--")

		route = b64decode(e_route).decode("utf-8")
		dump = b64decode(e_dump).decode("utf-8")
		payload = loads(dump)

		signal = Signal(payload, route)

		return signal

