from Set import Set
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

if __name__ == "__main__":
    training = Set("data/training/TE3-Silver-data/", "data/training/TBAQ-cleaned/AQUAINT/", "data/training/TBAQ-cleaned/TimeBank/")
    test = Set("data/test/te3-platinum/")

    X_train, y_train = training.get_classification_data_event_event()
    X_test, y_test = test.get_classification_data_event_event()

    # Train a random forest classifier
    rf = RandomForestClassifier(n_jobs=2, n_estimators=100)
    rf.fit(X_train, y_train)

    y_predicted = rf.predict(X_test)

    print "Accuracy"
    print rf.score(X_test, y_test)
    print
    print "F1-Score"
    print f1_score(y_test, y_predicted)
