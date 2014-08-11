from nltk.stem.wordnet import WordNetLemmatizer
from parsexml.event import Event

class Lemma:
    def __init__(self, training_set):
        self.lemmatizer = WordNetLemmatizer()

        self.lemmas = self._get_all_lemmas(training_set)

    def get_index(self, word):
        lemma = self._get_lemma(word.lower())

        try:
            index = self.lemmas.index(lemma)
        except ValueError:
            return None

    def get_length(self):
        return len(self.lemmas)

    def _get_all_lemmas(self, training_set):
        lemmas = set()

        # Getting all lemmas
        for text_obj in training_set.text_objects:
            for relation in text_obj.relations:
                # TODO: Does it make sense to not use Timex?
                if type(relation.source) == Event:
                    lemmas.add(self._get_lemma(relation.source.text))
                if type(relation.target) == Event:
                    lemmas.add(self._get_lemma(relation.target.text))

        return list(lemmas)

    def _get_lemma(self, text):
        text = text.lower()
        # http://stackoverflow.com/questions/771918/how-do-i-do-word-stemming-or-lemmatization
        # Assumption: Just assume text is a verb
        return self.lemmatizer.lemmatize(text, 'v')
