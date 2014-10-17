from parsexml.relationtype import RelationType
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from collections import namedtuple
from tabulate import tabulate

class Result:
    def __init__(self, y_test_truth, y_test_predicted):
        """Arguments: True y values of test set, predicted y values of test set."""
        self.truth = y_test_truth
        self.predicted = y_test_predicted

    def __str__(self):
        output = ""
        output += "Averaged f1-score: %s\n" % f1_score(self.truth, self.predicted)
        output += "Averaged accuracy: %s\n" % accuracy_score(self.truth, self.predicted)
        self._print_detailed_results()
        self._print_dristibution()

        return output

    def _print_detailed_results(self):
        table = []
        header = ["Class", "Precision", "Recall", "F1-Score", "Accuracy"]
        table.append(header)

        for rel_type in RelationType():
            tp, fp, fn, tn = self._get_table(rel_type)
            row = [RelationType.get_string_by_id(rel_type)]
            row.append(self.get_precision(rel_type))
            row.append(self.get_recall(rel_type))
            row.append(self.get_f1(rel_type))
            row.append(self.get_accuracy(rel_type))
            table.append(row)

        print tabulate(table)

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

        # c => 1, other classes => 0
        self._make_binary(y_truth, c)
        self._make_binary(y_predicted, c)

        tp = fp = fn = tn = 0
        for i, predicted in enumerate(y_predicted):
            if predicted == 1 and predicted == y_truth[i]:
                # Recognized as c and it is c
                tp += 1

            if predicted != 1 and predicted != y_truth[i]:
                # Not recognized as c but actually c
                fn += 1

            if predicted == 1 and predicted != y_truth[i]:
                # Recognized as c but it is not c
                fp += 1

            if predicted != 1 and predicted == y_truth[i]:
                # Recognized as not c which is the truth
                tn += 1

        return tp, fp, fn, tn

    def _make_binary(self, data, c):
        for i, d in enumerate(data):
            if d == c:
                data[i] = 1
            else:
                data[i] = 0

    def _print_dristibution(self):
        table = []
        header = ["Class", "TP", "FP", "FN"]
        table.append(header)

        for rel_type in RelationType():
            tp, fp, fn, tn = self._get_table(rel_type)
            row = [RelationType.get_string_by_id(rel_type), tp, fp, fn]
            table.append(row)

        print tabulate(table)
