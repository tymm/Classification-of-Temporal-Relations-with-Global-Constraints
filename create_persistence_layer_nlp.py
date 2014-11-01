from helper.nlp_persistence import Nlp_persistence
from TrainingSet import TrainingSet
from TestSet import TestSet
import logging
from Data import Data

# Setting up logging
logging.basicConfig(filename='creating_nlp_file.log',level=logging.DEBUG)

# Preprocessing nlp information for all relations
data = Data()

persistence = Nlp_persistence(fallback=True)
persistence.create_persistence(data.training.relations + data.test.relations)
