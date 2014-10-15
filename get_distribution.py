from Data import Data
from parsexml.relationtype import RelationType

def number_of_type(event_event, temporal_type):
    count = 0
    for text_obj in data.training.text_objects:
        for relation in text_obj.relations:
            if event_event:
                if relation.is_event_event():
                    if relation.relation_type == temporal_type:
                        count += 1
            else:
                if relation.is_event_timex():
                    if relation.relation_type == temporal_type:
                        count += 1

    return str(count)

if __name__ == "__main__":
    data = Data(inverse=True, closure=False)

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
    print
    print "training event-event distribution:"
    print "BEFORE: " +      number_of_type(True, RelationType.BEFORE)
    print "AFTER: " +       number_of_type(True, RelationType.AFTER)
    print "IBEFORE: " +     number_of_type(True, RelationType.IBEFORE)
    print "IAFTER: " +      number_of_type(True, RelationType.IAFTER)
    print "BEGINS: " +      number_of_type(True, RelationType.BEGINS)
    print "BEGUN_BY: "+     number_of_type(True, RelationType.BEGUN_BY)
    print "ENDS: " +        number_of_type(True, RelationType.ENDS)
    print "ENDED_BY: "+     number_of_type(True, RelationType.ENDED_BY)
    print "DURING: " +      number_of_type(True, RelationType.DURING)
    print "DURING_INV: "+   number_of_type(True, RelationType.DURING_INV)
    print "INCLUDES: " +    number_of_type(True, RelationType.INCLUDES)
    print "IS_INCLUDED: "+  number_of_type(True, RelationType.IS_INCLUDED)
    print "SIMULTANEOUS: "+ number_of_type(True, RelationType.SIMULTANEOUS)
    print "IDENTITY: " +    number_of_type(True, RelationType.IDENTITY)

    print "training event-timex distribution:"
    print "BEFORE: " +       number_of_type(False, RelationType.BEFORE)
    print "AFTER: " +        number_of_type(False, RelationType.AFTER)
    print "IBEFORE: " +      number_of_type(False, RelationType.IBEFORE)
    print "IAFTER: " +       number_of_type(False, RelationType.IAFTER)
    print "BEGINS: " +       number_of_type(False, RelationType.BEGINS)
    print "BEGUN_BY: " +     number_of_type(False, RelationType.BEGUN_BY)
    print "ENDS: " +         number_of_type(False, RelationType.ENDS)
    print "ENDED_BY: " +     number_of_type(False, RelationType.ENDED_BY)
    print "DURING: " +       number_of_type(False, RelationType.DURING)
    print "DURING_INV: " +   number_of_type(False, RelationType.DURING_INV)
    print "INCLUDES: " +     number_of_type(False, RelationType.INCLUDES)
    print "IS_INCLUDED: " +  number_of_type(False, RelationType.IS_INCLUDED)
    print "SIMULTANEOUS: " + number_of_type(False, RelationType.SIMULTANEOUS)
    print "IDENTITY: " +     number_of_type(False, RelationType.IDENTITY)
