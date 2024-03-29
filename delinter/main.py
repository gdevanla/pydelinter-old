import os
import re
import typing as tp
import difflib
import argparse
import collections
import dataclasses
from typing import Set
from typing import Dict
from typing import Union
from collections import defaultdict

from pylint import epylint as lint

import libcst as cst
from delinter.unused_imports import UnusedImportsDelinter
from delinter.unused_imports import RemoveUnusedImportTransformer

SUPPORTED_LINTER_MAP = {
        UnusedImportsDelinter.CODE: (UnusedImportsDelinter, RemoveUnusedImportTransformer)
        }

pylint_str = str # output formatted string of Pylint output

class Delinter:

    pattern = re.compile(
            r'(?P<file_path>.*.py):(?P<line_no>.*):\[(?P<code>.*)\(.*\),(?P<obj>.*)\](?P<warning>.*)'
            )

    @classmethod
    def parse_linter_warnings(cls, warnings: tp.Iterable[pylint_str], msg_id):

        if msg_id not in SUPPORTED_LINTER_MAP:
            raise ValueError(f'{msg_id} not currently supported for delinting.')

        parsed_warnings = []
        for warning in warnings:
            m = re.match(cls.pattern, warning)
            if not m:
                raise ValueError(f'Unknown format {warning}')
            file_path = m.group('file_path')
            line_no = m.group('line_no')
            line_no = int(m.group('line_no'))
            code = m.group('code')
            warning_text = m.group('warning')

            if code != msg_id:
                continue
            if code not in SUPPORTED_LINTER_MAP:
                continue
            class_ = SUPPORTED_LINTER_MAP[code][0]
            parsed_warning = class_.parse_linter_warning(
                    (file_path, line_no, warning_text))
            parsed_warnings.append(parsed_warning)
        return parsed_warnings


def get_arg_parser():
    '''
    Return the arg parse for the delinter.
    '''
    p = argparse.ArgumentParser(
            description='Command line tool for delinting certain pylint messages',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''Examples:

            Running the below examples will generate an unified-diff file that can be used as a patch to apply the changes to git or Mercurial.
            delinter/main.py --msg W0611 foo/core.py

            To process multiple python files, provide a folder
            delinter/main.py --msg W0611 foo/

            Running, this command on the test file available with this repository:
            delinter/main.py --msg W0611 delinter/test/input


            --- a/delinter/test/input/test_unused_imports.py
            +++ b/delinter/test/input/test_unused_imports.py
            @@ -1,12 +1,7 @@
            -import unitest.mock.patch, unittest.mock.patch as p1
             import unitest.mock.patch, unittest.mock.patch as p2
            -import unittest as t, unittest as t2
            +import unittest as t2
             import unitest.mock.patch as p
            -import os
            -import pandas as pd, numpy as np
            -from collections.abc import defaultdict, OrderedDict
            -from itertools import filterfalse as _filterfalse
            -from collections.abc import x, y
            +from collections.abc import y
             from collections import *

             p2.mock() # use p2

            ''')
    p.add_argument(
            '--msg_id',
            type=str,
            help=("The pylint message that will be delinterd. Eg W0611"))

    p.add_argument('file_path_or_folder',
            type=str,
            help=(
            "Path to a .py file or folder contain *.py files. "
            "This relative path will be used to generate the unified diff files.")
            )
    return p


def main():

    options = get_arg_parser().parse_args()

    root_file_path = 'delinter/test/input/test_unused_imports.py'
    msg_template = r'{path}:{line}:[{msg_id}({symbol}),{obj}]{msg}'
    pylint_command = f"{root_file_path} --enable=W --disable=C,R,E,F --msg-template={msg_template} --score=n"

    out, _ = lint.py_run(pylint_command, return_std=True)
    result = "".join(out.readlines()).split('\n')
    result = [r.strip() for r in result if r.strip() and not r.strip().
            startswith('************* Module ')]
    parsed_warnings = Delinter.parse_linter_warnings(result, options.msg_id)
    if os.path.isdir(root_file_path):
        from pathlib import Path
        files = Path(root_file_path).glob('**/*.py')
    else:
        files = [root_file_path]

    for file_path in files:
        with open(file_path) as f:
            source_code = "".join(f.readlines())
            source_tree = cst.parse_module(source_code)
            wrapper = cst.MetadataWrapper(source_tree)
            local_warnings = [p for p in parsed_warnings if p.file_path == str(file_path)]
            fixed_module = wrapper.visit(
                    SUPPORTED_LINTER_MAP[options.msg_id][1](local_warnings))
            a_file_path = 'a/' + str(file_path)
            b_file_path = 'b/' + str(file_path)
            print("".join(difflib.unified_diff(
                    source_code.splitlines(1),
                    fixed_module.code.splitlines(1),
                    fromfile=a_file_path,
                    tofile=b_file_path
                    )))

if __name__ == '__main__':
    main()
