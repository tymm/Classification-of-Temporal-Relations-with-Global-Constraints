from parsexml.relationtype import RelationType
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from collections import namedtuple

class Result:
    def __init__(self, y_test_truth, y_test_predicted):
        """Arguments: True y values of test set, predicted y values of test set."""
        self.truth = y_test_truth
        self.predicted = y_test_predicted

    def __str__(self):
        """
        output =  "Class: BEFORE  IS_INCLUDED  AFTER  INCLUDES  ENDS  ENDED_BY  IBEFORE  IAFTER  SIMULTANEOUS  BEGINS  BEGUN_BY  DURING  DURING_INV  IDENTITY  NONE\n"
        output += "Precision: %s  %s           %s     %s        %s    %s        %s       %s      %s            %s      %s        %s      %s          %s        %s\n" % (self.get_precision(RelationType.BEFORE), self.get_precision(RelationType.IS_INCLUDED), self.get_precision(RelationType.AFTER), self.get_precision(RelationType.INCLUDES), self.get_precision(RelationType.ENDS), self.get_precision(RelationType.ENDED_BY), self.get_precision(RelationType.IBEFORE), self.get_precision(RelationType.IAFTER), self.get_precision(RelationType.SIMULTANEOUS), self.get_precision(RelationType.BEGINS), self.get_precision(RelationType.BEGUN_BY), self.get_precision(RelationType.DURING), self.get_precision(RelationType.DURING_INV), self.get_precision(RelationType.IDENTITY), self.get_precision(RelationType.NONE))
        output += "Recall:    %s  %s           %s     %s        %s    %s        %s       %s      %s            %s      %s        %s      %s          %s        %s\n" % (self.get_recall(RelationType.BEFORE), self.get_recall(RelationType.IS_INCLUDED), self.get_recall(RelationType.AFTER), self.get_recall(RelationType.INCLUDES), self.get_recall(RelationType.ENDS), self.get_recall(RelationType.ENDED_BY), self.get_recall(RelationType.IBEFORE), self.get_recall(RelationType.IAFTER), self.get_recall(RelationType.SIMULTANEOUS), self.get_recall(RelationType.BEGINS), self.get_recall(RelationType.BEGUN_BY), self.get_recall(RelationType.DURING), self.get_recall(RelationType.DURING_INV), self.get_recall(RelationType.IDENTITY), self.get_recall(RelationType.NONE))
        output += "F1-Score:  %s  %s           %s     %s        %s    %s        %s       %s      %s            %s      %s        %s      %s          %s        %s\n" % (self.get_f1(RelationType.BEFORE), self.get_f1(RelationType.IS_INCLUDED), self.get_f1(RelationType.AFTER), self.get_f1(RelationType.INCLUDES), self.get_f1(RelationType.ENDS), self.get_f1(RelationType.ENDED_BY), self.get_f1(RelationType.IBEFORE), self.get_f1(RelationType.IAFTER), self.get_f1(RelationType.SIMULTANEOUS), self.get_f1(RelationType.BEGINS), self.get_f1(RelationType.BEGUN_BY), self.get_f1(RelationType.DURING), self.get_f1(RelationType.DURING_INV), self.get_f1(RelationType.IDENTITY), self.get_f1(RelationType.NONE))
        output += "Accuracy:  %s  %s           %s     %s        %s    %s        %s       %s      %s            %s      %s        %s      %s          %s        %s\n" % (self.get_accuracy(RelationType.BEFORE), self.get_accuracy(RelationType.IS_INCLUDED), self.get_accuracy(RelationType.AFTER), self.get_accuracy(RelationType.INCLUDES), self.get_accuracy(RelationType.ENDS), self.get_accuracy(RelationType.ENDED_BY), self.get_accuracy(RelationType.IBEFORE), self.get_accuracy(RelationType.IAFTER), self.get_accuracy(RelationType.SIMULTANEOUS), self.get_accuracy(RelationType.BEGINS), self.get_accuracy(RelationType.BEGUN_BY), self.get_accuracy(RelationType.DURING), self.get_accuracy(RelationType.DURING_INV), self.get_accuracy(RelationType.IDENTITY), self.get_accuracy(RelationType.NONE))

        output += "\n"
        """
        output = ""
        output += "Averaged f1-score: %s\n" % f1_score(self.truth, self.predicted)
        output += "Averaged accuracy: %s\n" % accuracy_score(self.truth, self.predicted)
        self._print_dristibution()

        return output

    def get_precision(self, c):
        """Return precision for class c."""
        tp, fp, fn, tn = self._get_table(c)

        try:
            return tp/float(tp+fp)
        except ZeroDivisionError:
            return 0

    def get_recall(self, c):
        """Return recall for class c."""
        tp, fp, fn, tn = self._get_table(c)

        try:
            return tp/float(tp+fn)
        except ZeroDivisionError:
            return 0

    def get_f1(self, c):
        """Return recall for class c."""

        recall = self.get_recall(c)
        precision = self.get_precision(c)

        try:
            return 2*recall*precision/float(precision+recall)
        except ZeroDivisionError:
            return 0

    def get_accuracy(self, c):
        """Return accuracy for class c."""
        tp, fp, fn, tn = self._get_table(c)

        try:
            return (tp + tn)/float(tp+tn+fp+fn)
        except ZeroDivisionError:
            return 0

    def _get_table(self, c):
        """Return table (tp, fp, fn, tn) for class c."""
        y_truth = list(self.truth)
        y_predicted = list(self.predicted)

        # c = 1, other classes = 0
        self._make_binary(truth)
        self._make_binary(predicted)

        tp = fp = fn = tn = 0
        for i, predicted in enumerate(y_predicted):
            if predicted == c and predicted == y_truth[i]:
                # Recognized as c and it is c
                tp += 1

            if predicted != c and predicted != y_truth[i]:
                # Not recognized as c but actually c
                fn += 1

            if predicted == c and predicted != y_truth[i]:
                # Recognized as c but it is not c
                fp += 1

            if predicted != c and predicted == y_truth[i]:
                # Recognized as not c which is the truth
                tn += 1

        return (tp, fp, fn, tn)

    def _make_binary(data, c):
        for i, d in enumerate(data):
            if d == c:
                data[i] = 1
            else:
                data[i] = 0

    def _print_dristibution(self):
        Row = namedtuple("Row", ["Class", "TP", "FP", "FN"])

        rows = []
        for rel_type in RelationType():
            tp, fp, fn, tn = self._get_table(rel_type)
            row = Row(RelationType.get_string_by_id(rel_type), tp, fp, fn)
            rows.append(row)

        self._pprinttable(rows)

    # From here: http://stackoverflow.com/questions/5909873/python-pretty-printing-ascii-tables
    def _pprinttable(self, rows):
        if len(rows) > 1:
            headers = rows[0]._fields
            lens = []
            for i in range(len(rows[0])):
                lens.append(len(max([x[i] for x in rows] + [headers[i]],key=lambda x:len(str(x)))))
            formats = []
            hformats = []
            for i in range(len(rows[0])):
                if isinstance(rows[0][i], int):
                    formats.append("%%%dd" % lens[i])
                else:
                    formats.append("%%-%ds" % lens[i])
                hformats.append("%%-%ds" % lens[i])
            pattern = " | ".join(formats)
            hpattern = " | ".join(hformats)
            separator = "-+-".join(['-' * n for n in lens])
            print hpattern % tuple(headers)
            print separator
            for line in rows:
                print pattern % tuple(line)
        elif len(rows) == 1:
            row = rows[0]
            hwidth = len(max(row._fields,key=lambda x: len(x)))
            for i in range(len(row)):
                print "%*s = %s" % (hwidth,row._fields[i],row[i])
