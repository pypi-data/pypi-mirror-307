""" Testing Input Init Module Methods.
"""
from pathlib import Path
from unittest.mock import Mock
import pytest

from test import get_simple_changelist_xml
from changelist_foci.format_options import FormatOptions
from changelist_foci.input import validate_input


def test_validate_input_empty_args_returns_data():
    test_input = []
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'workspace.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: get_simple_changelist_xml())
        #
        result = validate_input(test_input)
    assert not result.all_changes
    assert result.changelist_name is None
    assert len(result.changelists) == 1
    assert result.format_options == FormatOptions(
        False, False, False
    )


def test_validate_input_all_changes_returns_data():
    test_input = ['-a']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'workspace.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: get_simple_changelist_xml())
        #
        result = validate_input(test_input)
    assert result.all_changes
    assert result.changelist_name is None
    assert len(result.changelists) == 1
    assert result.format_options == FormatOptions(
        False, False, False
    )


def test_validate_input_full_path_returns_data():
    test_input = ['--full-path']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'workspace.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: get_simple_changelist_xml())
        #
        result = validate_input(test_input)
    assert not result.all_changes
    assert result.changelist_name is None
    assert len(result.changelists) == 1
    assert result.format_options == FormatOptions(
        True, False, False
    )


def test_validate_input_filename_only_returns_data():
    test_input = ['-fx']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'workspace.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: get_simple_changelist_xml())
        #
        result = validate_input(test_input)
    assert not result.all_changes
    assert result.changelist_name is None
    assert len(result.changelists) == 1
    assert result.format_options == FormatOptions(
        False, True, True
    )


def test_validate_input_file_does_not_exist_raises_exit():
    test_input = []
    with (pytest.MonkeyPatch().context() as ctx):
        ctx.setattr(Path, 'exists', lambda _: False)
        result = validate_input(test_input)
    assert result.changelist_name is None
    assert len(result.changelists) == 0


def test_validate_input_file_is_empty_raises_exit():
    test_input = []
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'workspace.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: '')
        try:
            validate_input(test_input)
            raised_exit = False
        except SystemExit:
            raised_exit = True
    assert raised_exit
