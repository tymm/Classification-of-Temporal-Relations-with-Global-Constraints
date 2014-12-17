from Data import Data
from System import System
from TrainingSet import TrainingSet
import pickle

def run(data):
    system = System(data)

    system.use_all_features()
    system.use_feature_selection()

    system.create_features()
    system.train()
    system.eval(quiet=True)

    return system.evaluation_accuracy_event_event, system.evaluation_accuracy_event_timex

def get_different_training_data():
    sets = {}

    timebank = Data()
    timebank.training = TrainingSet(False, False, "data/training/TBAQ-cleaned/TimeBank/")
    sets["TimeBank"] = timebank

    tbaq = Data(inverse=False, closure=False)
    sets["TBAQ"] = tbaq

    tbaq_i = Data(inverse=True, closure=False)
    sets["TBAQ-I"] = tbaq_i

    tbaq_ic = Data(inverse=True, closure=True)
    sets["TBAQ-IC"] = tbaq_ic

    return sets

if __name__ == "__main__":
    accs = {}
    datas = get_different_training_data()

    for data in datas.items():
        accs[data[0]] = run(data[1])

    pickle.dump(accs, open("datasets_eval.p", "wb"))
    print accs
