"""Mistune v2 Plugin for Reading Markdown Metadata

Used by ConfluenceRenderer to enable the parsing of page title,
later used for setting the page tile using Confluence API.

"""
import re


class MetadataPlugin():

    stack = {'title': None}  # Used by ConfluenceRenderer

    METADATA_PATTERN = re.compile((
        r'(?:---)'
        r'((?:\s+)([a-z]+ *:[ \S]+(?:\s+))+)'
        r'(?:---)'
    ), flags=re.M | re.I)

    def parse_metadata(self, parser, match, state):
        lines = match.group(1).split("\n")
        non_empty_lines = [line for line in lines if line.strip() != ""]
        for line in non_empty_lines:
            if line != '':
                key, value = line.split(':')
                if (key.strip()) == 'title':
                    title = value.strip()
                    self.stack['title'] = title

        return {'type': 'newline', 'blank': True}  # Return just line break

    def render_html_metadata(self, title):
        return ''  # No xhtml page content, just extracting page title

    def plugin_metadata(self, md):
        md.block.register_rule(
            'metadata', self.METADATA_PATTERN, self.parse_metadata)
        md.block.rules.append('metadata')
        if md.renderer.NAME == 'html':
            md.renderer.register(
                'metadata', self.render_html_metadata)
