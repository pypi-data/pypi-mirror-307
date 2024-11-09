from typing import Optional
from tinydb import TinyDB, where
from mlbodega.ports import Models as Collection
from mlbodega.schemas import Model, Experiment
from mlbodega.tinydb.metrics import Metrics
from mlbodega.tinydb.transactions import Transactions

class Models(Collection):
    def __init__(self, location: str, experiment: Experiment):
        self.db = TinyDB(f'{location}/database.json')
        self.metrics = Metrics(location)
        self.transactions = Transactions(location)
        self.table = self.db.table(f'models')
        self.key = str(experiment.id)
    
    def put(self, model: Model):
        self.table.upsert({**model.dump(), 'key': self.key}, where('hash') == model.hash)

    def get(self, hash: str) -> Optional[Model]:
        result = self.table.get((where('hash') == hash) & (where('key') == self.key))
        if result is None:
            return None
        return Model(**{key: value for key, value in result.items() if key != 'key'})
    
    def list(self) -> list[Model]:
        results = self.table.search(where('key') == self.key)
        return [Model(**{key: value for key, value in result.items() if key != 'key'}) for result in results]
    
    def remove(self, model: Model):
        self.table.remove((where('hash') == model.hash) & (where('key') == self.key))
        self.metrics.clear(model)
        
        