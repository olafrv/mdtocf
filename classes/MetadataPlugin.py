"""Mistune v2 Plugin for Reading Markdown Metadata

Used by ConfluenceRenderer to enable the parsing of page title,
later used for setting the page tile using Confluence API.

"""
class MetadataPlugin():

    stack = { 'title' : None } # Used by ConfluenceRenderer to get and set the Page Title

    METADATA_PATTERN = (
        #---
        #title : Title of the Page (Markdown file)
        #---
        r'---\s*\ntitle\s*:([\s\S]+)\n---' 
    )

    def parse_metadata(self, parser, match, state):
        title = match.group(1).strip()
        self.stack['title'] = title
        return 'metadata', title

    def render_html_metadata(self, title):
        return '' # Not used in xhtml page content but for setting the page in Confluence API

    def plugin_metadata(self, md):
        md.inline.register_rule('metadata', self.METADATA_PATTERN, self.parse_metadata)
        md.inline.rules.append('metadata')
        if md.renderer.NAME == 'html':
            md.renderer.register('metadata', self.render_html_metadata)
