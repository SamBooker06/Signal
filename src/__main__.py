from bus.net.server.host import Host
from bus.net.client import Client


def main():
    h = Host("127.0.0.1", 7092)
    h.run()
    h.OnConnect

    c = Client("127.0.0.1", 7092)
    c.connect()


if __name__ == "__main__":
    main()
