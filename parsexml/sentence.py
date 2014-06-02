class Sentence:
    def __init__(self, node):
        self.text = self._get_sentence(node)

    def __eq__(self, other):
        return self.sentence == other.sentence

    def __hash__(self):
        return hash(self.sentence)

    def get_position(self, node):
        """Returns the position of node.text in the sentence"""
        # TODO: This is a super naive version
        split = self.sentence.split(" ")

        try:
            return split.index(node.text)
        except ValueError:
            return None

    def _get_sentence(self, node):
        left = self._get_left_part(node)
        right = self._get_right_part(node)

        if left and right:
            text = left + right
        elif left:
            text = left
        elif right:
            text = right

        return self._strip_dots(text)

    def _strip_dots(self, text):
        if "." in text:
            string = None
            parts = text.split(".")

            if len(parts) == 3:
                string = parts[1]
            elif len(parts) == 2:
                string = parts[0]
            else:
                string = parts[0]

            string = string.strip() + "."
            return string
        else:
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
            # We are at the beginning
            return node.getparent().text

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
