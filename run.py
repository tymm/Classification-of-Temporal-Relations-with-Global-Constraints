from TrainingSet import TrainingSet
from TestSet import TestSet
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from feature.lemma import Lemma
from feature.token import Token

if __name__ == "__main__":
    # Creating xml mapping objects from scratch with "False" as first argument
    load = False

    if load:
        print "Loading training and test set"
    else:
        print "Creating training and test set"

    training = TrainingSet(load, "data/training/TE3-Silver-data/", "data/training/TBAQ-cleaned/AQUAINT/", "data/training/TBAQ-cleaned/TimeBank/")
    #test = TestSet(load, "data/test/te3-platinum/AP_20130322.tml")

    # Must be called before training.get_classification_data_event_event()
    lemma = Lemma(training)
    token = Token(training)

    if load:
        print "Done loading training and test set"
    else:
        print "Done creating training and test set"

    print "Creating features"
    X_train, y_train = training.get_classification_data_event_event(lemma, token)
    print "Done creating features"
    print

    # Train a random forest classifier
    print "Train the classifier"
    rf = RandomForestClassifier(n_jobs=2, n_estimators=5)
    rf.fit(X_train, y_train)
    print "Done training the classifier"
    print

    print "Creating confidence scores in test set"
    test.create_confidence_scores(rf)
    print "Done creating confidence scores"
    print

    print "Searching for the best solution"
    test.find_best_set_of_relations()
    print "Done searching for the best solution"
