from Data import Data
import cPickle as pickle

if __name__ == "__main__":
    data = Data()
    strings = set()

    for text_obj in data.training.text_objects:
        for relation in text_obj.relations:
            strings.add(relation.source.text)
            strings.add(relation.target.text)

    pickle.dump(strings, open("strings.p", "wb"))
