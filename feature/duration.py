import re
from nltk.stem.wordnet import WordNetLemmatizer
from parsexml.event import Event
from parsexml.timex import Timex

class Duration:
    def __init__(self, nlp_persistence_obj):
        self.FILE = "event.lexicon.distributions"
        self.nlp_persistence_obj = nlp_persistence_obj
        self.durations = ["seconds", "minutes", "hours", "days", "weeks", "months", "years", "decades"]

    def get_duration(self, entity):
        if type(entity) is Event:
            return self._get_event_duration(entity)
        elif type(entity) is Timex:
            return self._get_timex_duration(entity)

    def _get_event_duration(self, event):
        if event.pos_xml == "NOUN" or event.pos_xml == "ADJECTIVE" or event.pos_xml == "PREPOSITION" or event.pos_xml == "PREP":
            # Get governing verb
            governing_verb = self.nlp_persistence_obj.get_governing_verb(event)

            return self._get_most_likely_duration(governing_verb)
        else:
            return self._get_most_likely_duration(event.text)

    def _get_timex_duration(self, timex):
        value = timex.value
        type = timex.type

        # Matches for stuff like: "2012", "1988", ...
        if re.match(r"^\d\d\d\d$", value):
            return self.durations.index("years")

        # Matches for stuff like "PXD" or "P1D"
        if re.match(r"^P.D$"):
            return self.durations.index("days")

        # Matches for stuff like "PXM" or "P1M"
        if re.match(r"^P.M$"):
            return self.durations.index("months")

        # Matches for stuff like "PXW" or "P1W"
        if re.match(r"^P.W$"):
            return self.durations.index("weeks")

        # Matches for stuff like "PXY" or "P1Y"
        if re.match(r"^P.Y$"):
            return self.durations.index("years")

        # Refers to "now"
        if value == "PRESENT_REF":
            return self.durations.index("sendonds")

        # Matches for stuff like "1999-02-06T06:22"
        if re.match(r"^\d\d\d\d-\d\d-\d\dT\d\d:\d\d$", value):
            return self.durations.index("seconds")

        # Matches for stuff like "2000-03-26TNI" which means Tuesday? Night
        if re.match(r"^\d\d\d\d-\d\d-\d\dT[A-Z][A-Z]$", value):
            return self.durations.index("hours")

        # Matches for stuff like "2012-W11"
        if re.match(r"^\d\d\d\d-W\d*$", value):
            return self.durations.index("weeks")

        # Matches for stuff like "2012-04-04" or "1998-10-XX"
        if re.match(r"^\d\d\d\d-\d\d-..$", value):
            return self.durations.index("days")

        # Matches for stuff like "2012-04"
        if re.match(r"^\d\d\d\d-\d\d$", value):
            return self.durations.index("months")

        # TODO: This should not happen since it's easy to find all rules. Check if this is ever the case
        return None

    def get_length(self):
        return len(self.durations)

    def _get_most_likely_duration(self, verb, obj=None):
        infinitive = self._get_infinitive(verb)

        if obj:
            # Searching for verb and object
            for line in open(self.FILE, "r"):
                if infinitive.lower() in line and obj.lower() in line:
                    # We found the line we are searching for
                    index = self._get_duration_from_line(line)
                    return index

        else:
            # Searching only for verb
            for line in open(self.FILE, "r"):
                if infinitive.lower() in line and "OBJ" not in line:
                    # We found the line which only has the verb and no object
                    index = self._get_duration_from_line(line)
                    return index

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

