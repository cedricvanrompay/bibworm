from . import Entry

import os
import shutil

import yaml

METADATA_DIR = os.path.expanduser('~/.bibworm')
PDF_DIR = os.path.expanduser('~/Documents/researchDocs')
PDF_DROP_DIR = os.path.expanduser('~/.bibworm-drop')

def add(entry):
    dropped_list = os.listdir(PDF_DROP_DIR)
    if len(dropped_list) == 0:
        raise Exception("no file in drop directory")
    else:
        path_to_dropped = os.path.join(PDF_DROP_DIR, dropped_list[0])

    os.makedirs(path_to_dir(entry.dblpid), exist_ok=False)

    path_to_pdf = os.path.join(PDF_DIR, dblpsuffix(entry.dblpid)+'.pdf')

    with open(path_to_bib(entry.dblpid), 'w') as file:
        file.write(entry.bib)

    with open(path_to_metadata(entry.dblpid), 'w') as file:
        yaml.dump(entry.metadata, file, default_flow_style=False)

    shutil.move(path_to_dropped, path_to_pdf)

def dblpsuffix(dblpid):
    return dblpid.split('/')[-1]

def path_to_dir(dblpid):
    return os.path.join(METADATA_DIR, dblpid)

def path_to_bib(dblpid):
    suffix = dblpsuffix(dblpid)
    return os.path.join(METADATA_DIR, dblpid, suffix+'.bib')

def path_to_metadata(dblpid):
    suffix = dblpsuffix(dblpid)
    return os.path.join(METADATA_DIR, dblpid, suffix+'.yaml')

def path_to_pdf(dblpid):
    filename = dblpsuffix(dblpid)+'.pdf'

    for step in os.walk(PDF_DIR):
        if filename in step[2]:
            return os.path.join(step[0], filename)

def list_categories():
    return os.walk(PDF_DIR).__next__()[1]

def search(text):

    entries = list()
    for each in [step[0] for step in os.walk(METADATA_DIR) if not step[1]]:
        dblpid = os.path.relpath(each,METADATA_DIR)

        with open(path_to_bib(dblpid)) as file:
            bib = file.read()
        with open(path_to_metadata(dblpid)) as file:
            metadata = yaml.load(file)

        entries.append(Entry(
            dblpid = dblpid,
            bib = bib,
            metadata = metadata
        ))


    if not text:
        return entries
    else:
        return [
            entry
            for entry in entries
            if any([
                text.lower() in str(value).lower()
                for value in entry.metadata.values()
            ])
        ]

def move_to_category(entry, category):
    path_to_category = os.path.join(PDF_DIR, category)
    os.makedirs(path_to_category, exist_ok=True)
    shutil.move(
        path_to_pdf(entry.dblpid),
        path_to_category
    )
