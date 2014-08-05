from helper.stanfordnlp.client import StanfordNLP
from nltk import word_tokenize

class Dependency:
    def __init__(self, relation):
        self.relation = relation
        self.source = relation.source
        self.target = relation.target
        self.tree = None

        # TODO: Thats probably not all
        self.dependency_types = ["conj_or", "prep_into", "prep_in", "prepc_amid", "partmod", "parataxis", "prepc_after", "prep_on", "prep_at", "prep_during", "ccomp", "xcomp", "nsubj", "det", "dobj", "conj_and", "advmod", "dep", "num", "prep_for", "advcl"]

        # These features only make sense when both entities are in the same sentence
        if self.relation.target.sentence == self.relation.source.sentence:
            self.sentence = self.relation.target.sentence
            nlp = StanfordNLP()
            self.tree = nlp.parse(unicode(self.sentence))
            print self.sentence

    def get_dependency_type(self):
        if self.tree:
            # Both entities are in the same sentence
            try:
                dependencies = self.tree['sentences'][0]['dependencies']
            except IndexError:
                return None

            for dependency in dependencies:
                a = dependency[1]
                b = dependency[2]
                type = dependency[0]

                if (a == self.source.text or a == self.target.text) and (b == self.source.text or b == self.target.text):
                    # Return index of dependency relation type
                    return self.dependency_types.index(type)
            else:
                return None

        else:
            return None

    def is_source_root(self):
        if self.tree:
            try:
                dependencies = self.tree['sentences'][0]['dependencies']
            except IndexError:
                return None

            for dependency in dependencies:
                b = dependency[2]
                type = dependency[0]

                if type == "root" and b == self.source.text:
                    return True
            else:
                return False

        else:
            return None


    def is_target_root(self):
        if self.tree:
            try:
                dependencies = self.tree['sentences'][0]['dependencies']
            except IndexError:
                return None

            for dependency in dependencies:
                b = dependency[2]
                type = dependency[0]

                if type == "root" and b == self.target.text:
                    return True
            else:
                return False

        else:
            return None

    def get_dependency_order(self):
        if self.tree:
            try:
                dependencies = self.tree['sentences'][0]['dependencies']
            except IndexError:
                return None

            sentence_tokens = word_tokenize(self.sentence)

            # Find governor/root
            governor_text = None
            governor_index = None
            dependent_index = None

            is_source_governor = False
            is_target_governor = False

            for dependency in dependencies:
                type = dependency[0]
                entity_text = dependency[2]

                if type == "root":
                    governor_text = entity_text
                    break

            if governor_text == self.source.text:
                # Source is the governor - let's take a look where it is in the sentence
                governor_index = sentence_tokens.index(governor_text)
                is_source_governor = True

            elif governor_text == self.target.text:
                # Target is the governor - let's take a look where it is in the sentence
                governor_index = sentence_tokens.index(governor_text)
                is_target_governor = True

            if is_source_governor:
                # Find the position of target
                dependent_index = sentence_tokens.index(self.target.text)
            elif is_target_governor:
                # Find the position of source
                dependent_index = sentence_tokens.index(self.source.text)

            if governor_index > dependent_index:
                return 0
            elif governor_index < dependent_index:
                return 1
            else:
                return 2

        else:
            return None
