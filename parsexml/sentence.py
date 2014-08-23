class Sentence(object):
    def __init__(self, node, filename):
        self.filename = filename
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

    def get_info_on_governing_verb(self, non_verb, nlp_persistence_obj):
        """This method returns information about the governing verb of a non-verb."""
        info = nlp_persistence_obj.get_info_for_sentence(self)

        if info:
            # Search for non_verb
            dependencies = info['sentences'][0]['dependencies']
            print dependencies

            governing_verb = self._get_governing_verb(non_verb, dependencies, info)

            info_on_words = info['sentences'][0]['words']

            info_on_governing_verb = (governing_verb, None)
            for word in info_on_words:
                if word[0] == governing_verb:
                    # Format: (text, POS)
                    info_on_governing_verb = (governing_verb, None)

            return info_on_governing_verb

        else:
            return None

    def _get_governing_verb(self, non_verb, dependencies, info):
        targets = [x[2] for x in dependencies]

        # Find occurrences of non_verb and get the indicies
        indicies = []
        for target in targets:
            if target == non_verb:
                indicies.append(targets.index(target))

        # Get the corresponding sources
        sources = [x[1] for x in dependencies]

        for index in indicies:
            source = sources[index]
            if self._is_verb(source, info):
                # Found the governing verb
                print source
                return source

        # This should not happen in a proper sentence
        return None

    def _is_verb(self, text, info):
        """Checks if text has the POS tag of a verb."""
        words = info['sentences'][0]['words']

        for word in words:
            if word[0] == text:
                if word[1]['PartOfSpeech'] in ['VBG', 'VBD', 'VB', 'VBN', 'VBP', 'VBZ']:
                    return True

        return False

    def get_root(self, nlp_persistence_obj):
        pass

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
