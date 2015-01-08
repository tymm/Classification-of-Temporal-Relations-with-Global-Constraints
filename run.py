from Data import Data
from System import System

# Create data
data = Data()
system = System(data)

# Create features and apply feature selection
system.use_all_features()
system.use_feature_selection()
system.create_features()

# Train classifiers and save them to pickle file
system.train()
# Save classifiers to pickle file
system.save_classifiers()

# Run pairwise classification
event_event, event_timex = system.eval()
print "Event-Event:"
print event_event
print "Event-Timex:"
print event_timex

# Create output tml files for evaluation script
system.save_predictions_to_relations()
data.test.create_evaluation_files()
