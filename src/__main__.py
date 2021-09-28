from bus.net.server.host import Host


def main():
    h = Host("127.0.0.1", 7092)
    h.run()


if __name__ == "__main__":
    main()
