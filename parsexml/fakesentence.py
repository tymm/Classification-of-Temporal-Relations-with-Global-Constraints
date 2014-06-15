class FakeSentence:
    """For being able to compare text with Sentence objects."""
    def __init__(self, text):
        self.text = text
