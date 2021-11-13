from netlib import Server, Client, Signal
from netlib.net.server.connection import Connection

from time import sleep as wait

def setup_server(s: Server):
	usernames = {}

	@s.OnConnection
	def handle_conn(conn: Connection):
		@conn.OnSignal("/message")
		def handle_message(signal: Signal):
			content = signal.payload.content
			username = usernames[conn.UUID]

			s.sent_to_all_except(Signal({
				"content": f"{username}) {content}"
			}, "/message"), conn)

		@conn.OnSignal("/username/set")
		def set_username(signal: Signal):
			username = signal.payload.username

			usernames[conn.UUID] = username


def setup_client(c: Client):
	@c.OnSignal("/message")
	def display_message(signal: Signal):
		content = signal.payload.content

		print(content)

def send_message(c: Client, content: str):
	c.send(Signal({
		"content": content
	}, "/message"))

	wait(1)


host = Server("127.0.0.1", 7777)

setup_server(host)

host.run()

c1 = Client("127.0.0.1", 7777)
c2 = Client("127.0.0.1", 7777)

setup_client(c1)
setup_client(c2)

c1.connect()
c2.connect()

c1.send(Signal({
	"username": "Bob"
}, "/username/set"))

c2.send(Signal({
	"username": "Alice"
}, "/username/set"))


send_message(c1, "Anyone here")
send_message(c2, "I am!")

c1.disconnect()

wait(1)
send_message(c2, ":(")

wait(1)

c2.disconnect()

wait(2)

host.exit()
