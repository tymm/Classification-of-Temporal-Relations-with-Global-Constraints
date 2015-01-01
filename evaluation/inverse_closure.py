from TrainingSet import TrainingSet

if __name__ == "__main__":
    test_plain = TrainingSet(False, False, "data/test/te3-platinum/")
    test_inverse_closure = TrainingSet(True, True, "data/test/te3-platinum/")
    test_closure = TrainingSet(False, True, "data/test/te3-platinum/")

    print "Number of relations: " + str(len(test_plain))
    print "Number of relations for closure: " + str(len(test_closure))
    print "Number of relations for inverse and closure: " + str(len(test_inverse_closure))
