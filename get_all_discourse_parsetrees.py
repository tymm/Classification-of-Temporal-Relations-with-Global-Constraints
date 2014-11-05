from Data import Data
import cPickle as pickle
from helper.nlp_persistence import Nlp_persistence
import subprocess
import os

class Wrapper:
    def __init__(self, parsetree):
        self.executable = "addDiscourse.pl"

        self.temp_file = self._create_temp_file(parsetree)

        # Execute addDiscourse perl script
        p = subprocess.Popen(["perl", self.executable, "--parses", self.temp_file], stdout=subprocess.PIPE)
        # Get output
        self.result = p.communicate()[0]

        # Delete file
        self._del_temp_file(self.temp_file)

    def _create_temp_file(self, text):
        f = open("tmp.txt", "w")
        f.write(text)
        f.close()

        return "tmp.txt"

    def _del_temp_file(self, filename):
        os.remove(filename)

def get_discourse_parsetree(parsetree):
    wrapper = Wrapper(parsetree)
    return wrapper.result

if __name__ == "__main__":
    data = Data()
    nlp_persistence_obj = Nlp_persistence()
    nlp_persistence_obj.load()

    d = {}
    for text_obj in data.training.text_objects + data.test.text_objects:
        for event in text_obj.events:
            parsetree = nlp_persistence_obj.get_parse_tree(event.sentence)
            discourse_parsetree = get_discourse_parsetree(parsetree)
            print discourse_parsetree

            d[event.sentence] = discourse_parsetree

    pickle.dump(d, open("discourse_cache.p", "wb"))
