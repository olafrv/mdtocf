class MetadataPlugin():

    stack = { 'title' : None }

    METADATA_PATTERN = (
        r'---\s*\ntitle\s*:([\s\S]+)\n---'
    )

    def parse_metadata(self, parser, match, state):
        title = match.group(1).strip()
        self.stack['title'] = title
        return 'metadata', title

    def render_html_metadata(self, title):
        #print(f'title: {title}')
        #return f'<h1>{title}</h1>'
        return ''

    def plugin_metadata(self, md):
        md.inline.register_rule('metadata', self.METADATA_PATTERN, self.parse_metadata)
        md.inline.rules.append('metadata')
        if md.renderer.NAME == 'html':
            md.renderer.register('metadata', self.render_html_metadata)
