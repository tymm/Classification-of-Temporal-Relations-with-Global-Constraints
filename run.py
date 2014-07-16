from TrainingSet import TrainingSet
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

if __name__ == "__main__":
    # Creating xml mapping objects from scratch with "False" as first argument
    load = False

    if load:
        print "Loading training and test set"
    else:
        print "Creating training and test set"

    training = TrainingSet(load, "data/training/TE3-Silver-data/", "data/training/TBAQ-cleaned/AQUAINT/", "data/training/TBAQ-cleaned/TimeBank/")
    test = TrainingSet(load, "data/test/te3-platinum/")

    if load:
        print "Done loading training and test set"
    else:
        print "Done creating training and test set"

    print "Creating features"
    X_train, y_train = training.get_classification_data_event_event()
    X_test, y_test = test.get_classification_data_event_event()
    print "Done creating features"

    # Train a random forest classifier
    print "Train the classifier"
    rf = RandomForestClassifier(n_jobs=2, n_estimators=50)
    rf.fit(X_train, y_train)
    print "Done training the classifier"

    y_predicted = rf.predict(X_test)

    print "Accuracy"
    print rf.score(X_test, y_test)
    print
    print "F1-Score"
    print f1_score(y_test, y_predicted)
