from Data import Data

if __name__ == "__main__":
    data = Data(inverse=True, closure=True)

    training_event_event = 0
    training_event_timex = 0

    test_event_event = 0
    test_event_timex = 0

    for text_obj in data.training.text_objects:
        for relation in text_obj.relations:
            if relation.is_event_event():
                training_event_event += 1
            elif relation.is_event_timex():
                training_event_timex += 1

    for text_obj in data.test.text_objects:
        for relation in text_obj.relations:
            if relation.is_event_event():
                test_event_event += 1
            elif relation.is_event_timex():
                test_event_timex += 1

    print "training event-event: " + str(training_event_event)
    print "training event-timex: " + str(training_event_timex)

    print "test event-event: " + str(test_event_event)
    print "test event-timex: " + str(test_event_timex)
