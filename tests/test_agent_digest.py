"""Comprehensive pytest test suite for agent-digest — 22+ tests."""

import pytest
from agent_digest import TextDigest, DataDigest, DigestReport, digest_output


# ─── TextDigest ───────────────────────────────────────────────────────────────

class TestTruncate:
    def test_no_truncation_needed(self):
        assert TextDigest.truncate("hello", 10) == "hello"

    def test_truncation_applied(self):
        result = TextDigest.truncate("hello world", 8)
        assert result == "hello..."
        assert len(result) == 8

    def test_exact_length(self):
        assert TextDigest.truncate("hello", 5) == "hello"

    def test_custom_suffix(self):
        result = TextDigest.truncate("hello world", 7, suffix="[…]")
        assert result.endswith("[…]")
        assert len(result) == 7

    def test_empty_string(self):
        assert TextDigest.truncate("", 5) == ""

    def test_type_error(self):
        with pytest.raises(TypeError):
            TextDigest.truncate(123, 5)  # type: ignore


class TestFirstNSentences:
    def test_single_sentence(self):
        assert TextDigest.first_n_sentences("Hello world.", 1) == "Hello world."

    def test_two_sentences(self):
        text = "Hello world. How are you? I am fine."
        result = TextDigest.first_n_sentences(text, 2)
        assert "Hello world." in result
        assert "How are you?" in result
        assert "I am fine." not in result

    def test_zero_n(self):
        assert TextDigest.first_n_sentences("Hello.", 0) == ""

    def test_n_exceeds_count(self):
        text = "One. Two."
        assert TextDigest.first_n_sentences(text, 10) == "One. Two."


class TestWordCount:
    def test_basic(self):
        assert TextDigest.word_count("hello world foo") == 3

    def test_empty(self):
        assert TextDigest.word_count("") == 0

    def test_whitespace_only(self):
        assert TextDigest.word_count("   ") == 0


class TestCharCount:
    def test_basic(self):
        assert TextDigest.char_count("hello") == 5

    def test_with_spaces(self):
        assert TextDigest.char_count("hi there") == 8


class TestExtractLines:
    def test_no_filter(self):
        text = "line1\nline2\nline3"
        assert TextDigest.extract_lines(text) == ["line1", "line2", "line3"]

    def test_with_pattern(self):
        text = "error: bad\ninfo: ok\nerror: again"
        result = TextDigest.extract_lines(text, pattern=r"^error")
        assert result == ["error: bad", "error: again"]

    def test_max_lines(self):
        text = "a\nb\nc\nd"
        assert TextDigest.extract_lines(text, max_lines=2) == ["a", "b"]

    def test_pattern_and_max_lines(self):
        text = "err1\nerr2\nok\nerr3"
        result = TextDigest.extract_lines(text, pattern="err", max_lines=2)
        assert result == ["err1", "err2"]


# ─── DataDigest ───────────────────────────────────────────────────────────────

class TestSummarizeDict:
    def test_limits_keys(self):
        data = {str(i): i for i in range(20)}
        result = DataDigest.summarize_dict(data, max_keys=5)
        assert len(result) == 5

    def test_truncates_long_values(self):
        data = {"key": "x" * 100}
        result = DataDigest.summarize_dict(data, max_value_len=10)
        assert isinstance(result["key"], str)
        assert len(result["key"]) <= 10

    def test_short_values_unchanged(self):
        data = {"a": 1, "b": "hello"}
        result = DataDigest.summarize_dict(data, max_value_len=50)
        assert result["a"] == 1
        assert result["b"] == "hello"

    def test_type_error(self):
        with pytest.raises(TypeError):
            DataDigest.summarize_dict([1, 2, 3])  # type: ignore


class TestFlatten:
    def test_simple(self):
        data = {"a": {"b": 1}}
        assert DataDigest.flatten(data) == {"a.b": 1}

    def test_deep_nesting(self):
        data = {"a": {"b": {"c": 42}}}
        result = DataDigest.flatten(data)
        assert result == {"a.b.c": 42}

    def test_max_depth(self):
        # max_depth=1 expands one level: "a" → value is the inner dict (unexpanded)
        data = {"a": {"b": {"c": 42}}}
        result = DataDigest.flatten(data, max_depth=1)
        assert "a" in result
        assert isinstance(result["a"], dict)
        # max_depth=2 expands two levels: "a.b" → value is the innermost dict
        result2 = DataDigest.flatten(data, max_depth=2)
        assert "a.b" in result2
        assert isinstance(result2["a.b"], dict)

    def test_custom_separator(self):
        data = {"x": {"y": 99}}
        result = DataDigest.flatten(data, separator="/")
        assert result == {"x/y": 99}

    def test_flat_dict_unchanged(self):
        data = {"a": 1, "b": 2}
        assert DataDigest.flatten(data) == {"a": 1, "b": 2}


class TestTopN:
    def test_basic(self):
        items = [3, 1, 4, 1, 5, 9, 2, 6]
        assert DataDigest.top_n(items, n=3) == [9, 6, 5]

    def test_with_key(self):
        items = [{"v": 10}, {"v": 3}, {"v": 7}]
        result = DataDigest.top_n(items, key=lambda x: x["v"], n=2)
        assert result == [{"v": 10}, {"v": 7}]

    def test_zero_n(self):
        assert DataDigest.top_n([1, 2, 3], n=0) == []


class TestFrequency:
    def test_basic(self):
        result = DataDigest.frequency(["a", "b", "a", "c", "b", "a"])
        assert result == {"a": 3, "b": 2, "c": 1}

    def test_empty(self):
        assert DataDigest.frequency([]) == {}


class TestChunk:
    def test_even(self):
        assert DataDigest.chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

    def test_uneven(self):
        assert DataDigest.chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    def test_invalid_size(self):
        with pytest.raises(ValueError):
            DataDigest.chunk([1, 2, 3], 0)


# ─── DigestReport ─────────────────────────────────────────────────────────────

class TestDigestReport:
    def test_str_summary(self):
        report = DigestReport("Hello " * 50, label="test")
        s = report.summary(max_length=20)
        assert len(s) <= 20

    def test_str_stats(self):
        report = DigestReport("Hello world.")
        stats = report.stats()
        assert stats["type"] == "str"
        assert stats["word_count"] == 2
        assert stats["char_count"] == 12

    def test_dict_stats(self):
        report = DigestReport({"a": 1, "b": 2})
        stats = report.stats()
        assert stats["type"] == "dict"
        assert stats["key_count"] == 2

    def test_list_stats(self):
        report = DigestReport([1, 2, 3, "x"])
        stats = report.stats()
        assert stats["type"] == "list"
        assert stats["item_count"] == 4

    def test_to_dict(self):
        report = DigestReport("test content", label="my-label")
        d = report.to_dict()
        assert d["label"] == "my-label"
        assert d["content_type"] == "str"
        assert "summary" in d
        assert "stats" in d


# ─── @digest_output ───────────────────────────────────────────────────────────

class TestDigestOutput:
    def test_str_truncated(self):
        @digest_output(max_chars=10)
        def big_str():
            return "x" * 100

        result = big_str()
        assert len(result) <= 10
        assert result.endswith("...")

    def test_str_not_truncated(self):
        @digest_output(max_chars=100)
        def small_str():
            return "hello"

        assert small_str() == "hello"

    def test_dict_summarized(self):
        @digest_output(max_chars=20)
        def big_dict():
            return {str(i): "value" * 20 for i in range(5)}

        result = big_dict()
        assert isinstance(result, dict)
        for v in result.values():
            assert len(str(v)) <= 23  # max_value_len=20 + "..."

    def test_other_type_passthrough(self):
        @digest_output(max_chars=10)
        def returns_int():
            return 42

        assert returns_int() == 42

    def test_preserves_function_metadata(self):
        @digest_output(max_chars=100)
        def my_func():
            """My docstring."""
            return "hello"

        assert my_func.__name__ == "my_func"
        assert my_func.__doc__ == "My docstring."
