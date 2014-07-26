class Sentence(object):
    def __init__(self, node):
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

        return self._strip(text) + "."

    def _get_most_right_sentence(self, sentences):
        if sentences:
            parts = sentences.split(".")

            return parts[-1]
        else:
            return ""

    def _get_most_left_sentence(self, sentences):
        if sentences:
            parts = sentences.split(".")

            return parts[0]
        else:
            return ""

    def _strip(self, text):
        text = text.strip()
        text = text.strip('.')
        text = text.strip('\n')

        return text

    def _get_left_part(self, node):
        beginning = None

        prev_node = node.getprevious()

        if prev_node is not None:
            beginning = prev_node.text + prev_node.tail
            if "." in beginning:
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

            if "." in end:
                return end
            else:
                return end + self._get_right_part(node.getnext())
        else:
            return ""
