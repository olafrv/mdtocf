import os
import mistune
from .KeyValue import KeyValue
from .ConfluenceRenderer import ConfluenceRenderer
from atlassian import Confluence

class ConfluencePublisher():

    def __init__(self, url, username, apiToken, markdownDir, dbPath, space, parentPageId):
        self.api = Confluence(url=url, username=username, password=apiToken)
        self.markdownDir = markdownDir
        self.space = space
        self.parentPageId = parentPageId
        self.kv = KeyValue(dbPath)
        self.renderer = mistune.create_markdown(
            renderer=ConfluenceRenderer(url),
            plugins=['strikethrough','footnotes','table','url']) 
        
    def __getFileContent(self, filepath):
        file = open(filepath,mode='r')
        content = file.read()
        file.close()
        return content

    def __hashChanged(self, filepath):
        hashOld = self.kv.load(filepath)
        hashNew = self.kv.sha256(self.__getFileContent(filepath))
        return hashOld != hashNew

    def __saveHash(self, filepath):
        hash = self.kv.sha256(self.__getFileContent(filepath))
        self.kv.save(filepath, hash)
        return hash

    def __removeHash(self, filepath):
        self.kv.remove(filepath)
        return hash

    def getStorageFormat(self, filepath):
        return self.renderer(self.__getFileContent(filepath))

    def __getPageTitle(self, filepath):
        return os.path.basename(filepath) + " [" + self.kv.sha256(filepath)[-6:] + "]"

    def __updatePage(self, space, parentId, filepath):
        title = self.__getPageTitle(filepath)
        if self.api.update_or_create(
            parent_id=parentId, 
            title=title, 
            body=self.getStorageFormat(filepath), 
            representation='storage'):
            self.__saveHash(filepath)
            return self.api.get_page_id(space, title)
        else:
            return None

    def delete(self):
        for filepath in sorted(self.kv.keys()):
            if not os.path.isfile(filepath):
                print("DEL: " + filepath)
                title = self.__getPageTitle(filepath)
                pageId = self.api.get_page_id(self.space, title)
                if pageId != None: self.api.remove_page(pageId)
                self.__removeHash(filepath)

    def publish(self):
        self.__publishRecursive(self.space, self.parentPageId, self.markdownDir)

    def __publishRecursive(self, space, parentId, path):
        # Directories: */
        for f in os.scandir(path):
            if f.is_dir():
                print(f.path)
                self.__publishRecursive(space, parentId, f.path)
        
        # Files: _index.md
        indexPath = path + os.sep + '_index.md'
        indexParentId = parentId
        if os.path.isfile(indexPath):
            print(indexPath)
            if self.__hashChanged(indexPath):
                indexParentId = self.__updatePage(space, parentId, indexPath)
            else:
                title = self.__getPageTitle(indexPath)
                indexParentId = self.api.get_page_id(space, title)                

        # Files: *.md (Except _index.md)
        for f in os.scandir(path):
            if f.path.endswith(".md") and not f.path.endswith('_index.md'):
                print(f.path)
                if self.__hashChanged(f.path):
                    updated = self.__updatePage(space, indexParentId, f.path)
                    if updated == None: print("Unable to update: " + f.path)
