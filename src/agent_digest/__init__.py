"""agent-digest: Data summarization utilities for agent outputs."""

from .text_digest import TextDigest
from .data_digest import DataDigest
from .report import DigestReport
from .decorators import digest_output

__all__ = ["TextDigest", "DataDigest", "DigestReport", "digest_output"]
__version__ = "1.0.0"
