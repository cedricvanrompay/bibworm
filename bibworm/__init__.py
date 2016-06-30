# standard libraries
import subprocess

# 3rd party libs
import requests
import yaml
from bs4 import BeautifulSoup

class Entry:
    def __init__(self, dblpid=None, bib=None, metadata=None):
        self.dblpid = dblpid

        if bib:
            self.bib = bib
        else:
            url = 'http://dblp.uni-trier.de/rec/bib/'+dblpid
            self.bib = requests.get(url).text.split('\n\n')[0]

        if metadata:
            self.metadata = metadata
        else:
            url = 'http://dblp.uni-trier.de/rec/xml/'+dblpid
            xml = BeautifulSoup(requests.get(url).text, "lxml")
            self.metadata = {
                'title': xml.title.get_text(),
                'authors': [node.get_text()
                            for node in xml.find_all('author')
                            ],
                'conference': xml.booktitle.get_text(),
                'year': int(xml.year.get_text()),
            }


    def __repr__(self):
        return "Entry('{}')".format(self.dblpid)

    def __str__(self):
        return '\n'.join([
            self.metadata['title'],
            ' and '.join(self.metadata['authors']),
            '{} {}'.format(
                self.metadata['conference'],
                self.metadata['year']
            )
        ])

def open_pdf(path_to_pdf):
    subprocess.Popen(['evince', path_to_pdf],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
