# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-03-25

### Added
- `TextDigest` class with `truncate`, `first_n_sentences`, `word_count`, `char_count`, `extract_lines`
- `DataDigest` class with `summarize_dict`, `flatten`, `top_n`, `frequency`, `chunk`
- `DigestReport` for structured digests of any content type
- `@digest_output` decorator for automatic output summarization
- Zero external dependencies (uses `re` and `collections.Counter` from stdlib)
- Full pytest test suite (22+ tests)
- Python 3.10+ support
