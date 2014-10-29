from shutil import copyfile
from lxml import etree
import os
from parsexml.event import Event
from parsexml.timex import Timex
from parsexml.relationtype import RelationType
import logging

class Output:
    def __init__(self, filename):
        self.OUTPUT_DIR = "output/"
        self.original_file = filename

        self.tree = None
        self.output_file = self._copy_to_output_dir()
        self._remove_relations()

    def create_relations(self, relations):
        root = self.tree.getroot()

        for relation in relations:
            if RelationType.get_string_by_id(relation.relation_type) != "NONE":
                # Don't create NONE links
                if type(relation.source) == Event and type(relation.target) == Event:
                    # Both entities are Events
                    tlink = etree.Element("TLINK", eventInstanceID=relation.source.eiid[0], relatedToEventInstance=relation.target.eiid[0])
                elif type(relation.source) == Timex and type(relation.target) == Timex:
                    # Both entities are Timex
                    tlink = etree.Element("TLINK", timeID=relation.source.tid, relatedToTime=relation.target.tid)
                elif type(relation.source) == Event and type(relation.target) == Timex:
                    # The target entity is a Timex
                    tlink = etree.Element("TLINK", eventInstanceID=relation.source.eiid[0], relatedToTime=relation.target.tid)
                elif type(relation.source) == Timex and type(relation.target) == Event:
                    # The source entity is a Timex
                    tlink = etree.Element("TLINK", timeID=relation.source.tid, relatedToEventInstance=relation.target.eiid[0])

                tlink.attrib["lid"] = relation.lid

                # If there is a prediction for this relation, append it to xml file
                if relation.predicted_class is not None:
                    tlink.attrib["relType"] = RelationType.get_string_by_id(relation.predicted_class)
                    root.append(tlink)
                else:
                    logging.warning("Creating output files without having class predictions for relations!")

    def write(self):
        self.tree.write(self.output_file, xml_declaration=True, pretty_print=True)

    def _copy_to_output_dir(self):
        # Copy .tml file to output directory
        try:
            copyfile(self.original_file, self.OUTPUT_DIR + self.original_file)
        except IOError:
            path_to_original = "/".join(self.original_file.split("/")[:-1])
            path = self.OUTPUT_DIR + path_to_original
            os.makedirs(path)
            # Once again
            copyfile(self.original_file, self.OUTPUT_DIR + self.original_file)

        return self.OUTPUT_DIR + self.original_file

    def _remove_relations(self):
        """Removing all relations from the output file."""
        self.tree = etree.parse(self.output_file)

        for tlink in self.tree.xpath("//TLINK"):
            tlink.getparent().remove(tlink)

