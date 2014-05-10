import os

class parser:
    def __init__(self, *corpora):
        self.corpora = corpora
        self._parse(self.corpora)

    def _parse(self, corpora):
        # Holds all corpora files
        files = []
        for corpus in corpora:
            files = files + self._fetch_files(corpus)

    def _fetch_files(self, directory):
        files = []

        # Append '/' if there is no at the end of directory string
        if not directory.endswith('/'):
            directory = directory + '/'

        for file in os.listdir(directory):
            files.append(directory + file)

        return files


if __name__ == "__main__":
    a = parser("data/training/TE3-Silver-data/", "data/training/TBAQ-cleaned/AQUAINT/", "data/training/TBAQ-cleaned/TimeBank/")
