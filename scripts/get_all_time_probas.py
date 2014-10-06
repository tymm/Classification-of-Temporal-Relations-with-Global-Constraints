import re
import cPickle as pickle

def parse_info(line):
    infinitive = re.search(r"EVENT\=to (.+?),", line).group(1)

    m = re.search(r"OBJ=(\w+),", line)
    if m:
        obj = m.group(1)
    else:
        obj = None

    m = re.search(r"DISTR\=\[(.*)\]$", line)
    if m:
        probas = m.group(1)
        probas = probas.strip(";").split(";")

        likelihoods = []
        for proba in probas:
            likelihoods.append(float(proba))
    else:
        likelihoods = None

    return (infinitive, obj, likelihoods)

def get_time(likelihoods):
    maximum = 0
    for proba in likelihoods:
        if proba > maximum:
            maximum = proba

    return likelihoods.index(maximum)

def get_likelihoods_from_file(filename):
    l = {}

    with open(filename, "r") as f:
        for line in f:
            infinitive, obj, likelihoods = parse_info(line)
            if obj == None and likelihoods:
                l.update({infinitive: get_time(likelihoods)})

    return l

if __name__ == "__main__":
    infinitive_likelihood = get_likelihoods_from_file("../event.lexicon.distributions")
    pickle.dump(infinitive_likelihood, open("../word_likelihoods.p", "wb"), protocol=-1)
