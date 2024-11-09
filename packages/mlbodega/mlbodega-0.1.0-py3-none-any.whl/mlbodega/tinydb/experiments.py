from os import path, makedirs
from uuid import uuid4
from typing import Optional
from tinydb import TinyDB, where
from mlbodega.ports import Experiments as Collection
from mlbodega.schemas import Experiment

class Experiments(Collection):
    def __init__(self, location: str):
        if not path.exists(location):
            makedirs(location)
        self.db = TinyDB(f'{location}/database.json')
        self.table = self.db.table('experiments')

    def read(self, name: str) -> Optional[Experiment]:
        result = self.table.get(where('name') == name)
        return Experiment(id=result['id'], name=result['name']) if result else None
    
    def create(self, name: str) -> Experiment:
        result = self.table.get(where('name') == name)
        if result:
            raise ValueError(f'Experiment with name {name} already exists')
        id = uuid4()
        self.table.insert({'id': str(id), 'name': name})
        return Experiment(id=id, name=name)

    def update(self, experiment: Experiment):
        self.table.update({'name': experiment.name}, where('id') == str(experiment.id))

    def delete(self, name: str):
        self.table.remove(where('name') == name)
    
    def list(self) -> list[Experiment]:
        return [Experiment(id=result['id'], name=result['name']) for result in self.table.all()]