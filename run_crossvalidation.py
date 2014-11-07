from Data import Data
from System import System

data = Data()
system = System(data)

system.use_best_feature_set()

system.create_features()
system.cross_validation()

print system.crossval_accuracy_event_event
print system.crossval_accuracy_event_timex
