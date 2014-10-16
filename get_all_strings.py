from Data import Data
import cPickle as pickle

if __name__ == "__main__":
    data = Data()
    strings = set()

    for text_obj in data.training.text_objects:
        for relation in text_obj.relations:
            strings.add(relation.source.text.lower())
            strings.add(relation.target.text.lower())

    pickle.dump(strings, open("strings.p", "wb"))
