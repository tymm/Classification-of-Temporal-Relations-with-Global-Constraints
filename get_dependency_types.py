from helper.nlp_persistence import Nlp_persistence
from Set import Set

data = Set(False, "data/training/TE3-Silver-data/", "data/training/TBAQ-cleaned/AQUAINT/", "data/training/TBAQ-cleaned/TimeBank/", "data/test/te3-platinum/")

with Nlp_persistence() as nlp_cache:
    nlp_cache.load()

    dependencies = set()

    for text_obj in data.text_objects:
        text_structure = text_obj.text_structure
        sentences = [s for s in text_structure.structure]

        for sentence in sentences:
            collapsed_dependencies = nlp_cache.get_info_for_sentence(sentence)['sentences'][0]['dependencies']

            for dependency in collapsed_dependencies:
                dependencies.add(dependency[0])

            print "Next sentence"

    print dependencies
