import difflib
import unittest

import libcst as cst
import delinter.unused_imports as unused_imports
from delinter.main import Delinter

source_code = '''
import unitest.mock.patch, unittest.mock.patch as p1
import unitest.mock.patch, unittest.mock.patch as p2
import unittest as t
import unitest.mock.patch as p
import os
import pandas as pd, numpy as np
from collections.abc import defaultdict, OrderedDict
from itertools import filterfalse as _filterfalse

p2.mock() # use p1
t.mock() # use t

'''

unused_import_warnings = '''
test_unused_imports.py:1: [W0611(unused-import), ] Unused import unitest.mock.patch
test_unused_imports.py:1: [W0611(unused-import), ] Unused unittest.mock.patch imported as p1
test_unused_imports.py:5: [W0611(unused-import), ] Unused import os
test_unused_imports.py:6: [W0611(unused-import), ] Unused pandas imported as pd
test_unused_imports.py:6: [W0611(unused-import), ] Unused numpy imported as np
test_unused_imports.py:7: [W0611(unused-import), ] Unused defaultdict imported from collections.abc
test_unused_imports.py:7: [W0611(unused-import), ] Unused OrderedDict imported from collections.abc
test_unused_imports.py:8: [W0611(unused-import), ] Unused filterfalse imported from itertools as _filterfalse
'''

class TestUnusedImports(unittest.TestCase):

    def test_pylint_warning(self):
        warnings = unused_import_warnings.split('\n')
        warnings = [w for w in warnings if w]
        parsed_warnings = Delinter.parse_linter_warnings(warnings)

        expected_warnings = [
                unused_imports.UnusedImportsWarning(file_path='test_unused_imports.py', line_no='1', alias=None, dotted_as_name='unitest.mock.patch'),
                unused_imports.UnusedImportsWarning(file_path='test_unused_imports.py', line_no='1', alias='p1', dotted_as_name='unittest.mock.patch'),
                unused_imports.UnusedImportsWarning(file_path='test_unused_imports.py', line_no='5', alias=None, dotted_as_name='os'),
                unused_imports.UnusedImportsWarning(file_path='test_unused_imports.py', line_no='6', alias='pd', dotted_as_name='pandas'),
                unused_imports.UnusedImportsWarning(file_path='test_unused_imports.py', line_no='6', alias='np', dotted_as_name='numpy'),
                unused_imports.UnusedFromImportsWarning(file_path='test_unused_imports.py', line_no='7', import_as_name='collections.abc', dotted_as_name='defaultdict', alias=None),
                unused_imports.UnusedFromImportsWarning(file_path='test_unused_imports.py', line_no='7', import_as_name='collections.abc', dotted_as_name='OrderedDict', alias=None),
                unused_imports.UnusedFromImportsWarning(file_path='test_unused_imports.py', line_no='8', import_as_name='filterfalse', dotted_as_name='itertools', alias='_filterfalse')]
        self.assertEqual(parsed_warnings, expected_warnings)




    # warnings = UnusedImportsDelinter.parse_linter_warnings([s2])
    # with open('test/input/test_unused_imports.py') as f:
    #     code = "".join(f.readlines())
    #     source_tree = cst.parse_module(code)
    #     wrapper = cst.MetadataWrapper(source_tree)
    #     fixed_module = wrapper.visit(RemoveUnusedImportTransformer(warnings))
    #     print("".join(difflib.unified_diff(code.splitlines(1), fixed_module.code.splitlines(1))))


if __name__ == '__main__':
    unittest.main()
