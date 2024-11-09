from uuid import UUID
from typing import Any
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class Schema:
    def dump(self):
        return asdict(self)

@dataclass
class Metric(Schema):
    name: str
    value: Any
    batch: int
    epoch: int
    phase: str

@dataclass
class Experiment(Schema):
    id: Any
    name: str

@dataclass
class Model(Schema):
    id: Any
    hash: str
    name: str
    epochs: int
    parameters: dict[str, Any]    

@dataclass
class Criterion(Schema):
    hash: str
    name: str
    parameters: dict[str, Any]
    

@dataclass
class Optimizer(Schema):
    hash: str
    name: str
    parameters: dict[str, Any]

@dataclass
class Dataset(Schema):
    hash: str
    name: str
    parameters: dict[str, Any]

@dataclass
class Iteration(Schema):
    phase: str
    dataset: Dataset
    parameters: dict[str, Any]
    
@dataclass
class Transaction(Schema):
    epochs: tuple[int, int]
    hash: str
    start: datetime
    end: datetime
    criterion: Criterion
    optimizer: Optimizer
    iterations: list[Iteration]