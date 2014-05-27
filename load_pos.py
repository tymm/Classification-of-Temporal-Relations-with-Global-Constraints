import cPickle as pickle
from sets import Set

def load_pos_tags():
    text_objs = None
    pos_tags = Set()

    try:
        text_objs = pickle.load(open("data.p", "rb"))
    except IOError:
        print "Please first load entity information by running run.py"

    for _, text_obj in text_objs.items():
        for event in text_obj.events:
            pos_tags.add(event.pos)

    return pos_tags

def save_pos_tags(tags):
    # Set -> Dict = { "NN": 0, "VB": 1, ... }
    tags_d = {}

    tags = list(tags)
    for i, tag in enumerate(tags):
        tags_d.update({tag: i})

    pickle.dump(tags_d, open("pos_tags.p", "wb"))

if __name__ == "__main__":
    # Saving all pos tags available
    tags = load_pos_tags()
    save_pos_tags(tags)
