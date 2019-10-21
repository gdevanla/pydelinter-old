import os
import re
import typing as tp
import collections
import dataclasses
from typing import Set
from typing import Dict
from typing import Union
from collections import defaultdict

import libcst as cst
from delinter.unused_imports import UnusedImportsDelinter
import difflib
from delinter import unused_imports

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

    #file_path = '/home/devanla/projects/rapc/RALib'
    file_path = 'test/input/test_unused_imports.py'
    msg_template = r'{path}:{line}:[{msg_id}({symbol}),{obj}]{msg}'
    #msg_template = '{msg}'
    pylint_command = f"{file_path} --enable=W --disable=C,R,E,F --msg-template={msg_template} --score=n"
    #pylint_command = f"{file_path} --enable=W --disable=C,R,E,F --output-format=parseable"

    from pylint import epylint as lint
    out, _ = lint.py_run(pylint_command, return_std=True)
    result = "".join(out.readlines()).split('\n')
    result = [r.strip() for r in result if r.strip() and not r.strip().
            startswith('************* Module ')]
    parsed_warnings = Delinter.parse_linter_warnings(result)

    if os.path.isdir(file_path):
        from pathlib import Path
        files = Path(file_path).glob('**/*.py')
    else:
        files = [file_path]

    for file_path in files:
        with open(file_path) as f:
            source_code = "".join(f.readlines())
            source_tree = cst.parse_module(source_code)
            wrapper = cst.MetadataWrapper(source_tree)
            fixed_module = wrapper.visit(
                    unused_imports.RemoveUnusedImportTransformer(parsed_warnings))
            print("".join(difflib.unified_diff(
                    source_code.splitlines(1),
                    fixed_module.code.splitlines(1),
                    fromfile=file_path,
                    tofile=f'updated_{file_path}'
                    )))


if __name__ == '__main__':
    main()
