from threading import Event as Waiter


class Event:
    def __init__(self):
        self._callbacks = []
        self._waiters = []
        self._waiter_return = None

    def __call__(self, fn):
        self.connect(fn)

    def fire(self, *args):
        for callback in self._callbacks:
            callback(*args)

        for w in self._waiters:
            self._waiter_return = args
            w.set()

        self._waiters = []

    def connect(self, fn):
        self._callbacks.append(fn)

    def wait(self):
        w = Waiter()

        self._waiters.append(w)

        w.wait()

        return self._waiter_return


class ConditionalEvent(Event):
    def __init__(self, checker):
        self._callbacks = {}
        self._waiters = {}
        self._conditioner = checker
        self._waiter_return = None

    def __call__(self, condition):
        return self.connect(condition)

    def fire(self, *args):
        target_condition = self._conditioner(*args)

        for condition, callback in self._callbacks.items():
            if condition == target_condition:
                callback(*args)

        for condition, waiter in self._waiters:
            if condition == target_condition:
                self._waiter_return = args
                waiter.set()
                self._waiter_return = None

    def connect(self, condition):
        def _handle_connect(fn):
            self._callbacks[condition] = fn

            return fn

        return _handle_connect

    def wait(self, condition):
        w = Waiter()

        if condition in self._waiters:
            self._waiters[condition].append(w)

        else:
            self._waiters[condition] = [w]

        w.wait()
        return self._waiter_return
