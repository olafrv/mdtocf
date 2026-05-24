import hashlib
import pytest
from mdtocf.classes.KeyValue import KeyValue


@pytest.fixture
def kv(tmp_path):
    return KeyValue(str(tmp_path / "test.db"))


class TestLoad:
    def test_missing_key_returns_default(self, kv):
        result = kv.load("nonexistent")
        assert result == {"id": None, "title": "", "sha256": ""}

    def test_load_after_save(self, kv):
        kv.save("myfile.md", {"id": "123", "title": "My Page", "sha256": "abc"})
        result = kv.load("myfile.md")
        assert result == {"id": "123", "title": "My Page", "sha256": "abc"}

    def test_load_preserves_none_id(self, kv):
        kv.save("file.md", {"id": None, "title": "Title", "sha256": "xyz"})
        result = kv.load("file.md")
        assert result["id"] is None


class TestSave:
    def test_save_overwrites_existing(self, kv):
        kv.save("file.md", {"id": "1", "title": "Old", "sha256": "old"})
        kv.save("file.md", {"id": "2", "title": "New", "sha256": "new"})
        assert kv.load("file.md")["title"] == "New"

    def test_save_multiple_keys(self, kv):
        kv.save("a.md", {"id": "1", "title": "A", "sha256": ""})
        kv.save("b.md", {"id": "2", "title": "B", "sha256": ""})
        assert kv.load("a.md")["id"] == "1"
        assert kv.load("b.md")["id"] == "2"


class TestRemove:
    def test_remove_returns_default_on_load(self, kv):
        kv.save("file.md", {"id": "1", "title": "Page", "sha256": "h"})
        kv.remove("file.md")
        assert kv.load("file.md") == {"id": None, "title": "", "sha256": ""}

    def test_remove_not_in_keys(self, kv):
        kv.save("file.md", {"id": "1", "title": "Page", "sha256": "h"})
        kv.remove("file.md")
        assert "file.md" not in kv.keys()


class TestKeys:
    def test_empty_store(self, kv):
        assert kv.keys() == []

    def test_keys_after_saves(self, kv):
        kv.save("a.md", {"id": "1", "title": "A", "sha256": ""})
        kv.save("b.md", {"id": "2", "title": "B", "sha256": ""})
        assert sorted(kv.keys()) == ["a.md", "b.md"]


class TestSha256:
    def test_known_hash(self, kv):
        expected = hashlib.sha256("hello".encode()).hexdigest()
        assert kv.sha256("hello") == expected

    def test_deterministic(self, kv):
        assert kv.sha256("test") == kv.sha256("test")

    def test_different_inputs_differ(self, kv):
        assert kv.sha256("foo") != kv.sha256("bar")

    def test_empty_string(self, kv):
        expected = hashlib.sha256(b"").hexdigest()
        assert kv.sha256("") == expected
