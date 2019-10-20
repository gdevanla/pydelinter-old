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

unused_imports: Dict[Union[cst.Import, cst.ImportFrom], Set[str]] = defaultdict(set)
undefined_references: Dict[cst.CSTNode, Set[str]] = defaultdict(set)

pylint_str = str # output formatted string of Pylint output

class RemoveUnusedImportTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (cst.metadata.SyntacticPositionProvider,)

    @classmethod
    def build_dotted_name(cls, import_alias: cst.ImportAlias):
        def walk(node):
            if isinstance(node, cst.Name):
                return (node.value,)
            children = walk(node.value)
            return children + (node.attr.value,)
        return walk(import_alias.name)

    def leave_import_alike(
        self,
        original_node: tp.Union[cst.Import, cst.ImportFrom],
        updated_node: tp.Union[cst.Import, cst.ImportFrom],
    ) -> tp.Union[cst.Import, cst.ImportFrom, cst.RemovalSentinel]:
        #import ipdb; ipdb.set_trace()
        pass

    def leave_Import(
        self, original_node: cst.Import, updated_node: cst.Import
    ) -> cst.Import:
        code = self.get_metadata(cst.metadata.SyntacticPositionProvider, original_node)

        new_import_alias = []
        for import_alias in updated_node.names:
            dotted_name = self.build_dotted_name(import_alias)
            if import_alias.asname:
                continue
            new_import_alias.append(import_alias)
        if new_import_alias:
            new_import_alias[-1] = new_import_alias[-1].with_changes(
                    comma=cst.MaybeSentinel.DEFAULT)
            return updated_node.with_changes(names=new_import_alias)
        if code.start.line == 1:
            return cst.RemoveFromParent()
        return updated_node


    def leave_ImportFrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> cst.ImportFrom:
        #import ipdb; ipdb.set_trace()
        #import ipdb; ipdb.set_trace()
        return updated_node


class Delinter:
    pass

@dataclasses.dataclass
class BaseUnusedImportsWarning:
    '''
    Sum type class to represent types
    '''

@dataclasses.dataclass
class UnusedFromImportsWarning(BaseUnusedImportsWarning):
    import_as_name: str
    dotted_as_name: str
    alias: str

@dataclasses.dataclass
class UnusedImportsWarning(BaseUnusedImportsWarning):
    alias: str
    dotted_as_name: str


class UnusedImportsDelinter(Delinter):

    # filter import without alias
    pattern_import = re.compile('Unused import (?P<dname>.*)')
    # filter import with alias
    pattern_import_with_alias = re.compile('Unused (?P<dname>.*) imported as (?P<aname>.*)')

    # filter from with alias
    pattern_from_with_alias = re.compile(
            'Unused (?P<dname>.*) imported from (?P<dname0>.*) as (?P<aname>.*)')

    # filter from
    pattern_from = re.compile('Unused (?P<dname>.*) imported from (?P<aname>.*)')

    patterns = [
            (pattern_import, UnusedImportsWarning),
            (pattern_import_with_alias, UnusedImportsWarning),
            # the order of from filters is implicit here, to keep the regex simple.
            (pattern_from_with_alias, UnusedFromImportsWarning),
            (pattern_from, UnusedFromImportsWarning)]

    @classmethod
    def parse_linter_warnings(cls,
            warnings: tp.Iterable[pylint_str]) -> BaseUnusedImportsWarning:
        '''
        Filter just the linter warnings
        '''
        def parse_warning(warning):
            for pattern, class_ in cls.patterns:
                m = re.match(pattern, warning)
                if m:
                    groups = m.groups()
                    if class_ is UnusedImportsWarning:
                        if len(groups) == 2:
                            return UnusedImportsWarning(
                                    alias=m.group('aname'),
                                    dotted_as_name=m.group('dname')
                                    )
                        return UnusedImportsWarning(
                                alias=None,
                                dotted_as_name=m.group('dname')
                                )

                    if class_ is UnusedFromImportsWarning:
                        if len(groups) == 2:
                            return UnusedFromImportsWarning(
                                    import_as_name=m.group('aname'),
                                    dotted_as_name=m.group('dname'),
                                    alias=None)
                        return UnusedFromImportsWarning(
                                    import_as_name=m.group('dname'),
                                    dotted_as_name=m.group('dname0'),
                                    alias=m.group('aname'))
            raise ValueError(f"Parsing failed for {warning}")


        import_warnings = []
        for warning in warnings:
            import_warnings.append(parse_warning(warning))
        return import_warnings


    @classmethod
    def update(cls, cst, warnings):
        '''
        Apply the refactor on each of the linter warnings
        '''
        pass


def main():
    # accept pylint output
    import libcst as cst
    from delinter.main import RemoveUnusedImportTransformer
    import difflib
    with open('test/input/test_unused_imports.py') as f:
        code = "".join(f.readlines())
        source_tree = cst.parse_module(code)
        wrapper = cst.MetadataWrapper(source_tree)
        fixed_module = wrapper.visit(RemoveUnusedImportTransformer())
        print("".join(difflib.unified_diff(code.splitlines(1), fixed_module.code.splitlines(1))))
    f()


if __name__ == '__main__':
    main()
