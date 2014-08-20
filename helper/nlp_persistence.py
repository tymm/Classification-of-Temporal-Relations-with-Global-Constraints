import logging
from helper.stanfordnlp.client import StanfordNLP
from helper.stanfordnlp.jsonrpc import RPCTransportError
import cPickle as pickle

class Nlp_persistence:
    """Persistence layer for having fast access to information produced by the StanfordCoreNLP tool."""
    def __init__(self):
        self.FILE = "nlp_infos.p"
        self.data = None

    def create_persistence(self, relations):
        data = {}

        # Create nlp information for all relevant sentences
        for relation in relations:
            if not relation.source.sentence in data:
                self._update_data(relation.source, data)

            if not relation.target.sentence in data:
                self._update_data(relation.target, data)

        print "Done!"
        # Save data to a file
        pickle.dump(data, open(self.FILE, "wb"))

    def _update_data(self, entity, data):
        sentence_obj = entity.sentence
        print sentence_obj.text

        data.update({sentence_obj: self._get_tree(sentence_obj.text)})

    def load(self):
        data = pickle.load(open(self.FILE, "rb"))
        self.data = data

    def get_info_for_sentence(self, sentence):
        if self.data:
            try:
                return self.data[sentence]
            except KeyError:
                logging.error("Nlp_persistence: This sentence is not a key")
        else:
            logging.error("You have to use Nlp_persistence.load() before you can get the information of a sentence")

    def _get_tree(self, text):
        nlp = StanfordNLP()

        b = True
        while b:
            b = False
            try:
                tree = nlp.parse(unicode(text))
            except RPCTransportError:
                logging.info("RPCTransportError in Nlp_persistence")
                b = True

        return tree
