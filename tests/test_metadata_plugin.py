import pytest
from pathlib import Path
from mdtocf.classes.MetadataPlugin import MetadataPlugin


class TestMetadataPlugin:
    """Test cases for MetadataPlugin regex pattern matching."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.mdp = MetadataPlugin()
        self.pattern = self.mdp.METADATA_PATTERN

    def test_metadata_pattern_matches_valid_yaml_frontmatter(self):
        """Test that the regex matches valid YAML front matter."""
        content = """---
title: Example Page
chapter: true
kind: index
---

# Heading"""

        match = self.pattern.match(content)
        assert match is not None
        assert "title: Example Page" in match.group(1)
        assert "chapter: true" in match.group(1)

    def test_metadata_pattern_matches_with_whitespace(self):
        """Test that the regex matches front matter with extra whitespace."""
        content = """---


title :Example Page

chapter: true
kind: index

---

# h1 Heading"""

        match = self.pattern.match(content)
        assert match is not None
        assert "title :Example Page" in match.group(1)

    def test_metadata_pattern_no_match_without_frontmatter(self):
        """Test that the regex doesn't match content without front matter."""
        content = """# Heading
This is just regular markdown content.
"""

        match = self.pattern.match(content)
        assert match is None

    def test_metadata_pattern_no_match_incomplete_frontmatter(self):
        """Test that the regex doesn't match incomplete front matter."""
        content = """---
title: Example Page
chapter: true
# Missing closing ---

# Heading"""

        match = self.pattern.match(content)
        assert match is None

    def test_metadata_pattern_with_example_files(self):
        """Test the regex against actual example files in the project."""
        # Test with example.md
        example_file = Path(__file__).parent.parent / "examples" / "example.md"
        if example_file.exists():
            with open(example_file, "r") as f:
                content = f.read()

            match = self.pattern.match(content)
            assert match is not None, "Should match example.md front matter"

        # Test with A/_index.md
        index_file = Path(__file__).parent.parent / "examples" / "A" / "_index.md"
        if index_file.exists():
            with open(index_file, "r") as f:
                content = f.read()

            match = self.pattern.match(content)
            assert match is not None, "Should match A/_index.md front matter"

    @pytest.mark.parametrize(
        "test_content,should_match",
        [
            ("---\ntitle: Test\n---\n# Content", True),
            ("---\nkey: value\nother: data\n---\nContent", True),
            ("No front matter here", False),
            ("---\nincomplete front matter", False),
            ("", False),
        ],
    )
    def test_metadata_pattern_parametrized(self, test_content, should_match):
        """Parametrized test for various content patterns."""
        match = self.pattern.match(test_content)
        if should_match:
            assert match is not None
        else:
            assert match is None


def test_metadata_plugin_instantiation():
    """Test that MetadataPlugin can be instantiated."""
    plugin = MetadataPlugin()
    assert plugin is not None
    assert hasattr(plugin, "METADATA_PATTERN")
    assert hasattr(plugin, "stack")


if __name__ == "__main__":
    # Allow running the test file directly
    pytest.main([__file__])
