import re
import subprocess
import os
from itertools import chain

from .db import path_to_pdf
from . import db

def parse_range_list(rngs):
    def parse_range(rng):
        parts = rng.split('-')
        if 1 > len(parts) > 2:
            raise ValueError("Bad range: '%s'" % (rng,))
        parts = [int(i) for i in parts]
        start = parts[0]
        end = start if len(parts) == 1 else parts[1]
        if start > end:
            end, start = start, end
        return range(start, end + 1)

    return sorted(set(chain(*[parse_range(rng) for rng in rngs.split(',')])))

def picker_simple(options):
    print('\n'.join('{}: {}'.format(i,option)
          for (i,option) in enumerate(options))
    )
    user_input = input('choice: ')
    if user_input.isdecimal():
        return options[int(user_input)]
    else:
        return user_input

def picker_complex(entries, default_action):

    options = [
        "# {}\n{}".format(i+1, entry)
        for (i,entry) in enumerate(entries)
    ]

    print('\n\n'.join(["# {}\n{}".format(i+1, entry)
                       for (i,entry) in enumerate(entries)
                      ]
    ))
    print('-----')
    while True:
        print('Choose items and an action')
        user_input = input('> ')
        match = re.match(r'([0-9,-]*) ?([a-z]*)', user_input)
        if not match:
            print('**Error: invalid input**')
            continue
        else:
            break

    if match.group(1) == '':
        choosed_docs = entries

    else:
        choosed_docs = [entries[each-1]
                        for each in parse_range_list(match.group(1))
                       ]

    action = match.group(2) or default_action

    return choosed_docs, action
