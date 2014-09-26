import logging
import cPickle as pickle
from corenlp import StanfordCoreNLP
from pexpect import TIMEOUT

class Nlp_persistence:
    """Persistence layer for having fast access to information produced by the StanfordCoreNLP tool."""
    def __init__(self):
        self.FILE = "nlp_infos.p"
        self.data = None
        self.data_length = None
        self.corenlp_dir = "helper/stanfordnlp/corenlp-python/stanford-corenlp-full-2013-11-12/"
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
        try:
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
        except:
            logging.error("Could not finish loading all nlp information to the persistence file. Saving all processed ones.")

        # Save data to a file
        pickle.dump(data, open(self.FILE, "wb"))

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
        if self.data is None:
            try:
                data = pickle.load(open(self.FILE, "rb"))
            except (IOError, EOFError):
                logging.warning("No cached nlp data.")

                data = {}
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
            if w[0] == word:
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

    def find_all_verb_pos_tags(self, sentence, event_text):
        """Returns all pos tags for all verbs based on the dependencies relation of the sentence."""

        if self.is_main_verb(sentence, event_text):
            # event_text is not an aux
            main_verb = event_text
        else:
            # event_text is aux (this should normally not happen due to the data)
            main_verb = self.get_verb_for_aux(sentence, event_text)

        auxes = self.get_all_aux_for_verb(sentence, main_verb)

        verb_pos = self.get_pos_tag_for_word(sentence, main_verb)

        aux_pos = map(lambda aux: self.get_pos_tag_for_word(sentence, aux), auxes)

        return aux_pos + [verb_pos]

    def get_governing_verb(self, event):
        sentence = event.sentence

        # info = [verb, aux, pos verb, pos aux]
        info = sentence.get_info_on_governing_verb(event.text, self)

        if info is None:
            return None
        #elif info[1]:
        #  return info[1] + " " + info[0]
        else:
           return info[0]

    def is_root(self, event):
        sentence = event.sentence
        collapsed_dependencies = self.get_info_for_sentence(sentence)['sentences'][0]['dependencies']

        for dependency in collapsed_dependencies:
            dependency_type = dependency[0]
            dependent = dependency[2]

            if dependency_type == "root" and dependent == event.text:
                return True
        else:
            return False

class PosTagNotFound(Exception):
    def __init__(self, sentence, word):
        self.sentence = sentence.text
        self.word = word

    def __str__(self):
        return repr("Could not find POS tag for word %s in sentence: %s" % (self.word, self.sentence))
