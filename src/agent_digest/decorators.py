"""digest_output decorator — auto-summarize function return values."""

import functools
from typing import Any, Callable
from .text_digest import TextDigest
from .data_digest import DataDigest


def digest_output(max_chars: int = 500) -> Callable:
    """
    Decorator that automatically digests function return values.

    - str returns > max_chars are truncated with suffix
    - dict returns are summarized with DataDigest.summarize_dict
    - other types pass through unchanged
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            if isinstance(result, str):
                if len(result) > max_chars:
                    return TextDigest.truncate(result, max_chars)
                return result
            elif isinstance(result, dict):
                return DataDigest.summarize_dict(result, max_value_len=max_chars)
            return result
        return wrapper
    return decorator
