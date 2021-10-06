from bus import Host, Client, Packet
from time import sleep as wait


def main():
    h = Host(Host.get_machine_info(), 7092)
    names = {}

    @h.OnConnect
    def handle_connect(conn):
        print("Connected")
        conn.send(Packet({"message": "Hello, World!", "author": "Joe"}))

        @conn.OnMessage
        def handle_message(packet):
            print("Received message")

        @conn.OnMessageOfType("set-username")
        def set_username(packet):
            names[conn.UUID] = packet.body['username']

        print

    @h.OnDisconnect
    def handle_disconnect(conn):
        print("Disconnected")

    h.run()

    c = Client(Host.get_machine_info(), 7092)

    @c.OnConnect
    def handle_connect():
        c.send(Packet({"username": "jog"}, request_type="set-username"))

    c.connect()


if __name__ == "__main__":
    main()
