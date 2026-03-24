"""DataDigest — dict/list summarization utilities."""

from collections import Counter
from typing import Any, Callable, Optional


class DataDigest:
    """Summarize and analyze dict/list data structures."""

    @staticmethod
    def summarize_dict(
        data: dict,
        max_keys: int = 10,
        max_value_len: int = 50,
    ) -> dict:
        """Return a summarized dict with limited keys and truncated values."""
        if not isinstance(data, dict):
            raise TypeError(f"Expected dict, got {type(data).__name__}")
        result = {}
        for i, (k, v) in enumerate(data.items()):
            if i >= max_keys:
                break
            str_v = str(v)
            if len(str_v) > max_value_len:
                str_v = str_v[:max_value_len - 3] + "..."
                result[k] = str_v
            else:
                result[k] = v
        return result

    @staticmethod
    def flatten(
        data: dict,
        separator: str = ".",
        max_depth: Optional[int] = None,
    ) -> dict:
        """Flatten a nested dict into a single-level dict with compound keys."""
        if not isinstance(data, dict):
            raise TypeError(f"Expected dict, got {type(data).__name__}")

        result: dict = {}

        def _flatten(obj: Any, prefix: str, depth: int) -> None:
            if isinstance(obj, dict) and (max_depth is None or depth < max_depth):
                for k, v in obj.items():
                    new_key = f"{prefix}{separator}{k}" if prefix else str(k)
                    _flatten(v, new_key, depth + 1)
            else:
                result[prefix] = obj

        _flatten(data, "", 0)
        return result

    @staticmethod
    def top_n(
        items: list,
        key: Optional[Callable] = None,
        n: int = 5,
    ) -> list:
        """Return the top n items from a list, optionally sorted by key."""
        if not isinstance(items, list):
            raise TypeError(f"Expected list, got {type(items).__name__}")
        if n <= 0:
            return []
        sorted_items = sorted(items, key=key, reverse=True)
        return sorted_items[:n]

    @staticmethod
    def frequency(items: list) -> dict:
        """Count occurrences of each item in a list."""
        if not isinstance(items, list):
            raise TypeError(f"Expected list, got {type(items).__name__}")
        return dict(Counter(items))

    @staticmethod
    def chunk(items: list, size: int) -> list[list]:
        """Split a list into fixed-size chunks."""
        if not isinstance(items, list):
            raise TypeError(f"Expected list, got {type(items).__name__}")
        if size <= 0:
            raise ValueError("size must be > 0")
        return [items[i : i + size] for i in range(0, len(items), size)]
