# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 1.0.x   | ✅ Yes    |

## Reporting a Vulnerability

If you discover a security vulnerability, **do not open a public GitHub issue**.

Instead, please report it privately via GitHub's Security Advisory feature:
1. Go to the repository → Security → Advisories → New draft security advisory.
2. Describe the vulnerability, steps to reproduce, and potential impact.

We will acknowledge your report within 48 hours and aim to release a fix within 14 days.

## Scope

`agent-digest` has **zero external dependencies** and performs no I/O, network calls, or execution of arbitrary code. The primary security surface is regex processing in `TextDigest.extract_lines` — pathological regex patterns (ReDoS) supplied by untrusted callers are the main risk. Callers should validate or sanitize regex patterns from untrusted input before passing them to library functions.
