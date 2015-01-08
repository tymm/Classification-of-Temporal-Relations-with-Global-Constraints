from Data import Data
from System import System

data = Data()
system = System(data)

# Create features and apply feature selection
system.use_all_features()
system.use_feature_selection()
system.create_features()

# Train classifiers and save them to pickle file
system.train()
system.save_classifiers()

# Run pairwise classification
event_event, event_timex = system.eval()
print "Event-Event:"
print event_event
print "Event-Timex:"
print event_timex

# Run global model
system.create_confidence_scores()
system.apply_global_model()

event_event, event_timex = system.eval_global_model()
print "Event-Event:"
print event_event
print "Event-Timex:"
print event_timex

# Create output tml files for evaluation script
data.test.create_evaluation_files()
