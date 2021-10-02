from signal import Host, Client, Packet


def create_client(ip, port):
    client = Client(ip, port)

    return client


def create_server(ip, port):
    server = Host(ip, port)

    return server


def main():
    ip, port = "127.0.0.1", 7092

    if input("Create server? y/n").lower() == "y":
        server = create_server(ip, port)

        @server.OnConnect
        def handle_connection(conn):
            @conn.OnMessage
            def handle_message(msg):
                if msg.headers["Request-Type"] == "message":
                    username = msg.body["user"]
                    body = msg.body["message"]

                    for other in server.get_connections():
                        packet = Packet(
                            {"username": username, "message": body}, request_type="echo")

                        other.send(packet)

        server.run()

    else:
        client = create_client(ip, port)

        username = input("Username")

        @client.OnMessage
        def handle_message(msg):
            if msg.headers["Request-Type"] == "echo":
                username = msg.body["user"]
                body = msg.body["message"]

                print("{}) {}".format(username, body))

        client.connect()
        while True:
            message = input("> ")

            packet = Packet(
                {"message": message, "user": username}, request_type="message")

            client.send(packet)


if __name__ == "__main__":
    main()
