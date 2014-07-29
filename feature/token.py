from parsexml.event import Event

class Token:
    def __init__(self, training_set):
        self.tokens = self._get_all_tokens(training_set)

    def get_index(self, token):
        try:
            index = self.tokens.index(token.lower())
        except ValueError:
            return None

    def get_length(self):
        return len(self.tokens)

    def _get_all_tokens(self, training_set):
        tokens = set()

        # Getting all tokens
        for text_obj in training_set.text_objects:
            for relation in text_obj.relations:
                if type(relation.source) == Event:
                    tokens.add(self._get_token(relation.source.text))
                if type(relation.target) == Event:
                    tokens.add(self._get_token(relation.target.text))

        return list(tokens)

    def _get_token(self, text):
        return text.lower()
