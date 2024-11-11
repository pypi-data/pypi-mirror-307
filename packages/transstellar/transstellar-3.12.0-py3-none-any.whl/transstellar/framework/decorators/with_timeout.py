import datetime
import time
from functools import wraps
from typing import Callable, TypeVar

T = TypeVar("T")


def with_timeout(timeout: int = 10):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):

            number_of_args = len(args)
            timeout_arg = args[number_of_args - 1]
            timeout_arg_existed = f"{timeout_arg}".isnumeric()

            if "timeout" in kwargs:
                remaining_timeout = kwargs["timeout"]
            elif timeout_arg_existed:
                remaining_timeout = timeout_arg
            else:
                remaining_timeout = timeout

            start_time = datetime.datetime.now()

            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                end_time = datetime.datetime.now()
                time_difference = (end_time - start_time).total_seconds()
                new_remaining_timeout = remaining_timeout - time_difference - 1

                if new_remaining_timeout > 0:
                    kwargs["timeout"] = new_remaining_timeout

                    time.sleep(1)

                    return wrapper(self, *args, **kwargs)
                else:
                    raise e

        return wrapper

    return decorator
