class FakeSentence(object):
    """For being able to compare text with Sentence objects."""
    def __init__(self, text):
        self.text = self._strip(text) + "."

    def __eq__(self, other):
        return self.text == other.text

    def __hash__(self):
        return hash(self.text)

    def __str__(self):
        return u"FakeSentence Object: %s" % (self.text)

    def _strip(self, text):
        text = text.strip()
        text = text.strip('.')
        text = text.strip('\n')

        return text
