from Data import Data
from System import System

data = Data()
system = System(data)

system.use_token()
system.use_lemma()
system.use_dependency_is_root()
system.use_dependency_order()
system.use_aspect()
system.use_tense()
system.use_same_tense()
system.use_same_aspect()
system.use_dependency_type()

system.use_dct()
system.use_type()
system.use_value()
system.use_same_polarity()
system.use_polarity()
system.use_class()
system.use_entity_distance()
system.use_textual_order()
system.use_duration()
system.use_duration_difference()
system.use_same_pos()
system.use_pos()
system.use_duration()
system.use_temporal_signal()

system.create_features()
system.train()

event_event, event_timex = system.eval()
print "Event-Event:"
print event_event
print "Event-Timex:"
print event_timex
