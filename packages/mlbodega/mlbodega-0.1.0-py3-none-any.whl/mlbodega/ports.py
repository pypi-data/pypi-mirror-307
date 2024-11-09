from abc import ABC, abstractmethod
from typing import Optional

from mlbodega.schemas import Experiment
from mlbodega.schemas import Model
from mlbodega.schemas import Metric
from mlbodega.schemas import Transaction
   
class Metrics(ABC):

    @abstractmethod
    def list(self, model: Model) -> list[Metric]: ...	

    @abstractmethod
    def add(self, metric: Metric, model: Model): ...

    @abstractmethod
    def clear(self, model: Model): ...

class Transactions(ABC):

    @abstractmethod
    def put(self, transaction: Transaction, model: Model): ...

    @abstractmethod
    def list(self, model: Model) -> list[Transaction]: ...

    @abstractmethod
    def get(self, hash: str, model: Model) -> Optional[Transaction]: ...

    @abstractmethod
    def remove(self, transaction: Transaction, model: Model): ...

    @abstractmethod
    def clear(self, model: Model): ...


class Models(ABC):
    metrics: Metrics
    transactions: Transactions

    @abstractmethod
    def list(self) -> list[Model]: ...

    @abstractmethod
    def get(self, hash: str) -> Optional[Model]: ...

    @abstractmethod
    def put(self, model: Model): ...

    @abstractmethod
    def remove(self, model: Model): ...

    
class Experiments(ABC):
    @abstractmethod
    def create(self, name: str) -> Experiment: ...

    @abstractmethod
    def list(self) -> list[Experiment]: ...

    @abstractmethod
    def read(self, name: str) -> Optional[Experiment]: ...

    @abstractmethod
    def update(self, experiment: Experiment): ...

    @abstractmethod
    def delete(self, name: str): ...