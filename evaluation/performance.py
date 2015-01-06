from Data import Data
from System import System
import time
import pickle
from os import listdir

STEPS_RELATIONS = 15

def measure_time(data):
    start = time.time()

    system = System(data)
    system.use_all_features()
    system.use_feature_selection()

    system.create_features()
    system.train()
    system.save_classifiers()

    system.eval()
    system.create_confidence_scores()
    system.apply_global_model()

    end = time.time()

    return end-start

def create_data():
    training_files = _get_training_files()
    series_training_files = _get_series_of_files(training_files)

    data = []
    for series in series_training_files:
        data.append(Data(series))

    return data

def _get_training_files():
    aquaint = listdir("data/training/TBAQ-cleaned/AQUAINT/")
    timebank = listdir("data/training/TBAQ-cleaned/TimeBank/")

    return aquaint + timebank

def _get_series_of_files(training_files):
    length = len(training_files)
    len_part = length/STEPS_RELATIONS

    lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

    parts = lol(training_files, len_part)

    series = []
    for i in range(STEPS_RELATIONS):
        s = []
        for j in range(i+1):
            s += parts[j]

        series.append(s)

    return series

def get_number_of_training_relations(data):
    return len(data.training.relations)

def save_time_relations_data():
    rels_time = {}

    for data in create_data():
        num_relations = get_number_of_relations(data)
        time = measure_time(data)

        rels_time[num_relations] = time

    pickle.dump(rels_time, open("rels_time.p", "wb"))

if __name__ == "__main__":
    save_time_relations_data()
