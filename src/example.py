from netlib import Server, Client, Packet
from netlib.net.server.connection import Connection


PORT = 7777


def setup_server(h: Server):
    usernames = {}

    @h.OnConnect
    def handle_connection(conn: Connection):

        @conn.OnSignalOfType("set-username")
        def set_username(packet: Packet):
            username = packet.body["username"]
            usernames[conn.UUID] = username

        @conn.OnSignalOfType("send-message")
        def handle_messages(packet: Packet):
            content = packet.body["content"]
            username = usernames[conn.UUID]

            message = Packet({
                "content": content,
                "username": username
            }, request_type="message")

            h.send_to_all_except(message, conn)

        @conn.OnDisconnect
        def handle_disconnect():
            username = usernames[conn.UUID]

            h.send_to_all_except(Packet({
                "username": username
            }, request_type="disconnect-message"))


def setup_client(c: Client):
    @c.OnSignalOfType("message")
    def display_message(packet: Packet):
        username = packet.body["username"]
        content = packet.body["content"]

        print(f"{username}) {content}")

    @c.OnSignalOfType("disconnect-message")
    def display_disconnect(packet: Packet):
        username = packet.body["username"]

        print(f"[{username}] HAS DISCONNECTED")


def chat_app():
    ip = Server.get_machine_info()
    port = PORT

    h = Server(ip, port)

    client_one = Client(ip, port)
    client_two = Client(ip, port)

    setup_server(h)
    setup_client(client_one)
    setup_client(client_two)

    c1_username = "Jim"
    c2_username = "Jam"

    h.run()

    client_one.connect()
    client_two.connect()

    # Set client usernames
    client_one.send(Packet({
        "username": c1_username
    }, request_type="set-username"))

    client_two.send(Packet({
        "username": c2_username
    }, request_type="set-username"))

    # Conversation
    client_one.send(Packet({
        "content": "Hello. Is anyone here?"
    }, request_type="send-message"))

    client_two.send(Packet({
        "content": "I'm here!"
    }, request_type="send-message"))

    client_one.disconnect()

    client_two.send(Packet({
        "content": ":("
    }, request_type="send-message"))

    client_two.disconnect()
    # h.close()


def main():
    chat_app()


main()
