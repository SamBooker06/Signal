from threading import Event as waiter


class Event:
    def __init__(self):
        self._callbacks = []
        self._waiters = []

    def __call__(self, fn):
        self.connect(fn)

    def fire(self, *args):
        for callback in self._callbacks:
            callback(*args)

        for w in self._waiters:
            w.set()

        self._waiters = []

    def connect(self, fn):
        self._callbacks.append(fn)

    def wait(self):
        w = waiter()

        self._waiters.append(w)

        w.wait()
