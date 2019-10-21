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

    @classmethod
    def parse_linter_warnings(cls, warnings: tp.Iterable[pylint_str]):

        parsed_warnings = []
        for warning in warnings:
            file_path, line_no, code, obj, warning_text = warning.split(':')
            if code not in SUPPORTED_LINTER_MAP:
                continue
            class_ = SUPPORTED_LINTER_MAP[code]
            parsed_warning = class_.parse_linter_warning(
                    (file_path, int(line_no), warning_text))
            parsed_warnings.append(parsed_warning)
        return parsed_warnings


def main():

    # parse args
    # load files
    # parse warnings
    #

    #file_path = '/home/devanla/projects/rapc/helix'
    file_path = 'test/input/test_unused_imports.py'
    msg_template = '{path}:{line}:{msg_id}:{obj}:{msg}'
    #msg_template = '{msg}'
    pylint_command = f"{file_path} --enable=W --disable=C,R,E,F --msg-template={msg_template}"

    from pylint import epylint as lint
    out, err = lint.py_run(pylint_command, return_std=True)
    result = "".join(out.readlines()).split('\n')
    result = [r.strip() for r in result if r.strip()][1:-2]
    parsed_warnings = Delinter.parse_linter_warnings(result)
    import ipdb; ipdb.set_trace()

    with open(file_path) as f:
        source_code = "".join(f.readlines())
        source_tree = cst.parse_module(source_code)
        wrapper = cst.MetadataWrapper(source_tree)
        fixed_module = wrapper.visit(
                unused_imports.RemoveUnusedImportTransformer(parsed_warnings))
        print("".join(difflib.unified_diff(source_code.splitlines(1), fixed_module.code.splitlines(1))))

if __name__ == '__main__':
    main()
