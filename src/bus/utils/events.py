from threading import Event as waiter


class Event:
    def __init__(self):
        self._callbacks = []
        self._waiters = []

    def fire(self, *args):
        for callback in self._callbacks:
            callback(*args)

        for w in self._waiters:
            w.set()

        self._waiters = []

    def wait(self):
        w = waiter()

        self._waiters.append(w)

        w.wait()
