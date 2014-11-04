from TrainingSet import TrainingSet
from System import System
from Data import Data

class LatexTable:
    def __init__(self, *trainings):
        self.training_data = trainings

        self._print_table()

    def _print_table(self):
        print "\\begin{center}"
        print "\t\\small"
        print "\t\\begin{tabular}{|c|c|c|}"
        print "\t\t\\hline"
        print "\t\t\\textbf{Training data} & \\textbf{event-event} & \\textbf{event-timex} \\\\"
        print "\t\t\\hline"

        for training in self.training_data:
            print "\t\t%s & %.2f% & %.2f% \\\\" % (training.name, self._make_percentage(training.result_event_event), self._make_percentage(training.result_event_timex))
            print "\t\t\\hline"

        print "\t\\end{tabular}"
        print "\\end{center}"

    def _make_percentage(self, value):
        percentage = value*100
        return percentage

class Run:
    def __init__(self, name, inverse, closure, *corpora):
        self.training = TrainingSet(inverse, closure, *corpora)
        self.name = name

        self.result_event_event = None
        self.result_event_timex = None

        self._run()

    def _run(self):
        data = Data()
        data.training = self.training

        system = System(data)
        system.use_best_feature_set()
        system.create_features()
        system.train()
        system.eval(quiet=True)

        self.result_event_event = system.evaluation_accuracy_event_event
        self.result_event_timex = system.evaluation_accuracy_event_timex


if __name__ == "__main__":
    TB = Run("Timebank", False, False, "data/training/TBAQ-cleaned/TimeBank/")
    TBAQ = Run("TBAQ", False, False, "data/training/TBAQ-cleaned/TimeBank/", "data/training/TBAQ-cleaned/AQUAINT/")
    TBAQ_Inverse = Run("TBAQ-I", True, False, "data/training/TBAQ-cleaned/TimeBank/", "data/training/TBAQ-cleaned/AQUAINT/")
    TBAQ_Inverse_Closure = Run("TBAQ-IC", True, True, "data/training/TBAQ-cleaned/TimeBank/", "data/training/TBAQ-cleaned/AQUAINT/")

    latex = LatexTable(TB, TBAQ, TBAQ_Inverse, TBAQ_Inverse_Closure)
