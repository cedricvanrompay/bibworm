import re
import os
import shutil

# for taking bibtex from cliboard
# https://github.com/asweigart/pyperclip
import pyperclip

METADATA_DIR = os.path.expanduser('~/.autolib')
PDF_DIR = os.path.expanduser('~/Documents/researchDocs')
PDF_DROP_DIR = os.path.expanduser('~/.autolib-drop')

print("reading clipboard...")
pasted = pyperclip.paste()
match = re.match("^@inproceedings{DBLP:(?P<id>[a-zA-Z0-9/]+),.+}$",
                pasted.replace('\n', ''))
if not match:
    raise Exception("could not parse clipboard content")
dblpid = match.group('id').split('/')[-1]
print("DBLP id:", dblpid)

metadata_dir = os.path.join(METADATA_DIR, dblpid)
if os.path.exists(metadata_dir):
    raise Exception("'{}' already exists".format(metadata_dir))

dropped_file = os.path.join(PDF_DROP_DIR, os.listdir(PDF_DROP_DIR)[0])

dst_file = os.path.join(PDF_DIR, dblpid.split('/')[-1] + '.pdf')
if os.path.exists(dst_file):
    raise Exception("'{}' already exists".format(dst_file))

# Begin Processing

os.makedirs(metadata_dir, exist_ok=True)

shutil.move(dropped_file, dst_file)
print("moved '{}' to '{}'".format(os.path.basename(dropped_file), dst_file))

path_to_bib = os.path.join(metadata_dir, dblpid+".bib")
with open(path_to_bib, 'w') as file:
    file.write(pasted)
