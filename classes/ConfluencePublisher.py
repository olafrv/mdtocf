""" Confluence Publisher

Encapsulate the logic of processing a markdown directory tree.

"""
import os
import json
import mistune
from classes.MetadataPlugin import MetadataPlugin
from classes.ConfluenceRenderer import ConfluenceRenderer
from classes.KeyValue import KeyValue
from atlassian import Confluence

class ConfluencePublisher():

    def __init__(
        self, url, username, apiToken, 
        markdownDir, dbPath, space, parentPageId, 
        forceUpdate=False, forceDelete=False, skipUpdate=False, 
    ):
        self.api = Confluence(url=url, username=username, password=apiToken)
        self.markdownDir = markdownDir
        self.kv = KeyValue(dbPath)
        self.space = space
        self.parentPageId = parentPageId
        self.forceUpdate = forceUpdate
        self.forceDelete = forceDelete
        self.skipUpdate = skipUpdate
        self.metadataPlugin = MetadataPlugin()
        self.renderer = mistune.create_markdown(
            renderer=ConfluenceRenderer(url),
            plugins=['strikethrough','footnotes','table','url', self.metadataPlugin.plugin_metadata]
        ) 
        # Hack to allow metadata plugin to work (See mistune/block_parser.py)
        self.renderer.block.rules.remove('thematic_break') 

    def __getFileContent(self, filepath):
        file = open(filepath,mode='r')
        content = file.read()
        file.close()
        return content

    def __updatePage(self, space, parentId, filepath):
        markdown = self.__getFileContent(filepath)

        hashOld = self.kv.load(filepath)['sha256'] 
        hashNew = self.kv.sha256(markdown)

        # --- Render (BEGIN)
        self.metadataPlugin.stack['title'] = None
        body = self.renderer(markdown)
        if self.metadataPlugin.stack['title'] == None:
            title = os.path.basename(filepath) 
        else:
            title = self.metadataPlugin.stack['title']
        # --- Render (END)

        title = title + " [" + self.kv.sha256(filepath)[-6:] + "]"

        if hashOld != hashNew or self.forceUpdate:
            print('UPD => Page Title: ' + title)
            if self.api.update_or_create(
                parent_id=parentId, 
                title=title, 
                body=body, 
                representation='storage'
            ):
                id = self.api.get_page_id(space, title)
                self.kv.save(filepath, {'id': id, 'title': title , 'sha256': hashNew } )
                return id
            else:
                return None
        else:
            print('SKP => Page Title: ' + title)
            return self.api.get_page_id(space, title)

    def __publishRecursive(self, space, parentId, path):
        # Files: _index.md
        indexParentId = parentId
        indexPath = path + os.sep + '_index.md'
        if os.path.isfile(indexPath):
            indexParentId = self.__updatePage(space, parentId, indexPath)

        # Directories: */
        for f in os.scandir(path):
            if f.is_dir():
                self.__publishRecursive(space, indexParentId, f.path)

        # Files: *.md (Except _index.md)
        for f in os.scandir(path):
            if f.path.endswith(".md") and not f.path.endswith('_index.md'):
                self.__updatePage(space, indexParentId, f.path)

    def delete(self):
        for filepath in sorted(self.kv.keys()):
            if not os.path.isfile(filepath) or self.forceDelete:
                metadata = self.kv.load(filepath) 
                print('DEL => Id: ' + metadata['id'] + ', Title: ' + metadata['title'])
                if self.api.get_page_id(self.space, metadata['title']):
                    self.api.remove_page(metadata['id'])
                self.kv.remove(filepath)

    def publish(self):
        self.__publishRecursive(self.space, self.parentPageId, self.markdownDir)
