from threading import Event as Waiter
from types import FunctionType
from typing import Any, List


class Event:
    """Object used for event-based programming
    """

    def __init__(self) -> None:
        """Object used for event-based programming
        """
        self._callbacks = []
        self._waiters = []
        self._waiter_return = None

    def __call__(self, fn: FunctionType) -> None:
        """Connect a function to be called when the event is fired.

        Args:
            fn (function): The function to be called.
        """
        self.connect(fn)

    def fire(self, *args: List[Any]) -> None:
        """Fire the event with any arguments.
        """
        for callback in self._callbacks:
            callback(*args)

        for w in self._waiters:
            self._waiter_return = args
            w.set()

        self._waiters = []

    def connect(self, fn: FunctionType) -> None:
        """Connect a function to be called when the event is fired.

        Args:
            fn (function): The function to be called.
        """

        self._callbacks.append(fn)

    def wait(self) -> Any:
        """Stops current thread until event is fired.

        Returns:
            Any: The values supplied to event when fired.
        """
        w = Waiter()

        self._waiters.append(w)

        w.wait()

        return self._waiter_return


class ConditionalEvent(Event):
    """Object used for event-based programming under certain conditions.
    """

    def __init__(self, checker: FunctionType, default=None) -> None:
        """Object used for event-based programming under certain conditions.

        Args:
            checker (FunctionType): Function to be called when the event is fired to check values are valid.
        """
        self._default = default
        self._callbacks = {}
        self._waiters = {}
        self._conditioner = checker
        self._waiter_return = None

    def __call__(self, condition: FunctionType=None):
        """Connect a function to be called when the event is fired.

        Args:
            fn (function): The function to be called.
        """

        if condition is None:
            condition = self._default

        return self.connect(condition)

    def fire(self, *args: List[Any]) -> None:
        """Fire the event with any arguments.
        """
        target_condition = self._conditioner(*args)

        for condition, callback in self._callbacks.items():
            if condition in target_condition:
                callback(*args)

        for condition, waiter in self._waiters:
            if condition in target_condition:
                self._waiter_return = args
                waiter.set()
                self._waiter_return = None

    def connect(self, condition: Any=None) -> None:
        """Connect a function to be called when the event is fired under a condition. Must be used as decorator.

        Args:
            condition (Any): Value that must be found as true in the checker to fire event.
        """

        if condition is None:
            condition = self._default

        def _handle_connect(fn: FunctionType):
            self._callbacks[condition] = fn

            return fn

        return _handle_connect

    def wait(self, condition: Any) -> List[Any]:
        """Wait until the event is fired under a condition.

        Args:
            condition (Any): Value that must be found as true in the checker to fire event.

        Return:
            List<Any>: The values passed when the event was fired.
        """
        w = Waiter()

        if condition in self._waiters:
            self._waiters[condition].append(w)

        else:
            self._waiters[condition] = [w]

        w.wait()
        return self._waiter_return
