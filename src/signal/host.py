from .endpoint import Endpoint


class Host(Endpoint):
    def __init__(self, ip, port):
        super().__init__(ip, port)

        self.connections = {}
        self.running = False

    def run(self):
        pass
