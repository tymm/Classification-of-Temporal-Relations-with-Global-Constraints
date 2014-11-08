from Data import Data
import cPickle as pickle
from helper.nlp_persistence import Nlp_persistence

def get_lemma(entity):
    lemma = nlp_persistence_obj.get_lemma_for_word(entity.sentence, entity.text)
    return lemma

if __name__ == "__main__":
    data = Data()
    nlp_persistence_obj = Nlp_persistence(fallback=True)
    nlp_persistence_obj.load()

    tokens = set()
    lemmas = set()

    for text_obj in data.training.text_objects:
        for relation in text_obj.relations:
            tokens.add(relation.source.text.lower())
            tokens.add(relation.target.text.lower())

            lemmas.add(get_lemma(relation.source))
            lemmas.add(get_lemma(relation.target))

    pickle.dump((tokens, lemmas), open("strings.p", "wb"))
