from helper.nlp_persistence import Nlp_persistence
from TrainingSet import TrainingSet
import logging

# Setting up logging
logging.basicConfig(filename='creating_nlp_file.log',level=logging.DEBUG)

# Preprocessing nlp information for all relations
training = TrainingSet(False, "data/training/TE3-Silver-data/AFP_ENG_19970401.0006.tml")

persistence = Nlp_persistence()
persistence.create_persistence(training.relations)
