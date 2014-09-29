import re
from nltk.stem.wordnet import WordNetLemmatizer
from parsexml.event import Event
from parsexml.timex import Timex
from helper.nlp_persistence import CouldNotFindGoverningVerb
from feature.exception import FailedProcessingFeature

class Duration:
    def __init__(self, nlp_persistence_obj):
        self.FILE = "event.lexicon.distributions"
        self.nlp_persistence_obj = nlp_persistence_obj
        self.durations = ["seconds", "minutes", "hours", "days", "weeks", "months", "years", "decades"]

    def get_length(self):
        return 9

    def get_duration(self, entity):
        if type(entity) is Event:
            try:
                duration = self._get_event_duration(entity)
                return duration
            except InfinitiveNotInDistributionFile:
                return 8
            except CouldNotFindGoverningVerb:
                raise FailedProcessingFeature("Duration")

        elif type(entity) is Timex:
            try:
                duration = self._get_timex_duration(entity)
                return duration
            except NoTimeSpan:
                return 8

    def _get_event_duration(self, event):
        if event.pos_xml == "NOUN" or event.pos_xml == "ADJECTIVE" or event.pos_xml == "PREPOSITION" or event.pos_xml == "PREP":
            # Get governing verb
            governing_verb = self.nlp_persistence_obj.get_governing_verb(event)

            return self._get_most_likely_duration(governing_verb)
        else:
            duration = self._get_most_likely_duration(event.text)
            if duration is None:
                return 8
            else:
                return duration

    def _get_timex_duration(self, timex):
        value = timex.value
        type = timex.type

        # Matches for stuff like: "2012", "1988", ...
        if re.match(r"^\d\d\d\d$", value):
            return self.durations.index("years")

        # Matches for stuff like "PXD" or "P1D"
        if re.match(r"^PXD|P\d+D$", value):
            return self.durations.index("days")

        # Matches for stuff like "P02:00D"
        if re.match(r"P0\d:\d\dD$", value):
            return self.durations.index("days")

        # Matches for stuff like "P12:00D"
        if re.match(r"P\d\d:\d\dD$", value):
            return self.durations.index("weeks")

        # Matches for stuff like "P1Q" or "PXQ"
        if re.match(r"^PXQ|P\d+Q$", value):
            return self.durations.index("months")

        # Matches for stuff like "PXM" or "P1M"
        if re.match(r"^PXM|P\d+M$", value):
            return self.durations.index("months")

        # Matches for stuff like "PXW" or "P1W"
        if re.match(r"^PXW|P\d+W$", value):
            return self.durations.index("weeks")

        # Matches for stuff like "PXY" or "P1Y"
        if re.match(r"^PXY|P\d+Y$", value):
            return self.durations.index("years")

        # Exceptions to the next one
        if re.match(r"^PT24H|PT48H|PT72H", value):
            return self.durations.index("days")

        # Matches for stuff like "PT5H" or "PT5H30M"
        if re.match(r"^PT(\d+|X)H", value):
            return self.durations.index("hours")

        # Matches for stuff like "P2C" or "P18C"
        if re.match(r"^P\d+C$", value):
            return self.durations.index("decades")

        # Matches for stuff like "P19:00C"
        if re.match(r"^P\d\d:\d\dC$", value):
            return self.durations.index("years")

        # Matches for stuff like "PT33.52S"
        if re.match(r"^PT\d\d(\.\d+){0,1}S$", value):
            return self.durations.index("seconds")

        # Matches for stuff like "PT1M" or "PT12.5M"
        if re.match(r"^PT\d+(\.\d+){0,1}M$", value):
            return self.durations.index("minutes")

        # Matches for stuff like "PT1M30S"
        if re.match(r"^PT\d+M\d\dS$", value):
            return self.durations.index("minutes")

        # Matches for stuff like "P1E" or "P1DE"
        if re.match(r"^P\d+(E|DE)$", value):
            return self.durations.index("decades")

        # Matches for stuff like "1997-W13-WE"
        if re.match(r"^\d\d\d\d-W(\d\d|XX)-WE", value):
            return self.durations.index("days")

        if re.match(r"^PXX$", value):
            raise NoTimeSpan

        if re.match(r"^21$", value):
            return self.durations.index("decades")

        # Refers to "now"
        if value == "PRESENT_REF":
            raise NoTimeSpan

        # Can't be reffered to a certain time span
        if value == "PAST_REF":
            raise NoTimeSpan

        # Can't be reffered to a certain time span
        if value == "FUTURE_REF":
            raise NoTimeSpan

        if value == "2006-W48-WE":
            return self.durations.index("days")

        # Matches for stuff like "2006-WI" (WI winter, SP spring, SU Summer, FA fall)
        if re.match(r"^(\d\d\d\d|XXXX)-(WI|SP|SU|FA)$", value):
            return self.durations.index("months")

        # Matches for stuff like 2005-Q3
        if re.match(r"^\d\d\d\d-Q(1|2|3|4|X)$", value):
            return self.durations.index("months")

        # Matches for stuff like XXXX-XX-XXTMO ("every morning")
        if re.match(r"^(XXXX|\d\d\d\d)-(XX|\d\d)-(XX|\d\d)TMO$", value):
            return self.durations.index("hours")

        # Matches for stuff like 2012-WXX-7TNI (example: "Sunday night")
        if re.match(r"^(\d\d\d\d|XXXX)-W(XX|\d\d)-\dTNI$", value):
            return self.durations.index("months")

        # Matches for stuff like "1999-02-06T06:22"
        if re.match(r"^\d\d\d\d-\d\d-\d\dT\d\d:\d\d$", value):
            return self.durations.index("seconds")

        if value == "2012-XX-XX" or value == "XXXX-XX-XX":
            return self.durations.index("days")

        # Matches for stuff like "2000-03-26TNI" which means Tuesday? Night
        if re.match(r"^\d\d\d\d-\d\d-\d\dT[A-Z][A-Z]$", value):
            return self.durations.index("hours")

        # Matches for stuff like "2012-W11" or "1989-WXX"
        if re.match(r"^\d\d\d\d-W(\d*|XX)$", value):
            return self.durations.index("weeks")

        # Matches for stuff like "2012-04-04" or "1998-10-XX"
        if re.match(r"^\d\d\d\d-\d\d-..$", value):
            return self.durations.index("days")

        # Matches for stuff like "2012-04"
        if re.match(r"^\d\d\d\d-\d\d$", value):
            return self.durations.index("months")

        # Matches for stuff like "XXXX-WXX-4" (for example: "each thursday")
        if re.match(r"^(XXXX|\d\d\d\d)-W(XX|\d\d)-\d$", value):
            return self.durations.index("days")

        # Matches for stuff like "1998-04-24T21:49:00"
        if re.match(r"^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d$", value):
            return self.durations.index("seconds")

        # Matches for stuff like "XXXX"
        if value == "XXXX":
            return self.durations.index("years")


        raise NoTimeSpan

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

        raise InfinitiveNotInDistributionFile

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
            raise InfinitiveNotInDistributionFile

class InfinitiveNotInDistributionFile(Exception):
    def __str__(self):
        return repr("Could not find infinitive of verb in distribution file.")

class NoTimeSpan(Exception):
    def __str__(self):
        return repr("No time span.")
