import re
from nltk.stem.wordnet import WordNetLemmatizer

class Duration:
    def __init__(self):
        self.FILE = "event.lexicon.distributions"
        self.durations = ["seconds", "minutes", "hours", "days", "weeks", "months", "years", "decades"]

    def _get_most_likely_duration(self, verb, obj=None):
        infinitive = self._get_infinitive(verb)

        if obj:
            # Searching for verb and object
            for line in open(self.FILE, "r"):
                if infinitive.lower() in line and obj.lower() in line:
                    # We found the line we are searching for
                    index = self._get_duration_from_line(line)
                    return self.durations[index]

        else:
            # Searching only for verb
            for line in open(self.FILE, "r"):
                if infinitive.lower() in line and "OBJ" not in line:
                    # We found the line which only has the verb and no object
                    index = self._get_duration_from_line(line)
                    return self.durations[index]

        return None

    def _get_infinitive(self, verb):
        lemmatizer = WordNetLemmatizer()
        infinitive = lemmatizer.lemmatize(verb, 'v')

        return infinitive

    def _get_duration_from_line(self, line):
        m = re.search(r"DISTR\=\[(.*)\]$", line)
        if m:
            probas = m.group(1)
            probas = probas.strip(";").split(";")

            max = 0
            for proba in probas:
                if float(proba) > float(max):
                    max = proba

            index_proba = probas.index(max)

            return index_proba
        else:
            return None

