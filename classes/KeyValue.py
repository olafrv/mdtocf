import os
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
        return self.db.get(key)

    def save(self, key, value):
        self.db.set(key, value)

    def remove(self, key):
        self.db.rem(key)

    def sha256(self, value):
        h = hashlib.sha256(value.encode())
        return h.hexdigest()

