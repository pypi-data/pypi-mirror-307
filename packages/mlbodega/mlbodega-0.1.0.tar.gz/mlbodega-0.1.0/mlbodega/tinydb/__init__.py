from mlbodega.tinydb.experiments import Experiments
from mlbodega.tinydb.models import Models

def get_experiments(database_location: str):
    return Experiments(database_location)

def get_models(experiment_name: str, database_location: str):
    experiments = Experiments(database_location)
    experiment = experiments.read(experiment)
    if experiment is None:
        experiment = experiments.create(experiment_name)
    return Models(database_location, experiment)
    
