import inspect
from functools import wraps
from typing import Any, Callable, Dict, Optional


class WithCache:
    def __init__(self, maxsize: Optional[int] = None):
        self.maxsize = maxsize
        self.cache: Dict[str, Any] = {}

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if inspect.ismethod(func) or (args and inspect.isclass(type(args[0]))):
                instance = args[0]
                class_name = instance.__class__.__name__
                cache_args = args[1:]
            else:
                class_name = ""
                cache_args = args

            cache_key = f"{class_name}.{func.__name__}:{str(cache_args)}:{str(kwargs)}"

            if cache_key in self.cache:
                return self.cache[cache_key]

            result = func(*args, **kwargs)

            if self.maxsize is None or len(self.cache) < self.maxsize:
                self.cache[cache_key] = result
            elif self.maxsize > 0:
                self.cache.pop(next(iter(self.cache)))
                self.cache[cache_key] = result

            return result

        return wrapper
