from Data import Data
from System import System
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from time import time
from operator import itemgetter

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
system = System(data)

system.use_best_feature_set()
system.create_features()

training = system.training_event_event
test = system.test_event_event

clf = SVC()

param_grid = {"C": [1, 10, 100, 1000],
              "kernel" : ["linear", "poly"],
              "gamma" : [0.001, 0.0001, 0.0],
              "class_weight": ["auto", None],
              "degree" : [1,2,3,4]}

# run grid search
start = time()
grid_search = GridSearchCV(clf, param_grid=param_grid)
grid_search.fit(training[0], training[1])

print("GridSearchCV took %.2f seconds for %d candidate parameter settings." % (time() - start, len(grid_search.grid_scores_)))
report(grid_search.grid_scores_)
