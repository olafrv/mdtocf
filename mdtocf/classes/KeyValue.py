"""Key-Value Store Used for Caching

Used by ConfluencePublisher to save metadata related to the processing
of each markdown file, like: Confluence Page ID, Confluence Page Title
and XHTML Confluence Content SHA256.

"""

import json
import hashlib
from pickledb import PickleDB


class KeyValue:

    def __init__(self, dbPath):
        self.db = PickleDB(dbPath)

    def keys(self):
        return [*self.db.all()]

    def load(self, key):
        value = self.db.get(key)
        if value is None:
            return {"id": None, "title": "", "sha256": ""}
        else:
            return json.loads(value)

    def save(self, key, value):
        self.db.set(key, json.dumps(value))
        self.db.save()

    def remove(self, key):
        self.db.remove(key)
        self.db.save()

    def sha256(self, value):
        h = hashlib.sha256(value.encode())
        return h.hexdigest()
