import logging
import cPickle as pickle
from corenlp import StanfordCoreNLP
from pexpect import TIMEOUT

class Nlp_persistence(object):
    """Persistence layer for having fast access to information produced by the StanfordCoreNLP tool."""
    def __init__(self, fallback=False):
        self.FILE = "nlp_infos.p"
        self.data = None
        self.data_length = None
        self.corenlp_dir = "helper/stanfordnlp/corenlp-python/stanford-corenlp-full-2013-11-12/"
        if fallback:
            try:
                self.corenlp = StanfordCoreNLP(self.corenlp_dir)
            except TIMEOUT:
                print "Stanford CoreNLP Timeout"

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        # When exiting, update pickle file with new sentences and kill StanfordCoreNLP before so we definitely have enough memory for that
        try:
            del(self.corenlp)
        except AttributeError:
            # There was a timeout
            pass

        # Write only if we added something to self.data
        if self.data_length < len(self.data):
            self._write()

    def create_persistence(self, relations):
        try:
            # Trying to load data
            data = pickle.load(open(self.FILE, "rb"))
        except (IOError, EOFError):
            # No data so far
            print "Could not open cache. Create new."
            logging.info("Could not find %s. Create new data.", self.FILE)
            data = {}

        # Create nlp information for all relevant sentences
        for relation in relations:
            if not relation.source.sentence in data:
                self._update_data(relation.source, data)
            else:
                print "Sentence is already in data"

            if not relation.target.sentence in data:
                self._update_data(relation.target, data)
            else:
                print "Sentence is already in data"
        print "Done!"
        logging.info("Successfully loaded all nlp information to persistence file.")

        # Save data to a file
        pickle.dump(data, open(self.FILE, "wb"), protocol=-1)

    def _update_data(self, entity, data):
        sentence_obj = entity.sentence
        try:
            tree = self._get_tree(sentence_obj)
        except RPCInternalError:
            logging.error("Could not process the following sentence from text %s: %s", sentence_obj.filename, sentence_obj.text)
            # Return without updating data
            return

        print "--- " + sentence_obj.filename
        print sentence_obj.text

        data.update({sentence_obj: tree})

    def load(self):
        data = {}

        if self.data is None:
            try:
                data = pickle.load(open(self.FILE, "rb"))
            except (IOError, EOFError):
                logging.warning("No cached nlp data.")
            finally:
                self.data = data
                self.data_length = len(data)
        else:
            # Data is already there - there is nothing to do
            pass

    def get_info_for_sentence(self, sentence):
        if type(self.data) is dict:
            try:
                return self.data[sentence]
            except KeyError:
                logging.error("Nlp_persistence: This sentence is not a key/Is not available in the Nlp persistence layer.")
                logging.info("Nlp_persistence fallback to CoreNLP server")
                # Fallback: Try to get tree from CoreNLP server
                tree = self._get_tree(sentence)

                # Drive by caching
                self.data.update({sentence: tree})

                return tree
        else:
            logging.error("You have to use Nlp_persistence.load() before you can get the information of a sentence")
            return None

    def get_collapsed_dependencies(self, sentence):
        info = self.get_info_for_sentence(sentence)

        return info['sentences'][0]['dependencies']

    def _write(self):
        # Save data to a file
        pickle.dump(self.data, open(self.FILE, "wb"))

    def _get_tree(self, sentence):
        tree = self.corenlp.raw_parse(sentence.text)
        return tree

    def get_pos_tag_for_word(self, sentence, word):
        """Returns the POS tag for a word in a sentence. If the word is not in the sentence raise WordNotInSentence error."""
        info_sentence = self.get_info_for_sentence(sentence)
        words = info_sentence['sentences'][0]['words']

        for w in words:
            if w[0] in word:
                return w[1]["PartOfSpeech"]
        else:
            raise PosTagNotFound(sentence, word)

    def is_main_verb(self, sentence, word):
        """Returns true if word is a main verb of sentence and not an aux."""
        info_sentence = self.get_info_for_sentence(sentence)
        dependencies = info_sentence['sentences'][0]['dependencies']

        for dependency in dependencies:
            if dependency[0] == "aux" and dependency[2] == word:
                return False
        else:
            return True

    def get_all_aux_for_verb(self, sentence, verb):
        """Returns all distinct aux for verb as strings in order of the sentence."""
        info_sentence = self.get_info_for_sentence(sentence)
        dependencies = info_sentence['sentences'][0]['dependencies']

        aux = []
        for dependency in dependencies:
            if (dependency[0] == "aux" or dependency[0] == "auxpass") and dependency[1] == verb:
                aux.append(dependency[2])

        return aux

    def get_verb_for_aux(self, sentence, aux):
        """Returns the governing verb for the aux as string."""
        info_sentence = self.get_info_for_sentence(sentence)
        dependencies = info_sentence['sentences'][0]['dependencies']

        for dependency in dependencies:
            if dependency[0] == "aux" and dependency[2] == aux:
                return dependency[1]
        else:
            raise AuxNotFound(aux)

    def find_all_verb_pos_tags(self, sentence, verb):
        """Returns all pos tags for all verbs based on the dependencies relation of the sentence."""

        if self.is_main_verb(sentence, verb):
            # verb is not an aux
            main_verb = verb
        else:
            # verb is aux (this should normally not happen due to the data)
            main_verb = self.get_verb_for_aux(sentence, verb)

        auxes = self.get_all_aux_for_verb(sentence, main_verb)

        verb_pos = self.get_pos_tag_for_word(sentence, main_verb)

        aux_pos = map(lambda aux: self.get_pos_tag_for_word(sentence, aux), auxes)

        return aux_pos + [verb_pos]

    def get_governing_verb(self, event):
        sentence = event.sentence

        # info = [verb, aux, pos verb, pos aux, index_of_verb]
        info = self.get_info_on_governing_verb(event.text, event.index, sentence)

        if info is None:
            raise CouldNotFindGoverningVerb
        else:
            if info[0] is None:
                raise CouldNotFindGoverningVerb
            else:
                return (info[0], info[4])

    def is_root(self, event):
        sentence = event.sentence
        info_sentence = self.get_info_for_sentence(sentence)

        collapsed_dependencies = info_sentence['sentences'][0]['dependencies']

        for dependency in collapsed_dependencies:
            dependency_type = dependency[0]
            dependent = dependency[2]

            if dependency_type == "root" and dependent == event.text:
                return True
        else:
            return False

    def get_info_on_governing_verb(self, non_verb, index, sentence):
        """This method returns information about the governing verb of a non-verb.

        It returns an array with the following format: [verb, aux, POS of verb, POS of aux, index_of_verb]
        """
        info = self.get_info_for_sentence(sentence)

        if info:
            # Search for non_verb
            governing_verb, index = self._get_governing_verb(non_verb, index, info)

            info_on_governing_verb = [governing_verb, None, None, None, index]

            # Set POS of main verb
            pos_verb = self._get_pos_of_verb(governing_verb, info)
            info_on_governing_verb[2] = pos_verb

            # Searching for an Aux for the governing verb
            aux = self._get_aux_of_verb(governing_verb, info)
            info_on_governing_verb[1] = aux

            # If there is an aux, get it's POS
            if aux:
                pos_aux = self._get_pos_of_verb(aux, info)
                info_on_governing_verb[3] = pos_aux

            return info_on_governing_verb

        else:
            return None

    def _get_aux_of_verb(self, verb, info):
        dependencies = info['sentences'][0]['dependencies']

        sources = [x[1] for x in dependencies]

        # Find index of verb in targets
        index = None
        for i, source in enumerate(sources):
            if source == verb and dependencies[i][0] == "aux":
                index = i

        # Get aux
        if index is None:
            # Not every verb has an aux
            return None
        else:
            aux = dependencies[index][2]

            return aux

    def _get_pos_of_verb(self, verb, info):
        info_on_words = info['sentences'][0]['words']

        for word in info_on_words:
            if word[0] == verb:
                return word[1]['PartOfSpeech']

    def _find_governing_word(self, word, dependencies):
        for dependency in dependencies:
            if dependency[2] == word:
                return dependency[1]
        else:
            return None

    def _find_governing_word_index(self, word, index, index_dependencies):
        word = word + "-" + str(index)

        for dependency in index_dependencies:
            if dependency[2] == word:
                # Remove governor with index appended
                return dependency[1]
        else:
            return None

    def _remove_index_from_token(self, token):
        if token:
            token = token.split("-")[:-1]
            return "-".join(token)
        else:
            return None

    def _get_index_from_token(self, token):
        if token:
            index = token.split("-")[-1]
            return index
        else:
            return None

    def _get_governing_verb(self, non_verb, index, info):
        index_dependencies = info['sentences'][0]['indexeddependencies']

        # Try to find a governor for non_verb
        governor = self._find_governing_word_index(non_verb, index, index_dependencies)

        # Search through tree as long we find a verb and until we can go further up
        while not self._is_verb(self._remove_index_from_token(governor), info) and governor is not None:
            old_governor = governor
            governor = self._find_governing_word_index(self._remove_index_from_token(governor), self._get_index_from_token(governor), index_dependencies)

            if governor == old_governor:
                # Detected circle (does not happen often, but happens. Not sure why.)
                governor = None
                break

        if governor:
            # Remove index from governor string
            return (self._remove_index_from_token(governor), int(self._get_index_from_token(governor)))
        else:
            # Examples when this is allowed to happen:
            # Example for when it happens: "And in Hong Kong, a three percent drop." <- no verb
            # Other example: "One exception was the swine flu pandemic of 2009-2010, when 348 children died." and "pandemic". "pandemic" is the root of the sentence and is not governed by anything
            # Other corner case: "And the dominant flu strain early in the season was one that tends to cause more severe illness." for "season"
            raise CouldNotFindGoverningVerb(non_verb, index)

    def _is_verb(self, text, info):
        """Checks if text has the POS tag of a verb."""
        if not text: return False

        words = info['sentences'][0]['words']

        for word in words:
            if word[0] == text:
                if word[1]['PartOfSpeech'] in ['VBG', 'VBD', 'VB', 'VBN', 'VBP', 'VBZ']:
                    return True

        return False



class PosTagNotFound(Exception):
    def __init__(self, sentence, word):
        self.sentence = sentence.text
        self.word = word

    def __str__(self):
        return repr("Could not find POS tag for word %s in sentence: %s" % (self.word, self.sentence))

class NoSentenceFound(Exception):
    def __str__(self):
        return repr("Could not find a sub sentence in sentence which includes this word.")

class CouldNotFindGoverningVerb(Exception):
    def __init__(self, non_verb=None, index=None):
        self.non_verb = non_verb
        self.index = index

    def __str__(self):
        if not self.non_verb and not self.index:
            return repr("Could not find a governing verb.")
        else:
            return repr("Could not find a governing verb for '%s' with index %i" % (self.non_verb, self.index))
