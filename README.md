# agent-digest

> **Data summarization utilities for agent outputs** — truncate text, summarize dicts, top-N lists, frequency counts, and structured digest reports. Zero dependencies.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Problem

Agents produce large outputs: 10,000-word text, deeply nested JSON, massive lists. Downstream components need summaries: "top 5 items", "first 100 words", "key-value extract". Without utilities, agents do ad-hoc string slicing everywhere — brittle, inconsistent, untested.

**agent-digest** solves this with a lean, zero-dependency toolkit.

---

## Installation

```bash
pip install agent-digest
```

---

## Quick Start — Agent Output Summarization

```python
from agent_digest import TextDigest, DataDigest, DigestReport, digest_output

# ── Scenario: LLM agent returned a 5000-word analysis ──────────────────────
agent_text_output = """
The quarterly revenue analysis shows significant growth across all segments.
Product A achieved 34% YoY growth. Product B saw slight decline at -2%.
The APAC region outperformed all others with 61% growth. Operating margins
improved to 18.4% from 15.1% last year. R&D spend increased by 22%...
""" * 20  # simulate large output

# Truncate to 200 chars for downstream display
summary = TextDigest.truncate(agent_text_output, max_chars=200)
print(summary)
# → "The quarterly revenue analysis shows significant growth..."

# Get first 2 sentences only
headline = TextDigest.first_n_sentences(agent_text_output, n=2)
print(headline)
# → "The quarterly revenue analysis shows significant growth across all segments. Product A achieved 34% YoY growth."

# Extract only lines containing numbers
metrics = TextDigest.extract_lines(agent_text_output, pattern=r"\d+%", max_lines=5)
print(metrics)
# → lines containing percentage figures

# ── Scenario: Agent returned a giant JSON blob ──────────────────────────────
agent_json_output = {
    "model": "gpt-4o",
    "tokens_used": 8192,
    "latency_ms": 1423,
    "usage": {"prompt": 4000, "completion": 4192},
    "metadata": {"session_id": "abc123", "user": "darshan", "org": "acme"},
    "results": [{"score": 0.95, "label": "positive"} for _ in range(1000)],
    "raw_logprobs": list(range(8192)),  # massive
}

# Summarize: keep top 10 keys, truncate long values
digest = DataDigest.summarize_dict(agent_json_output, max_keys=5, max_value_len=30)
print(digest)
# → {'model': 'gpt-4o', 'tokens_used': 8192, 'latency_ms': 1423, ...}

# Flatten nested metadata
flat = DataDigest.flatten(agent_json_output["metadata"])
print(flat)
# → {'session_id': 'abc123', 'user': 'darshan', 'org': 'acme'}

# Top 5 results by score
top_results = DataDigest.top_n(
    agent_json_output["results"],
    key=lambda x: x["score"],
    n=5
)

# ── Scenario: Agent returned a list of 10,000 log labels ───────────────────
log_labels = ["error", "info", "warning", "error", "error", "info"] * 1000

freq = DataDigest.frequency(log_labels)
print(freq)
# → {'error': 3000, 'info': 2000, 'warning': 1000}

# Process in batches of 500
batches = DataDigest.chunk(log_labels, size=500)
print(f"Processing {len(batches)} batches")

# ── DigestReport — all-in-one structured digest ─────────────────────────────
report = DigestReport(agent_text_output, label="quarterly-analysis")
print(report.summary(max_length=150))
print(report.stats())
# → {'type': 'str', 'char_count': ..., 'word_count': ..., 'line_count': ...}
print(report.to_dict())

# ── @digest_output — decorator for auto-summarization ───────────────────────
@digest_output(max_chars=300)
def run_analysis_agent(query: str) -> str:
    # Simulated large agent output
    return f"Analysis of '{query}': " + "Very detailed findings. " * 200

result = run_analysis_agent("Q4 revenue")
print(len(result))  # → ≤ 300
print(result.endswith("..."))  # → True


@digest_output(max_chars=50)
def fetch_agent_metadata() -> dict:
    return {"key_" + str(i): "value_" * 10 for i in range(50)}

meta = fetch_agent_metadata()
print(type(meta))  # → dict (summarized automatically)
```

---

## API Reference

### `TextDigest`

| Method | Description |
|--------|-------------|
| `truncate(text, max_chars, suffix="...")` | Truncate to max_chars with suffix |
| `first_n_sentences(text, n)` | Return first n sentences |
| `word_count(text)` | Count words |
| `char_count(text)` | Count characters |
| `extract_lines(text, pattern=None, max_lines=None)` | Filter/limit lines |

### `DataDigest`

| Method | Description |
|--------|-------------|
| `summarize_dict(data, max_keys=10, max_value_len=50)` | Limit keys and truncate values |
| `flatten(data, separator=".", max_depth=None)` | Flatten nested dict |
| `top_n(items, key=None, n=5)` | Top N items, optionally by key |
| `frequency(items)` | Count occurrences |
| `chunk(items, size)` | Split into fixed-size chunks |

### `DigestReport`

```python
report = DigestReport(content, label="optional-label")
report.summary(max_length=200)   # → str
report.stats()                   # → dict (type-specific)
report.to_dict()                 # → full dict representation
```

### `@digest_output`

```python
@digest_output(max_chars=500)
def my_agent_function() -> str | dict:
    ...  # str → truncated if > max_chars; dict → summarized
```

---

## Design Principles

- **Zero dependencies** — only `re`, `collections.Counter`, `functools` from stdlib
- **No LLMs** — purely algorithmic, deterministic, fast
- **Type-safe** — raises `TypeError` on wrong inputs
- **Composable** — functions are stateless, combine freely

---

## License

MIT
