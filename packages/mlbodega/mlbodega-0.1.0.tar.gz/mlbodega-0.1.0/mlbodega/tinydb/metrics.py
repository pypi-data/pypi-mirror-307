from os import makedirs, path
from tinydb import TinyDB
from tinydb import where
from mlbodega.ports import Metrics as Collection
from mlbodega.schemas import Metric, Model

class Metrics(Collection):
    def __init__(self, location: str):
        if not path.exists(location):
            makedirs(location)
        self.db = TinyDB(f'{location}/database.json')
        self.table = self.db.table('metrics')
    
    def add(self, metric: Metric, model: Model):
        self.table.insert({**metric.dump(), 'model': model.hash})   

    def list(self, model: Model) -> list[Metric]:
        results = self.table.search(where('model') == model.hash)
        return [Metric(**{key: value for key, value in result.items() if key != 'model'}) for result in results]
    
    def clear(self, model: Model):
        self.table.remove(where('model') == model.hash)