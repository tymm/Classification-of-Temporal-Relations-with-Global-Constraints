from sklearn.feature_selection import RFECV
from sklearn import linear_model
from Data import Data
from System import System
from TrainingSet import TrainingSet
import pickle

if __name__ == "__main__":
    data = Data()
    data.training = TrainingSet(False, False, "data/training/TBAQ-cleaned/TimeBank/")

    system = System(data)
    system.use_all_features()
    system.create_features()

    X_event, y_event = system.training_event_event
    X_timex, y_timex = system.training_event_timex

    estimator = linear_model.LinearRegression()
    selector = RFECV(estimator, step=1, cv=5)
    selector = selector.fit(X_event, y_event)

    print selector.ranking_
    print selector.n_features_
    pickle.dump(selector.ranking_, open("selector_ee.p", "wb"))
    pickle.dump(selector.n_features_, open("selector_n_features_ee.p", "wb"))
    pickle.dump(selector, open("selector_object_ee.p", "wb"))

    estimator = linear_model.LinearRegression()
    selector = RFECV(estimator, step=1, cv=5)
    selector = selector.fit(X_timex, y_timex)
    pickle.dump(selector.ranking_, open("selector_et.p", "wb"))
    pickle.dump(selector.n_features_, open("selector_n_features_et.p", "wb"))
    pickle.dump(selector, open("selector_object_et.p", "wb"))

    print selector.ranking_
    print selector.n_features_
