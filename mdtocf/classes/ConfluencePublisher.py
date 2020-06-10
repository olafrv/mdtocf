""" Confluence Publisher

Encapsulate the logic of processing a markdown directory tree.

"""
import os
import mistune
from .MetadataPlugin import MetadataPlugin
from .ConfluenceRenderer import ConfluenceRenderer
from .KeyValue import KeyValue
from atlassian import Confluence
from atlassian.confluence import ApiError
from requests import HTTPError


class ConfluencePublisher():

    def __init__(
        self, url, username, apiToken,
        pageTitlePrefix, markdownDir, dbPath, space, parentPageId,
        forceUpdate=False, forceDelete=False, skipUpdate=False,
    ):
        self.api = Confluence(url=url, username=username, password=apiToken)
        self.pageTitlePrefix = pageTitlePrefix
        self.markdownDir = markdownDir
        self.kv = KeyValue(dbPath)
        self.space = space
        self.parentPageId = parentPageId
        self.forceUpdate = forceUpdate
        self.forceDelete = forceDelete
        self.skipUpdate = skipUpdate
        self.confluenceRenderer = ConfluenceRenderer(url)
        self.metadataPlugin = MetadataPlugin()
        self.renderer = mistune.create_markdown(
            renderer=self.confluenceRenderer,
            plugins=['strikethrough', 'footnotes', 'table', 'url',
                     self.metadataPlugin.plugin_metadata]
        )

        # Hack to allow metadata plugin to work (See mistune/block_parser.py)
        self.renderer.block.rules.remove('thematic_break')

    def __getFileContent(self, filepath):
        file = open(filepath, mode='r')
        content = file.read()
        file.close()
        return content

    def __updatePage(self, space, parentId, filepath, autoindex=False):

        if autoindex:
            markdown = ''
        else:
            markdown = self.__getFileContent(filepath)

        metadata = self.kv.load(filepath)

        currentTitle = metadata['title']
        currentHash = metadata['sha256']
        hash = self.kv.sha256(markdown)

        # --- Render (BEGIN)
        self.metadataPlugin.stack['title'] = None

        if autoindex:
            body = self.confluenceRenderer.generate_autoindex()
        else:
            body = self.renderer(markdown)

        if self.metadataPlugin.stack['title'] is None:
            if autoindex:
                title = 'Folder ' + os.path.basename(os.path.dirname(filepath))
            else:
                title = os.path.basename(filepath)
        else:
            title = self.metadataPlugin.stack['title']

        title = self.pageTitlePrefix + title
        # >>> Removed: + " [" + self.kv.sha256(filepath)[-6:] + "]"
        # --- Render (END)

        if currentTitle and currentTitle != title:
            print('REN => Title: ' + title)
            pageId = self.api.get_page_id(space, currentTitle)
            self.api.update_page(pageId, title, body)

        if currentHash != hash or self.forceUpdate:
            if autoindex:
                print('IDX => Title: ' + title)
            else:
                print('UPD => Title: ' + title)

            if self.api.update_or_create(
                parent_id=parentId,
                title=title,
                body=body,
                representation='storage'
            ):
                id = self.api.get_page_id(space, title)
                self.kv.save(filepath,
                             {'id': id, 'title': title, 'sha256': hash})
                return id
            else:
                return None
        else:
            print('SKP => Title: ' + title)
            return self.api.get_page_id(space, title)

    def __deleteAttachment(self, filepath):
        metadata = self.kv.load(filepath)
        filename = os.path.basename(filepath)
        if metadata['id']:
            try:
                print('DEL Att. => Title: ' + filename)        
                # https://confluence.atlassian.com/confkb/confluence-rest-api-lacks-delete-method-for-attachments-715361922.html
                # self.api.delete_attachment_by_id(metadata['id'], 1)
                self.api.remove_content(metadata['id'])
            except (HTTPError, ApiError):
                pass

    def __updateAttachment(self, space, pageId, filepath):
        filename = os.path.basename(filepath)

        print('UPD Att. => Title: ' + filename)
        results = self.api.attach_file(filepath,
                                       name=filename,
                                       page_id=pageId,
                                       space=space)
        id = results['id'] if 'id' in results else results['results'][0]['id']
        self.kv.save(filepath, {'id': id, 'title': filename, 'sha256': None})
        return id

    def __publishRecursive(self, space, parentId, path):
        # File: _index.md
        indexParentId = parentId
        indexPath = path + os.sep + '_index.md'
        if os.path.isfile(indexPath):
            # Use local _index.md file
            indexParentId = self.__updatePage(space, parentId, indexPath)
        else:
            # Autoindex simulate _index.md in Confluence if missing locally
            # Except for (root) parentPageId because missing in markdownDir!
            if parentId != self.parentPageId:
                indexParentId = self.__updatePage(
                    space, parentId, indexPath, True)

        # Directories: */
        for f in os.scandir(path):
            if f.is_dir():
                self.__publishRecursive(space, indexParentId, f.path)

        # Files: *.* (Except _index.md)
        for f in os.scandir(path):
            if f.is_file():
                if f.path.endswith(".md"):
                    if not f.path.endswith(os.sep + '_index.md'):
                        self.__updatePage(space, indexParentId, f.path)
                else:
                    self.__deleteAttachment(f.path)
                    self.__updateAttachment(space, indexParentId, f.path)

    def delete(self):
        for filepath in sorted(self.kv.keys()):
            metadata = self.kv.load(filepath)

            # Page has Sub-pages (Childs)?
            indexWithChilds = False
            if filepath.endswith('_index.md'):
                childs = 0
                if os.path.isdir(os.path.dirname(filepath)):
                    for f in os.scandir(os.path.dirname(filepath)):
                        if f.path.endswith(".md") and \
                           not f.path.endswith('_index.md'):
                            childs = childs + 1
                indexWithChilds = childs > 0

            if self.forceDelete \
               or (not os.path.isfile(filepath) and not indexWithChilds):
                print('DEL => Id: '
                      + metadata['id'] + ', Title: ' + metadata['title'])
                if filepath.endswith(".md"):
                    try:
                        if self.api.get_page_by_id(metadata['id']):
                            self.api.remove_page(metadata['id'])
                    except HTTPError as ex:
                        code = ex.response.status_code
                        if code != 404:
                            print("DEL Pag. (Error):" + str(code))
                        else:
                            pass
                else:
                    self.__deleteAttachment(filepath)

                self.kv.remove(filepath)

    def publish(self):
        self.__publishRecursive(
            self.space, self.parentPageId, self.markdownDir)
