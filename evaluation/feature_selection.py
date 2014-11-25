from sklearn.feature_selection import RFECV
from sklearn import linear_model
from Data import Data
from System import System
from TrainingSet import TrainingSet

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

    estimator = linear_model.LinearRegression()
    selector = RFECV(estimator, step=1, cv=5)
    selector = selector.fit(X_timex, y_timex)

    print selector.ranking_
