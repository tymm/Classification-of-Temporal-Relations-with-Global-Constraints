from Data import Data
from System import System
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from time import time
from operator import itemgetter
import numpy as np

# Utility function to report best scores
def report(grid_scores, n_top=3):
    top_scores = sorted(grid_scores, key=itemgetter(1), reverse=True)[:n_top]
    for i, score in enumerate(top_scores):
        print("Model with rank: {0}".format(i + 1))
        print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
              score.mean_validation_score,
              np.std(score.cv_validation_scores)))
        print("Parameters: {0}".format(score.parameters))
        print("")


data = Data()
data.training = TrainingSet(False, False, "data/training/TBAQ-cleaned/TimeBank/")

system = System(data)

system.use_all_features()
system.use_feature_selection()
system.create_features()

training_ee = system.training_event_event
test_ee = system.test_event_event

training_et = system.training_event_timex
test_et = system.test_event_timex

clf = SVC()

param_grid = {"C": [1, 10, 100, 1000],
              "kernel" : ["linear", "poly"],
              "gamma" : [0.001, 0.0001, 0.0],
              "class_weight": ["auto", None],
              "degree" : [1,2,3,4]}

# run grid search
start = time()
grid_search = GridSearchCV(clf, param_grid=param_grid, n_jobs=-1)
grid_search.fit(training_ee[0], training_ee[1])

print("GridSearchCV took %.2f seconds for %d candidate parameter settings." % (time() - start, len(grid_search.grid_scores_)))
report(grid_search.grid_scores_)

start = time()
grid_search = GridSearchCV(clf, param_grid=param_grid, n_jobs=-1)
grid_search.fit(training_et[0], training_et[1])

print("GridSearchCV took %.2f seconds for %d candidate parameter settings." % (time() - start, len(grid_search.grid_scores_)))
report(grid_search.grid_scores_)
