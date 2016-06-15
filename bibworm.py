#! /usr/bin/python3

# standard libs
import re
import os
import shutil
import argparse
import subprocess
import sys

# 3rd party libs
import pyperclip
import yaml

METADATA_DIR = os.path.expanduser('~/.bibworm')
PDF_DIR = os.path.expanduser('~/Documents/researchDocs')
PDF_DROP_DIR = os.path.expanduser('~/.bibworm-drop')

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

parser_add = subparsers.add_parser('add')
parser_add.add_argument('--emulate',
                        action = 'store_true',
                        help="don't do any action, just print what would be done")
parser_add.add_argument('--eprint',
                        action = 'store_true')

parser_search = subparsers.add_parser('search')
parser_search.add_argument('text')
parser_show = subparsers.add_parser('show')

def get_bibtex_tag(tagname, bib):
    bib = bib.replace('\n','')
    start = re.search(tagname+' *= *{(.+?)},', bib).start(1)
    level = 1
    i = start
    while level > 0:
        if bib[i] == '{':
            level += 1
        elif bib[i] == '}':
            level -= 1
        i += 1

    tmp = bib[start:i-1]
    return  re.sub(' +',' ',tmp).replace('{','').replace('}','')

def find(root, name):
    for step in os.walk(root):
        if name in step[2]:
            return os.path.join(step[0], name)

def add():
    print("reading clipboard...")
    pasted = pyperclip.paste()
    match = re.match("^@[a-z]+{DBLP:(?P<id>[a-zA-Z0-9/]+),.+}$",
                    pasted.replace('\n', ''))
    if not match:
        raise Exception("could not parse clipboard content")
    dblpid = match.group('id').split('/')[-1]
    print("DBLP id:", dblpid)

    print(get_bibtex_tag('author', pasted))
    print(get_bibtex_tag('title', pasted))

    metadata_dir = os.path.join(METADATA_DIR, dblpid)
    if os.path.exists(metadata_dir):
        raise Exception("'{}' already exists".format(metadata_dir))

    droplist = os.listdir(PDF_DROP_DIR)
    if len(droplist) == 0:
        raise Exception("no PDF file in '{}'".format(PDF_DROP_DIR))
    elif len(droplist) > 1:
        raise Exception("Several files in '{}'".format(PDF_DROP_DIR))
    dropped_file = os.path.join(PDF_DROP_DIR, droplist[0])

    dst_file = dblpid.split('/')[-1] + '.pdf'
    existing_pdf = find(PDF_DIR, dst_file)
    if existing_pdf:
        raise Exception("'{}' already exists as '{}'".format(dst_file, existing_pdf))
    path_to_pdf = os.path.join(PDF_DIR, dst_file)

    if args.emulate:
        print("would move '{}' to '{}'".format(os.path.basename(dropped_file), path_to_pdf))
    else:
        os.makedirs(metadata_dir, exist_ok=True)

        shutil.move(dropped_file, path_to_pdf)
        print("moved '{}' to '{}'".format(os.path.basename(dropped_file), path_to_pdf))

        path_to_bib = os.path.join(metadata_dir, dblpid+".bib")
        with open(path_to_bib, 'w') as file:
            file.write(pasted)

        path_to_metadata = os.path.join(metadata_dir, dblpid+".yaml")
        with open(path_to_metadata, 'w') as file:
            file.write("- eprint")


def search(text):
    result = dict()
    for entry in os.listdir(METADATA_DIR):
        path_to_bib = os.path.join(METADATA_DIR, entry, entry+'.bib')
        with open(path_to_bib) as bibfile:
            matching_lines = [line.strip() for line in bibfile
                            if text.lower() in line.lower()]
            if len(matching_lines) > 0:
                result[entry] = matching_lines

    if result:
        print(yaml.dump(result, default_flow_style=False))

def show():
    entries = os.listdir(METADATA_DIR)

    result = dict()
    for entry in entries:
        path_to_bib = os.path.join(METADATA_DIR, entry, entry+'.bib')
        with open(path_to_bib) as bibfile:
            bib = bibfile.read()

        result[entry] = {
            'author': get_bibtex_tag('author', bib),
            'title': get_bibtex_tag('title', bib)
        }

    options = [
        '{:2}: {}\n    "{}"'.format(
            i, result[entry]['author'], result[entry]['title'])
        for (i,entry) in enumerate(entries, start=1)
    ]

    print("\n\n".join(options))

    print('-------')
    print("chose PDF to see")
    try:
        choice = int(input("> "))-1
    except KeyboardInterrupt:
        print('exit')
        sys.exit()

    path_to_pdf = find(PDF_DIR, entries[choice]+'.pdf')
    print("evince",path_to_pdf)
    subprocess.Popen(['evince',path_to_pdf])
    sys.exit()


if __name__ == '__main__':
    args = parser.parse_args()
    if args.command == "add":
        add()
    elif args.command == "search":
        search(args.text)
    elif args.command == "show":
        show()
