class Temporal_signal:
    def __init__(self, relation):
        self.relation = relation
        self.text_structure = relation.parent.text_structure
        self.signals_event = ["then", "as", "when", "before", "after", "until"]
        self.signals_timex = ["at", "for", "within", "before", "after", "until"]
        self.signal = None

    def get_signal(self, event=True):
        """Returns a number representing a certain signal word or zero if there is no signal word.

        If event=True the event signals will be returned. Otherwise the timex signals.
        """
        source_sentence = self.text_structure.get_sentence(relation.source)
        target_sentence = self.text_structure.get_sentence(relation.target)

        if source_sentence == target_sentence:
            sentence = source_sentence

            if event:
                for signal in self.signals_event:
                    if signal in sentence.text:
                        self.signal = signal
                        return (self.signals_event.index(signal) + 1)

                else:
                    return 0
            else:
                for signal in self.signals_timex:
                    if signal in sentence.text:
                        self.signal = signal
                        return (self.signals_timex.index(signal) + 1)

                else:
                    return 0

        else:
            # Lets only consider signals when source and target entity are in the same sentence
            return False

    def get_signal_position_relative_to_entities(self):
        """Must be called after get_signal()."""
        pass

    def is_at_begging_of_sentence(self):
        """Must be called after get_signal(). Returns 0 if the signal is at the beginning of a sentence and 1 otherwise."""
        source_sentence = self.text_structure.get_sentence(relation.source)
        target_sentence = self.text_structure.get_sentence(relation.target)

        if source_sentence == target_sentence:
            if self.signal:
                sentence = source_sentence

                if sentence.text.split()[0] == self.signal:
                    return 0
                else:
                    return 1

            else:
                return False
        else:
            # Lets only consider signals when source and target entity are in the same sentence
            return False
