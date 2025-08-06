"""Mistune v2 renderer for Confluence Storage Format (XHTML)

Used by ConfluencePublisher class to parse Markdown using
mistune v2 and convert it to Confluence XHTML Storage Format.

"""

import mistune


class ConfluenceRenderer(mistune.HTMLRenderer):

    def __init__(self, confluenceUrl=None):
        self.confluenceUrl = confluenceUrl
        super().__init__()

    def image(self, text, url, title=None):
        if url.find("/") == -1:
            # Attached Image
            return (
                "<ac:image>"
                + '<ri:attachment ri:filename="'
                + url
                + '" />'
                + "</ac:image>"
            )
        else:
            # External Image
            return '<ac:image><ri:url ri:value="' + url + '" /></ac:image>'

    def link(self, text, url, title=None):
        if url.find("/") == -1:
            return (
                '\n<ac:link><ri:attachment ri:filename="'
                + url
                + '" />'
                + "<ac:plain-text-link-body>"
                + "<![CDATA["
                + (text if text is not None else "Link to a Confluence Attachment")
                + "]]>"
                + "</ac:plain-text-link-body>"
                + "</ac:link>\n"
            )
        else:
            return (
                '<a href="'
                + url
                + '" alt="'
                + (title if title is not None else "")
                + '">'
                + (text if text is not None else url)
                + "</a>"
            )

    def block_code(self, code, info=None):
        return (
            '\n<ac:structured-macro ac:name="code">'
            + '<ac:parameter ac:name="title">Snippet</ac:parameter>'
            + '<ac:parameter ac:name="theme">Emacs</ac:parameter>'
            + '<ac:parameter ac:name="linenumbers">true</ac:parameter>'
            + '<ac:parameter ac:name="language">'
            + (info.strip() if info is not None else "")
            + "</ac:parameter>"
            + '<ac:parameter ac:name="firstline">0001</ac:parameter>'
            + '<ac:parameter ac:name="collapse">false</ac:parameter>'
            + "<ac:plain-text-body><![CDATA["
            + code
            + "]]></ac:plain-text-body>"
            + "</ac:structured-macro>\n"
        )

    def generate_autoindex(self):
        return '<ac:structured-macro ac:name="children" />'
