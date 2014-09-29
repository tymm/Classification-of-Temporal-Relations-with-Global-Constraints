class Temporal_signal:
    def __init__(self, relation):
        self.relation = relation
        self.text_structure = relation.parent.text_structure
        self.signals_event = ["then", "as", "when", "before", "after", "until"]
        self.signals_timex = ["at", "for", "within", "before", "after", "until"]
        self.indexes = list(set(self.signals_event + self.signals_timex))

        try:
            self.signal, self.sentence_with_signal = self._get_signal()
            self.signal_position_in_sentence = self._get_signal_position_in_sentence(self.sentence_with_signal)
        except MultipleSignalsInSentence:
            self.signal = None
            self.sentence_with_signal = None
            self.signal_position_in_sentence = None

    def get_length(self):
        return len(self.indexes) + 1

    def get_signal(self):
        if self.signal is None:
            return 0
        else:
            return self.indexes.index(self.signal)

    def _get_signal_position_in_sentence(self, sentence):
        if self.signal and self.sentence_with_signal:
            begin = sentence.text.find(self.signal)
            end = begin + len(self.signal)

            return (begin, end)
        else:
            return None

    def _get_signal(self):
        source_sentence = self.text_structure.get_sentence(self.relation.source)
        target_sentence = self.text_structure.get_sentence(self.relation.target)

        if source_sentence == target_sentence:
            # We only use a signal, if there is only one signal in this sentence
            signal = self._find_signal_in_sentence(source_sentence)
            return (signal, source_sentence)
        else:
            # We only use a signal, if in both sentences there is one signal in total
            signal_source = self._find_signal_in_sentence(source_sentence)
            signal_target = self._find_signal_in_sentence(target_sentence)

            if signal_source and not signal_target:
                return (signal_source, source_sentence)
            elif not signal_source and signal_target:
                return (signal_target, target_sentence)
            else:
                raise MultipleSignalsInSentence

    def _find_signal_in_sentence(self, sentence):
        signals = []

        # Use different signal sets for event-event and event-timex
        if self.relation.is_event_event():
            for signal in self.signals_event:
                if signal in sentence.text:
                    signals.append(signal)
        else:
            for signal in self.signals_timex:
                if signal in sentence.text:
                    signals.append(signal)

        if len(signals) == 1:
            return signals[0]
        elif len(signals) == 0:
            return None
        else:
            raise MultipleSignalsInSentence

    def is_signal_at_beginning(self):
        if self.sentence_with_signal and self.signal:
            if self.sentence_with_signal.text.strip().startswith(self.signal):
                return True
            else:
                return False
        else:
            return None

    def entity_before_signal(self, entity):
        if self.signal:
            if entity in self.text_structure.structure[self.sentence_with_signal]:
                # Signal and entity are in the same sentence
                if entity.begin > self.signal_position_in_sentence[0]:
                    return False
                else:
                    return True
            else:
                # Signal and entity are not in the same sentence
                sentence = self.text_structure.get_sentence(entity)

                if self.text_structure.is_sentence_before_sentence(sentence, self.sentence_with_signal):
                    return True
                else:
                    return False
        else:
            return None

class MultipleSignalsInSentence(Exception):
    def __str__(self):
        return repr("There are multiple signals in sentence. Do not know which one to choose.")
