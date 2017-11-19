#!/usr/bin/env python3
# GPL License, Version 3.0 or later

import os
import subprocess
import textwrap
import re

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
COMMAND_NAME = 'nitf-rename'


def patch_help_test(help_output):
    help_output = help_output.replace(
        'usage: ' + COMMAND_NAME,
        'usage::\n'
        '\n'
        '       ' + COMMAND_NAME,
    )
    help_output = help_output.replace(
        "{none,auto,git,hg,svn}", "<none,auto,git,hg,svn>",
    )
    return help_output


def main():
    p = subprocess.run(
        [
            'python3',
            os.path.join(BASE_DIR, COMMAND_NAME),
            '--help',
        ],
        stdout=subprocess.PIPE,
    )

    help_output = (
        p.stdout.decode('utf-8').rstrip() +
        '\n\n'
    )

    # strip trailing space
    help_output = re.sub(r'[ \t]+(\n|\Z)', r'\1', help_output)

    help_output = patch_help_test(help_output)

    # Try write reStructuredText directly!
    # help_output = textwrap.indent(help_output, '   ')
    help_output = (
        '\nOutput of ``' + COMMAND_NAME + ' --help``\n\n' +
        help_output
    )

    with open('readme.rst', 'r', encoding='utf-8') as f:
        data = f.read()

    help_begin_text = '.. BEGIN HELP TEXT'
    help_end_text = '.. END HELP TEXT'
    help_begin_index = data.find(help_begin_text)
    help_end_index = data.find(help_end_text, help_begin_index)

    if help_begin_index == -1:
        print('Error: {!r} not found'.format(help_begin_text))
        return
    if help_end_index == -1:
        print('Error: {!r} not found'.format(help_end_text))
        return

    help_begin_index += len(help_begin_text) + 1

    data_update = data[:help_begin_index] + help_output + data[help_end_index:]

    with open('readme.rst', 'w', encoding='utf-8') as f:
        f.write(data_update)


if __name__ == "__main__":
    main()
