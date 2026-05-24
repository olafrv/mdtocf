"""Mistune v3 Plugin for Reading Markdown Metadata

Used by ConfluencePublisher to extract page title from YAML front matter
and strip it from the markdown before rendering.

"""

import re


class MetadataPlugin:

    METADATA_PATTERN = re.compile(
        (r"(?:---)" r"((?:\s+)([a-z]+ *:[ \S]+(?:\s+))+)" r"(?:---)"), flags=re.M | re.I
    )

    def extract(self, markdown):
        """Return (metadata_dict, stripped_markdown).

        Strips the YAML front matter block from markdown and parses its
        key/value pairs. Returns an empty dict and the original markdown
        unchanged if no front matter is found.
        """
        match = self.METADATA_PATTERN.match(markdown)
        if not match:
            return {}, markdown

        metadata = {}
        for line in match.group(1).split("\n"):
            line = line.strip()
            if line:
                key, value = line.split(":", 1)
                metadata[key.strip().lower()] = value.strip()

        stripped = markdown[match.end():].lstrip("\n")
        return metadata, stripped
