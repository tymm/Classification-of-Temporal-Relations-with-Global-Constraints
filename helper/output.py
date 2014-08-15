from shutil import copyfile
from lxml import etree
import os

class Output:
    def __init__(self, filename):
        self.OUTPUT_DIR = "output/"
        self.original_file = filename

        self.tree = None
        self.output_file = self._copy_to_output_dir()
        self._remove_relations()

    def create_relations(self, relations):
        pass

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

