from helper.nlp_persistence import Nlp_persistence
from TrainingSet import TrainingSet

# Preprocessing nlp information for all relations
training = TrainingSet(False, "data/training/TE3-Silver-data/", "data/training/TBAQ-cleaned/AQUAINT/", "data/training/TBAQ-cleaned/TimeBank/", "data/test/te3-platinum/")

persistence = Nlp_persistence()
persistence.create_persistence(training.relations)
