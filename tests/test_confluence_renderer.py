import pytest
from mdtocf.classes.ConfluenceRenderer import ConfluenceRenderer


@pytest.fixture
def renderer():
    return ConfluenceRenderer(confluenceUrl="https://example.atlassian.net")


class TestImage:
    def test_attached_image(self, renderer):
        result = renderer.image("alt text", "diagram.png")
        assert (
            result == '<ac:image><ri:attachment ri:filename="diagram.png" /></ac:image>'
        )

    def test_external_image(self, renderer):
        result = renderer.image("alt text", "https://example.com/img.png")
        assert (
            result
            == '<ac:image><ri:url ri:value="https://example.com/img.png" /></ac:image>'
        )

    def test_attached_image_title_ignored(self, renderer):
        result = renderer.image("alt", "file.png", title="My Title")
        assert "ri:attachment" in result
        assert "ri:filename" in result


class TestLink:
    def test_attachment_link(self, renderer):
        result = renderer.link("Download", "report.pdf")
        assert '<ri:attachment ri:filename="report.pdf"' in result
        assert "<![CDATA[Download]]>" in result
        assert "<ac:plain-text-link-body>" in result

    def test_attachment_link_no_text(self, renderer):
        result = renderer.link(None, "report.pdf")
        assert "<![CDATA[Link to a Confluence Attachment]]>" in result

    def test_external_link(self, renderer):
        result = renderer.link("Docs", "https://example.com", title="Example")
        assert '<a href="https://example.com"' in result
        assert ">Docs<" in result
        assert 'alt="Example"' in result

    def test_external_link_no_title(self, renderer):
        result = renderer.link("Click", "https://example.com")
        assert 'alt=""' in result

    def test_external_link_no_text(self, renderer):
        result = renderer.link(None, "https://example.com")
        assert ">https://example.com<" in result


class TestBlockCode:
    def test_with_language(self, renderer):
        result = renderer.block_code("print('hello')", info="python")
        assert '<ac:parameter ac:name="language">python</ac:parameter>' in result
        assert "<![CDATA[print('hello')]]>" in result
        assert '<ac:structured-macro ac:name="code">' in result

    def test_without_language(self, renderer):
        result = renderer.block_code("some code", info=None)
        assert '<ac:parameter ac:name="language"></ac:parameter>' in result

    def test_language_stripped(self, renderer):
        result = renderer.block_code("x = 1", info="  python  ")
        assert '<ac:parameter ac:name="language">python</ac:parameter>' in result

    def test_fixed_parameters_present(self, renderer):
        result = renderer.block_code("code")
        assert '<ac:parameter ac:name="title">Snippet</ac:parameter>' in result
        assert '<ac:parameter ac:name="theme">Emacs</ac:parameter>' in result
        assert '<ac:parameter ac:name="linenumbers">true</ac:parameter>' in result
        assert '<ac:parameter ac:name="firstline">0001</ac:parameter>' in result
        assert '<ac:parameter ac:name="collapse">false</ac:parameter>' in result


class TestAutoindex:
    def test_autoindex_macro(self, renderer):
        result = renderer.generate_autoindex()
        assert result == '<ac:structured-macro ac:name="children" />'
