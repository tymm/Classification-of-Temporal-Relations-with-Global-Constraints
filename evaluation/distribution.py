from TrainingSet import TrainingSet
from parsexml.relationtype import RelationType

class LatexTable:
    def __init__(self, tb, tbaq, tbaq_i, tbaq_ic, test):
        self.tb_event_event = tb.count_event_event
        self.tb_event_timex = tb.count_event_timex

        self.tbaq_event_event = tbaq.count_event_event
        self.tbaq_event_timex = tbaq.count_event_timex

        self.tbaq_i_event_event = tbaq_i.count_event_event
        self.tbaq_i_event_timex = tbaq_i.count_event_timex

        self.tbaq_ic_event_event = tbaq_ic.count_event_event
        self.tbaq_ic_event_timex = tbaq_ic.count_event_timex

        self.test_event_event = test.count_event_event
        self.test_event_timex = test.count_event_timex

    def print_table(self):
        print "\\begin{center}"
        print "\t\\tiny"
        print "\t\\begin{tabular}{| l | l | l | l | l | l || l | l | l | l | l |}"
        print "\t\t\hline"
        print "\t\t\\multirow{3}{*}{\\textbf{Relations}} & \\multicolumn{5}{|c||}{\\textbf{event-event}} & \\multicolumn{5}{|c|}{\\textbf{event-timex}} \\\\"
        print "\t\t\\cline{2-11}"
        print "\t\t& \\multicolumn{4}{|c|}{training} & \\multicolumn{1}{c||}{test} & \\multicolumn{4}{|c|}{training} & \\multicolumn{1}{|c|}{test} \\\\"
        print "\t\t\\cline{2-11}"
        print "\t\t& TB & TBAQ & TBAQ-I & TBAQ-IC & TE3-P & TB & TBAQ & TBAQ-I & TBAQ-IC & TE3-P \\\\"
        print "\t\t\\hline"

        for rel_type in RelationType():
            print "\t\t%s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s \\\\" % (RelationType.get_string_by_id(rel_type), self.tb_event_event[rel_type], self.tbaq_event_event[rel_type], self.tbaq_i_event_event[rel_type], self.tbaq_ic_event_event[rel_type], self.test_event_event[rel_type], self.tb_event_timex[rel_type], self.tbaq_event_timex[rel_type], self.tbaq_i_event_timex[rel_type], self.tbaq_ic_event_timex[rel_type], self.test_event_timex[rel_type])
            print "\t\t\\hline"

        print "\t\t%s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s \\\\" % ("Total", self.tb_event_event["all"], self.tbaq_event_event["all"], self.tbaq_i_event_event["all"], self.tbaq_ic_event_event["all"], self.test_event_event["all"], self.tb_event_timex["all"], self.tbaq_event_timex["all"], self.tbaq_i_event_timex["all"], self.tbaq_ic_event_timex["all"], self.test_event_timex["all"])

        print "\t\\end{tabular}"
        print "\\end{center}"


class Distribution:
    def __init__(self, name, inverse, closure, *corpora):
        self.data = TrainingSet(inverse, closure, *corpora)
        self.name = name

        self.count_event_event = self._count_event_event_relations()
        self.count_event_timex = self._count_event_timex_relations()

    def _print(self):
        print self.name
        print "event-event"
        for rel_type in RelationType():
            print RelationType.get_string_by_id(rel_type), self.count_event_event[rel_type]

        print "event-timex"
        for rel_type in RelationType():
            print RelationType.get_string_by_id(rel_type), self.count_event_event[rel_type]

    def _count_event_event_relations(self):
        counts = {}
        for rel_type in RelationType():
            counts[rel_type] = 0

        for relation in self.data.relations:
            if relation.is_event_event():
                counts[relation.relation_type] += 1

        all = 0
        for rel_type in RelationType():
            all += counts[rel_type]

        counts["all"] = all

        return counts

    def _count_event_timex_relations(self):
        counts = {}
        for rel_type in RelationType():
            counts[rel_type] = 0

        for relation in self.data.relations:
            if relation.is_event_timex():
                counts[relation.relation_type] += 1

        all = 0
        for rel_type in RelationType():
            all += counts[rel_type]

        counts["all"] = all

        return counts

if __name__ == "__main__":
    TB = Distribution("TB", False, False, "data/training/TBAQ-cleaned/TimeBank/")
    TBAQ = Distribution("TBAQ", False, False, "data/training/TBAQ-cleaned/TimeBank/", "data/training/TBAQ-cleaned/AQUAINT/")
    TBAQ_Inverse = Distribution("TBAQ-I", True, False, "data/training/TBAQ-cleaned/TimeBank/", "data/training/TBAQ-cleaned/AQUAINT/")
    TBAQ_Inverse_Closure = Distribution("TBAQ-IC", True, True, "data/training/TBAQ-cleaned/TimeBank/", "data/training/TBAQ-cleaned/AQUAINT/")
    Test = Distribution("Test", False, False, "data/test/te3-platinum/")

    latex = LatexTable(TB, TBAQ, TBAQ_Inverse, TBAQ_Inverse_Closure, Test)
    latex.print_table()
