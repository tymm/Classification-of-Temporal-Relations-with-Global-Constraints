from helper.nlp_persistence import Nlp_persistence
from TrainingSet import TrainingSet
import logging

# Setting up logging
logging.basicConfig(filename='creating_nlp_file.log',level=logging.DEBUG)

# Preprocessing nlp information for all relations
training = TrainingSet(load, "data/training/TE3-Silver-data/", "data/training/TBAQ-cleaned/AQUAINT/", "data/training/TBAQ-cleaned/TimeBank/", "data/test/te3-platinum/")

persistence = Nlp_persistence()
persistence.create_persistence(training.relations)
