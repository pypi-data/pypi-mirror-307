from os import path, makedirs
from typing import Optional
from tinydb import TinyDB, where
from mlbodega.schemas import Transaction, Model
from mlbodega.ports import Transactions as Collection

class Transactions(Collection):
    def __init__(self, location: str):
        if not path.exists(location):
            makedirs(location)
        self.db = TinyDB(f'{location}/database.json')
        self.table = self.db.table('transactions')

    def put(self, transaction: Transaction, model: Model):
        self.table.upsert({**transaction.dump(), 'model': model.hash}, where('hash') == transaction.hash)

    def list(self, model: Model) -> list[Transaction]:
        results = self.table.search(where('model') == model.hash)
        return [Transaction(**{key: value for key, value in result.items() if key != 'model'}) for result in results]
    
    def get(self, hash: str, model: Model) -> Optional[Transaction]:
        result = self.table.get((where('hash') == hash) & (where('model') == model.hash))
        if result is None:
            return None
        return Transaction(**{key: value for key, value in result.items() if key != 'model'})
    
    def remove(self, transaction: Transaction, model: Model):
        self.table.remove((where('hash') == transaction.hash) & (where('model') == model.hash))
    
    def clear(self, model: Model):
        self.table.remove(where('model') == model.hash)