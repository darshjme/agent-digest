"""TextDigest — text summarization without LLMs."""

import re
from typing import Optional


class TextDigest:
    """Summarize and analyze text content."""

    @staticmethod
    def truncate(text: str, max_chars: int, suffix: str = "...") -> str:
        """Truncate text to max_chars, appending suffix if truncated."""
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        if max_chars < 0:
            raise ValueError("max_chars must be >= 0")
        if len(text) <= max_chars:
            return text
        # Make room for suffix
        cut = max_chars - len(suffix)
        if cut < 0:
            return suffix[:max_chars]
        return text[:cut] + suffix

    @staticmethod
    def first_n_sentences(text: str, n: int) -> str:
        """Return the first n sentences from text."""
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        if n <= 0:
            return ""
        # Split on sentence-ending punctuation followed by whitespace or end-of-string
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        # Filter out empty strings
        sentences = [s for s in sentences if s]
        return " ".join(sentences[:n])

    @staticmethod
    def word_count(text: str) -> int:
        """Count words in text."""
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        return len(text.split()) if text.strip() else 0

    @staticmethod
    def char_count(text: str) -> int:
        """Count characters in text (including whitespace)."""
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        return len(text)

    @staticmethod
    def extract_lines(
        text: str,
        pattern: Optional[str] = None,
        max_lines: Optional[int] = None,
    ) -> list[str]:
        """Extract lines from text, optionally filtering by regex pattern and limiting count."""
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        lines = text.splitlines()
        if pattern is not None:
            regex = re.compile(pattern)
            lines = [line for line in lines if regex.search(line)]
        if max_lines is not None:
            lines = lines[:max_lines]
        return lines
