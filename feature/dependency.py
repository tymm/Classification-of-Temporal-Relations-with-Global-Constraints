from nltk import word_tokenize
import logging

class Dependency:
    def __init__(self, relation, nlp_persistence_obj):
        self.relation = relation
        self.source = relation.source
        self.target = relation.target
        self.tree = None

        # List of all dependencies (from data and the Stanford dependencies manual
        self.dependency_types = ["prep_like", "prep_out", "prep_because_of", "conj_just", "prep_apart_from", "prepc_including", "prepc_in_addition_to", "prepc_upon", "prep_upon", "prep_through", "cop", "auxpass", "prepc_such_as", "iobj", "csubjpass", "prepc_apart_from", "prepc_toward", "prep_that", "prep_besides", "prepc_besides", "prep_behind", "prep_between", "prepc_unlike", "prep_until", "prep_along_with", "prep_out_of", "prep_despite", "prepc_out", "conj", "pcomp", "prepc_about", "prep_in_case_of", "prepc_instead_of", "prep_instead_of", "prep_away_from", "prepc_among", "prep_including", "prepc_into", "prep_within", "npadvmod", "prepc_despite", "prep", "prep_prior_to", "prep_amid", "prepc_against", "prep_without", "prepc_from", "prep_between", "prepc_to", "prep_amidst", "prep_throughout", "prep_from", "nn", "prepc_of", "prep_to", "prep_against", "prep_by", "rcmod", "pobj", "prepc_in", "infmod", "prepc_during", "prepc_without", "prep_pending", "prep_due_to", "prepc_since", "prep_since", "prepc_around", "conj_nor", "prep_under", "prep_following", "nsubjpass", "prep_as", "nsubjpass", "prepc_on", "poss", "prep_over", "prepc_at", "prepc_while", "prepc_with", "csubj", "prepc_as", "acomp", "xsubj", "agent", "prep_of", "prep_before", "prepc_by", "prepc_for", "prepc_on", "aux", "tmod", "prep_about", "attr", "prep_off", "prepc_over", "prepc_at", "prep_ahead_of", "prepc_before", "prep_after", "purpcl", "conj_only", "conj_but", "prep_with", "amod", "conj_or", "prep_into", "prep_in", "prepc_amid", "partmod", "parataxis", "prepc_after", "prep_on", "prep_at", "prep_during", "ccomp", "xcomp", "nsubj", "det", "dobj", "conj_and", "advmod", "dep", "num", "prep_for", "advcl", "arg", "comp", "obj", "subj", "cc", "expl", "mod", "appos", "predet", "preconj", "vmod", "mwe", "mark", "neg", "quantmod", "number", "possessive", "prt", "punct", "ref", "sdep"]

        # These features only make sense when both entities are in the same sentence
        if self.relation.target.sentence == self.relation.source.sentence:
            self.sentence = self.relation.target.sentence
            self.tree = nlp_persistence_obj.get_info_for_sentence(self.sentence)

            # Get collapsed dependency relations
            try:
                self.collapsed_dependencies = self.tree['sentences'][0]['dependencies']
            except IndexError:
                return None


    def get_dependency_type(self):
        for dependency in self.collapsed_dependencies:
            a = dependency[1]
            b = dependency[2]
            type = dependency[0]

            if (a == self.source.text or a == self.target.text) and (b == self.source.text or b == self.target.text):
                # Return index of dependency relation type
                try:
                    return self.dependency_types.index(type)
                except ValueError:
                    logging.error("Dependency feature: Do not know %s", type)
                    return 0
        else:
            return None

    def is_source_root(self):
        for dependency in self.collapsed_dependencies:
            b = dependency[2]
            type = dependency[0]

            if type == "root" and b == self.source.text:
                return True
        else:
            return False

    def is_target_root(self):
        for dependency in self.collapsed_dependencies:
            b = dependency[2]
            type = dependency[0]

            if type == "root" and b == self.target.text:
                return True
        else:
            return False

    def get_dependency_order(self):
        sentence_tokens = word_tokenize(self.sentence.text)

        # Find governor/root
        governor_text = None
        governor_index = None
        dependent_index = None

        is_source_governor = False
        is_target_governor = False

        for dependency in self.collapsed_dependencies:
            type = dependency[0]
            entity_text = dependency[2]

            if type == "root":
                governor_text = entity_text
                break

        try:
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

        except ValueError:
            # TODO: This shouldn't happen - It does though
            return None

        if governor_index > dependent_index:
            return 0
        elif governor_index < dependent_index:
            return 1
        else:
            return 2
