class FakeSentence(object):
    """For being able to compare text with Sentence objects."""
    def __init__(self, text):
        self.text = text

    def __eq__(self, other):
        return self.text == other.text

    def __hash__(self):
        return hash(self.text)
