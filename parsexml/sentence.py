import nltk.data
import re

class Sentence(object):
    def __init__(self, node, filename):
        self.filename = filename
        self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        self.text = self._get_sentence(node)

    def __eq__(self, other):
        return self.text == other.text

    def __hash__(self):
        return hash(self.text)

    def __str__(self):
        return u"Sentence Object: %s" % (self.text)

    def get_position(self, text):
        """Returns the position of text in the sentence"""
        # TODO: This is a super naive version
        split = self.text.split(" ")

        try:
            return split.index(text)
        except ValueError:
            return None

    def _get_sentence(self, node):
        left = self._get_left_part(node)
        right = self._get_right_part(node)

        left_sentence = self._get_most_right_sentence(left)
        right_sentence = self._get_most_left_sentence(right)

        if left_sentence and right_sentence:
            text = left_sentence + right_sentence
        elif left_sentence:
            text = left_sentence
        elif right_sentence:
            text = right_sentence

        text = self._strip(text)
        return text

    def _get_most_right_sentence(self, sentences):
        if sentences:
            parts = self.sent_detector.tokenize(sentences)

            if sentences.endswith('.\n\n"') or sentences.endswith('.\n"'):
                # Case: Bla bla.\n\n"<Entity>
                # nltk sentence tokenizer thinks Bla bla.\n\n" is one sentence
                return '"'
            elif sentences.endswith('.\n\n'):
                # Case: Bla bla!".\n\n<Entity>
                return ""
            elif len(parts) == 1 and ".\n" in parts[0]:
                # Case: Bla bla.\n<Entity> blab bla.
                # But not case: Text beginning --> Bla bla <entity> bla bla.
                return ""
            else:
                return parts[-1]
        else:
            return ""

    def _get_most_left_sentence(self, sentences):
        if sentences:
            parts = self.sent_detector.tokenize(sentences)

            # Using sentences instead of parts[0] because self.sent_detector removes \n
            if len(parts) == 1 and (sentences.endswith('.\n\n"') or sentences.endswith('.\n"')):
                # Case: <entity> bla bla.\n\n"
                # The nltk sentence tokenizer thinks that the " belongs to the sentence which is not the case
                left_sentence = sentences
                left_sentence = re.sub('\n+"', '', left_sentence, re.MULTILINE)

                return left_sentence
            else:
                return parts[0]
        else:
            return ""

    def _strip(self, text):
        text = text.strip()
        text = text.strip('\n')

        return text

    def _get_left_part(self, node):
        beginning = None

        prev_node = node.getprevious()

        if prev_node is not None:
            beginning = prev_node.text + prev_node.tail
            if ".\n" in beginning or '."\n' in beginning or "!\n" in beginning or '!"\n' in beginning:
                return beginning
            else:
                return self._get_left_part(prev_node) + beginning
        else:
            # We are either at the beginning or in a headline
            parent_text = node.getparent().text

            # Assumption: Parents of headlines (<DCT></DCT>) don't have text
            if parent_text:
                return parent_text
            else:
                return ""

    def _get_right_part(self, node):
        if node is not None:
            # Get next text
            if node.tail:
                end = node.text + node.tail
            else:
                end = node.text

            if ".\n" in end or '."\n' in end or "!\n" in end or '!"\n' in end:
                return end
            else:
                return end + self._get_right_part(node.getnext())
        else:
            return ""
