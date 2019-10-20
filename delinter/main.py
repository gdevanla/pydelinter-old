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

SUPPORTED_LINTER_MAP = {
        UnusedImportsDelinter.CODE: UnusedImportsDelinter,
        }

pylint_str = str # output formatted string of Pylint output

class Delinter:

    pattern = re.compile(
            r'(?P<file_path>.*.py):(?P<line_no>.*): \[(?P<code>.*)\(.*\), \] (?P<warning>.*)'
            #r'(?P<file_path>.*.py):(?P<line_no>.*): .*'
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
            code = m.group('code')
            warning_text = m.group('warning')

            class_ = SUPPORTED_LINTER_MAP[code]
            parsed_warning = class_.parse_linter_warning(
                    (file_path, line_no, warning_text))
            parsed_warnings.append(parsed_warning)
        import ipdb; ipdb.set_trace()
        return parsed_warnings


def main():
    pass

if __name__ == '__main__':
    main()
