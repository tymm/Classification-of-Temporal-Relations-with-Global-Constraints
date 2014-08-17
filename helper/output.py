from shutil import copyfile
from lxml import etree
import os
from parsexml.event import Event
from parsexml.timex import Timex
from parsexml.relationtype import RelationType

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
                    tlink = etree.Element("TLINK", eventInstanceID=relation.source.eid, relatedToEventInstance=relation.target.eid)
                elif type(relation.source) == Timex and type(relation.target) == Timex:
                    # Both entities are Timex
                    tlink = etree.Element("TLINK", timeID=relation.source.tid, relatedToTime=relation.target.tid)
                elif type(relation.source) == Event and type(relation.target) == Timex:
                    # The target entity is a Timex
                    tlink = etree.Element("TLINK", eventInstanceID=relation.source.eid, relatedToTime=relation.target.tid)
                elif type(relation.source) == Timex and type(relation.target) == Event:
                    # The source entity is a Timex
                    tlink = etree.Element("TLINK", timeID=relation.source.tid, relatedToEventInstance=relation.target.eid)

                tlink.attrib["lid"] = relation.lid
                tlink.attrib["relType"] = RelationType.get_string_by_id(relation.relation_type)

                root.append(tlink)

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
        parser = etree.XMLParser(remove_blank_text=True)
        self.tree = etree.parse(self.output_file, parser=parser)

        for tlink in self.tree.xpath("//TLINK"):
            tlink.getparent().remove(tlink)

