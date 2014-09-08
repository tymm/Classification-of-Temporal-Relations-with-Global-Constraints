import logging
import cPickle as pickle
from corenlp import StanfordCoreNLP

class Nlp_persistence:
    """Persistence layer for having fast access to information produced by the StanfordCoreNLP tool."""
    def __init__(self):
        self.FILE = "nlp_infos.p"
        self.data = None
        self.corenlp_dir = "helper/stanfordnlp/corenlp-python/stanford-corenlp-full-2013-11-12/"
        self.corenlp = StanfordCoreNLP(self.corenlp_dir)

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
            except IOError:
                logging.warning("No cached nlp data.")

                self.data = {}
                return self.data
            finally:
                self.data = data

        return self.data

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
                self._write()

                return tree
        else:
            logging.error("You have to use Nlp_persistence.load() before you can get the information of a sentence")
            return None

    def _write(self):
        # Save data to a file
        pickle.dump(self.data, open(self.FILE, "wb"))

    def _get_tree(self, sentence):
        tree = self.corenlp.raw_parse(sentence.text)
        return tree
