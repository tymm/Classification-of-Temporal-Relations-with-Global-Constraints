from nltk import word_tokenize
import logging

class Dependency:
    def __init__(self, relation, nlp_persistence_obj):
        self.relation = relation
        self.source = relation.source
        self.target = relation.target
        self.tree = None

        # List of all dependencies used in data
        self.dependency_types = ['prep_down', 'prepc_toward', 'prep_pending', 'prep_below', 'prep_astride', 'prep_despite', 'prepc_in', 'predet', 'prepc_compared_to', 'prep_during', 'prepc_alongside', 'conj_nor', 'prepc_at', 'prep_throughout', 'conj_still', 'prepc_regardless_of', 'prepc_as', 'prepc_like', 'prepc_with', 'prep_as_of', 'prep_about', 'mwe', 'advcl', 'prep_out', 'aux', 'prep_in_lieu_of', 'prep_though', 'prep_unlike', 'parataxis', 'prepc_apart_from', 'prep_over', 'prep_monitoring', 'nsubj', 'prep_close_to', 'prep_contrary_to', 'prep_upon', 'prep_except', 'prep_inside', 'prepc_between', 'prep_onto', 'prep_@', 'prep_underneath', 'prep_apart_from', 'npadvmod', 'prep_while', 'conj_negcc', 'prepc_as_for', 'prepc_unlike', 'prep_de', 'prep_atop', 'amod', 'prep_on', 'prep_as_for', 'prep_aside_from', 'prep_as', 'prep_of', 'prep_afer', 'prepc_below', 'prep_next_to', 'prep_excluding', 'prep_outside_of', 'prepc_across_from', 'prep_by', 'prep_with', 'prepc_before', 'prep_whether', 'prepc_according_to', 'prep_across', 'prep_en', 'prep_that', 'ccomp', 'prep_along', 'num', 'prep_than', 'prepc_for', 'prep_on_behalf_of', 'prepc_ahead_of', 'prepc_along_with', 'prep_ahead_of', 'prepc_as_to', 'prep_in_accordance_with', 'prep_starting', 'prepc_as_of', 'prep_in_case_of', 'neg', 'prep_pursuant_to', 'prepc_from', 'auxpass', 'prepc_away_from', 'prep_because', 'infmod', 'conj_of', 'prep_till', 'prep_for', 'prep_away_from', 'conj_just', 'prepc_until', 'prep_on_top_of', 'prepc_amid', 'prep_through', 'prep_at', 'prep_worth', 'prepc_instead_of', 'prepc_into', 'prep_between', 'punct', 'prepc_despite', 'acomp', 'pcomp', 'prep_per', 'prepc_near', 'prep_around', 'poss', 'prep_according', 'xcomp', 'cop', 'prepc_among', 'prepc_than', 'conj_plus', 'prep_past', 'appos', 'prep_like', 'prepc_against', 'dobj', 'prep_following', 'prep_in', 'prepc_off', 'prep__', 'prepc_upon', 'prep_being', 'prep_involving', 'prep_above', 'prepc_that', 'prep_against', 'prepc_to', 'prep_beneath', 'cc', 'prep_via', 'prep_among', 'prep_on_account_of', 'prep_up', 'number', 'possessive', 'prepc_such_as', 'nsubjpass', 'conj_or', 'csubj', 'prep_considering', 'prepc_compared_with', 'prep_without', 'prepc_including', 'prepc_about', 'prep_under', 'prep_after', 'prep_due_to', 'prep_toward', 'prep_out_of', 'prep_aboard', 'prep_off_of', 'mark', 'prepc_around', 'advmod', 'prep_besides', 'prep', 'prepc_over', 'conj_and', 'prepc_towards', 'prep_outside', 'prep_including', 'prepc_except_for', 'prep_because_of', 'prepc_without', 'prep_along_with', 'prep_to', 'prep_near', 'tmod', 'prepc_because', 'prep_before', 'prepc_out_of', 'prepc_depending_on', 'prep_off', 'conj_soon', 'prep_next', 'prepc_followed_by', 'prep_amongst', 'conj_+', 'prepc_through', 'prep_beginning', 'prepc_next_to', 'dep', 'prep_in_addition_to', 'det', 'prep_regardless_of', 'prep_prior_to', 'pobj', 'iobj', 'prep_amp', 'expl', 'prep_such_as', 'prepc_contrary_to', 'preconj', 'prep_concerning', 'root', 'conj_but', 'prepc_besides', 'prepc_of', 'conj_merely', 'conj_in', 'prepc_under', 'prepc_on', 'prepc_since', 'prep_with_regard_to', 'agent', 'prep_instead_of', 'prt', 'prep_into', 'prep_from', 'prepc_following', 'prep_amid', 'conj', 'prep_beyond', 'conj_vs', 'conj_only', 'prepc_as_per', 'nn', 'conj_and/or', 'prep_far_from', 'csubjpass', 'prepc_because_of', 'prep_except_for', 'discourse', 'prep_beside', 'prepc_during', 'prep_since', 'prepc_while', 'prep_within', 'prep_followed_by', 'prep_in_spite_of', 'conj_often', 'rcmod', 'prep_behind', 'prepc_near_to', 'prepc_due_to', 'prep_nearer', 'prep_irrespective_of', 'conj_versus', 'prepc_in_addition_to', 'prepc_based_on', 'prep_in_place_of', 'prep_towards', 'prep_across_from', 'prep_thanks_to', 'prep_regarding', 'prep_barring', 'partmod', 'conj_yet', 'prep_together_with', 'prepc_out', 'prep_alongside', 'quantmod', 'prep_if', 'prep_in_front_of', 'prepc_after', 'prepc_by', 'prepc_far_from', 'prep_until', 'prep_amidst']

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
