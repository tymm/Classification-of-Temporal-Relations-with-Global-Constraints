from helper.nlp_persistence import Nlp_persistence
from TrainingSet import TrainingSet
import logging

# Setting up logging
logging.basicConfig(filename='creating_nlp_file.log',level=logging.DEBUG)

# Preprocessing nlp information for all relations
training = TrainingSet(True, True, "data/training/TBAQ-cleaned/AQUAINT/", "data/training/TBAQ-cleaned/TimeBank/", "data/test/te3-platinum/")

with Nlp_persistence(fallback=True) as persistence:
    persistence.load()
    persistence.create_persistence(training.relations)
