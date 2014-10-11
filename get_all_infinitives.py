from nltk.stem.wordnet import WordNetLemmatizer
from Data import Data
from helper.nlp_persistence import Nlp_persistence
from helper.nlp_persistence import CouldNotFindGoverningVerb
from parsexml.event import Event
import cPickle as pickle

data = Data()
nlp_persistence_obj = Nlp_persistence()
nlp_persistence_obj.load()
lemmatizer = WordNetLemmatizer()

infinitive_verb = {}

def _get_verb(event):
    if event.pos_xml == "NOUN" or event.pos_xml == "ADJECTIVE" or event.pos_xml == "PREPOSITION" or event.pos_xml == "PREP":
        # Get governing verb
        governing_verb = nlp_persistence_obj.get_governing_verb(event)[0]

        return governing_verb.lower()
    else:
        return event.text.lower()

def add(verb, infinitive):
    infinitive_verb.update({verb: infinitive})

if __name__ == "__main__":
    for text_obj in data.training.text_objects + data.test.text_objects:
        for relation in text_obj.relations:
            if type(relation.source) == Event:
                try:
                    verb = _get_verb(relation.source)
                except CouldNotFindGoverningVerb:
                    continue

                infinitive = lemmatizer.lemmatize(verb, 'v')
                add(verb, infinitive)

            if type(relation.target) == Event:
                try:
                    verb = _get_verb(relation.target)
                except CouldNotFindGoverningVerb:
                    continue

                infinitive = lemmatizer.lemmatize(verb, 'v')
                add(verb, infinitive)

    pickle.dump(infinitive_verb, open("infinitives.p", "wb"), protocol=-1)
