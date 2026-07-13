"""Optional lightweight timing decorators."""

from functools import wraps
import sys
import time


GLOBAL_TIMER_ON_DEFAULT = False


class MyTimer:
    def __init__(self, timer_name: str) -> None:
        self.timer_name = timer_name
        self.begin_time = time.perf_counter()
        self.timer_on = GLOBAL_TIMER_ON_DEFAULT

    def toggle(self) -> None:
        self.timer_on = not self.timer_on

    def timer_show(self) -> float:
        elapsed = time.perf_counter() - self.begin_time
        if self.timer_on:
            print(f"TIMER: {self.timer_name}: {elapsed:.3f}s", file=sys.stderr)
        return elapsed


def timer_wrap(function, function_name):
    @wraps(function)
    def wrapped_function(*args, **kwargs):
        timer = MyTimer(str(function_name))
        try:
            return function(*args, **kwargs)
        finally:
            timer.timer_show()

    return wrapped_function


def timer_wrap_gen(function_name):
    return lambda function: timer_wrap(function, function_name)
