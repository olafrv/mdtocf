import os
import json
import hashlib
import pickledb

class KeyValue():
    def __init__(self, dbPath):
        self.db = pickledb.load(dbPath, False)

    def __del__(self):
        self.db.dump()

    def keys(self):
        return [*self.db.getall()]

    def load(self, key):
        value = self.db.get(key)
        if value == False:
            return { 'id' : None, 'title': '', 'sha256': '' }
        else:
            return json.loads(value)

    def save(self, key, value):
        self.db.set(key, json.dumps(value))

    def remove(self, key):
        self.db.rem(key)

    def sha256(self, value):
        h = hashlib.sha256(value.encode())
        return h.hexdigest()

