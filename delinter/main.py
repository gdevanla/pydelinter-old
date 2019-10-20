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
from delinter.unused_imports import RemoveUnusedImportTransformer
import difflib

def main():
    # accept pylint output


    with open('test/input/test_unused_imports.py') as f:
        code = "".join(f.readlines())
        source_tree = cst.parse_module(code)
        wrapper = cst.MetadataWrapper(source_tree)
        fixed_module = wrapper.visit(RemoveUnusedImportTransformer())
        print("".join(difflib.unified_diff(code.splitlines(1), fixed_module.code.splitlines(1))))
    f()


if __name__ == '__main__':
    main()
