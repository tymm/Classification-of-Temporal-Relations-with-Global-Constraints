from Data import Data
from System import System
from TrainingSet import TrainingSet
import pickle
import gc

def run(data):
    system = System(data)

    system.use_all_features()
    system.use_feature_selection()

    system.create_features()
    system.train()
    system.eval(quiet=True)

    return system.evaluation_accuracy_event_event, system.evaluation_accuracy_event_timex

def get_accs():
    accs = {}

    timebank = Data()
    timebank.training = TrainingSet(False, False, "data/training/TBAQ-cleaned/TimeBank/")
    accs["TimeBank"] = run(timebank)
    del timebank
    gc.collect()

    tbaq = Data(inverse=False, closure=False)
    accs["TBAQ"] = run(tbaq)
    del tbaq
    gc.collect()

    tbaq_i = Data(inverse=True, closure=False)
    accs["TBAQ-I"] = run(tbaq_i)
    del tbaq_i
    gc.collect()

    tbaq_ic = Data(inverse=True, closure=True)
    accs["TBAQ-IC"] = run(tbaq_ic)
    del tbaq_ic
    gc.collect()

    return accs

if __name__ == "__main__":

    accs = get_accs()

    pickle.dump(accs, open("datasets_eval.p", "wb"))
    print accs
