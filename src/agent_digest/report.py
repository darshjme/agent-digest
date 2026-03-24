"""DigestReport — structured digest of any content."""

from typing import Any, Optional
from .text_digest import TextDigest
from .data_digest import DataDigest


class DigestReport:
    """Generate a structured digest report for any content type."""

    def __init__(self, content: Any, label: Optional[str] = None) -> None:
        self.content = content
        self.label = label
        self._content_type = type(content).__name__

    def summary(self, max_length: int = 200) -> str:
        """Return a human-readable summary of the content."""
        if isinstance(self.content, str):
            return TextDigest.truncate(self.content, max_length)
        elif isinstance(self.content, dict):
            summarized = DataDigest.summarize_dict(self.content, max_value_len=40)
            raw = str(summarized)
            return TextDigest.truncate(raw, max_length)
        elif isinstance(self.content, list):
            count = len(self.content)
            preview = str(self.content[:5])
            raw = f"List[{count} items]: {preview}"
            return TextDigest.truncate(raw, max_length)
        else:
            raw = str(self.content)
            return TextDigest.truncate(raw, max_length)

    def stats(self) -> dict:
        """Return type-specific statistics about the content."""
        if isinstance(self.content, str):
            return {
                "type": "str",
                "char_count": TextDigest.char_count(self.content),
                "word_count": TextDigest.word_count(self.content),
                "line_count": len(self.content.splitlines()),
            }
        elif isinstance(self.content, dict):
            return {
                "type": "dict",
                "key_count": len(self.content),
                "keys": list(self.content.keys()),
            }
        elif isinstance(self.content, list):
            freq = DataDigest.frequency(
                [type(item).__name__ for item in self.content]
            )
            return {
                "type": "list",
                "item_count": len(self.content),
                "type_distribution": freq,
            }
        else:
            return {
                "type": self._content_type,
                "str_len": len(str(self.content)),
            }

    def to_dict(self) -> dict:
        """Return a full dict representation of the digest report."""
        return {
            "label": self.label,
            "content_type": self._content_type,
            "summary": self.summary(),
            "stats": self.stats(),
        }
