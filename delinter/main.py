import os
import re
import typing as tp
import difflib
import collections
import dataclasses
from typing import Set
from typing import Dict
from typing import Union
from collections import defaultdict

import libcst as cst
from pylint import epylint as lint

from delinter import unused_imports
from delinter.unused_imports import UnusedImportsDelinter

SUPPORTED_LINTER_MAP = {
        UnusedImportsDelinter.CODE: UnusedImportsDelinter,
        }

pylint_str = str # output formatted string of Pylint output

class Delinter:

    pattern = re.compile(
            r'(?P<file_path>.*.py):(?P<line_no>.*):\[(?P<code>.*)\(.*\),(?P<obj>.*)\](?P<warning>.*)'
            )

    @classmethod
    def parse_linter_warnings(cls, warnings: tp.Iterable[pylint_str]):
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

            if code not in SUPPORTED_LINTER_MAP:
                continue
            class_ = SUPPORTED_LINTER_MAP[code]
            parsed_warning = class_.parse_linter_warning(
                    (file_path, line_no, warning_text))
            parsed_warnings.append(parsed_warning)
        return parsed_warnings


    # @classmethod
    # def parse_linter_warnings(cls, warnings: tp.Iterable[pylint_str]):

    #     parsed_warnings = []
    #     import ipdb; ipdb.set_trace()
    #     for warning in warnings:
    #         print(warning.split(':'))
    #         file_path, line_no, code, obj, warning_text = warning.split(':')
    #         if code not in SUPPORTED_LINTER_MAP:
    #             continue
    #         class_ = SUPPORTED_LINTER_MAP[code]
    #         parsed_warning = class_.parse_linter_warning(
    #                 (file_path, int(line_no), warning_text))
    #         parsed_warnings.append(parsed_warning)
    #     return parsed_warnings


def main():

    root_file_path = 'delinter/test/input/test_unused_imports.py'
    msg_template = r'{abspath}:{line}:[{msg_id}({symbol}),{obj}]{msg}'
    pylint_command = f"{root_file_path} --enable=W --disable=C,R,E,F --msg-template={msg_template} --score=n"

    out, _ = lint.py_run(pylint_command, return_std=True)
    result = "".join(out.readlines()).split('\n')
    result = [r.strip() for r in result if r.strip() and not r.strip().
            startswith('************* Module ')]
    parsed_warnings = Delinter.parse_linter_warnings(result)
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
                    unused_imports.RemoveUnusedImportTransformer(local_warnings))
            a_file_path = 'a' + str(file_path)
            b_file_path = 'b' + str(file_path)
            print("".join(difflib.unified_diff(
                    source_code.splitlines(1),
                    fixed_module.code.splitlines(1),
                    fromfile=a_file_path,
                    tofile=b_file_path
                    )))

if __name__ == '__main__':
    main()
