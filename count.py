from Data import Data
from Feature import Feature
from helper.nlp_persistence import Nlp_persistence
from helper.duration_cache import Duration_cache
import cPickle as pickle

if __name__ == "__main__":
    data = Data()

    count = 0

    for text_obj in data.training.text_objects:
        for relation in text_obj.relations:
            if relation.is_event_event() or relation.is_event_timex():
                count += 1

    print "# relations: " + str(count)

    nlp_persistence_obj = Nlp_persistence()
    nlp_persistence_obj.load()
    strings_cache = pickle.load(open("strings.p", "rb"))
    duration_cache = Duration_cache()

    f = Feature(data.training.text_objects[0].relations[0], strings_cache, nlp_persistence_obj, duration_cache, "all")
    feature = f.get_feature()

    print "feature length: " + str(feature.shape)
