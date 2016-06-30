import argparse
from . import ui
from . import db
from . import Entry, open_pdf
from .core import Entry

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

parser_add = subparsers.add_parser('add')
parser_add.add_argument('dblpid')

parser_search = subparsers.add_parser('search')
parser_search.add_argument('text', nargs="?")

args = parser.parse_args()

if args.command == 'add':
    entry = Entry(args.dblpid)
    print("adding entry:")
    print(entry)
    db.add(entry)

elif args.command == 'search':
    matching_entries = db.search(args.text)
    choosed_entries, action = ui.picker_complex(matching_entries, default_action='pdf')
    if action == 'pdf':
        for entry in choosed_entries:
            path_to_pdf = db.path_to_pdf(entry.dblpid)
            print('openning', path_to_pdf)
            open_pdf(path_to_pdf)
    elif action == 'move':
        categories = db.list_categories()
        category = ui.picker_simple(categories)
        print('moving to',category)
        for entry in choosed_entries:
            print(entry.dblpid)
            db.move_to_category(entry,category)
