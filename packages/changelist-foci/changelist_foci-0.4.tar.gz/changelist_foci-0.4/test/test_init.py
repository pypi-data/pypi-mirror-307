"""Testing Changelist Foci Module Initialization Methods.
"""
from changelist_data.xml.workspace import read_xml

from changelist_foci import get_changelist_foci, _filter_list
from changelist_foci.input.input_data import InputData
from . import get_simple_changelist_xml, get_multi_changelist_xml


def test_get_changelist_foci_simple_changelist():
    test_input = InputData(
        changelists=read_xml(get_simple_changelist_xml()),
        changelist_name=None,
    )
    result = get_changelist_foci(test_input)
    assert result.count('\n') == 1


def test_get_changelist_foci_multi_changelist():
    test_input = InputData(
        changelists=read_xml(get_multi_changelist_xml()),
        changelist_name=None,
    )
    result = get_changelist_foci(test_input)
    assert result.count('\n') == 2


def test_get_changelist_foci_multi_changelist_test_cl():
    test_input = InputData(
        changelists=read_xml(get_multi_changelist_xml()),
        changelist_name='Test',
    )
    result = get_changelist_foci(test_input)
    assert result.count('\n') == 1


def test_get_changelist_foci_multi_changelist_test_cl_lowercase_raises_exit():
    test_input = InputData(
        changelists=read_xml(get_multi_changelist_xml()),
        changelist_name='test',
    )
    try:
        get_changelist_foci(test_input)
        raised_exit = False
    except SystemExit:
        raised_exit = True
    assert raised_exit


def test_get_changelist_foci_multi_changelist_all_changes():
    test_input = InputData(
        changelists=read_xml(get_multi_changelist_xml()),
        changelist_name=None,
        all_changes=True,
    )
    result = get_changelist_foci(test_input)
    assert result.count('\n') == 5


def test_get_changelist_foci_multi_changelist_name_not_present():
    test_input = InputData(
        changelists=read_xml(get_multi_changelist_xml()),
        changelist_name='Missing Name',
    )
    try:
        get_changelist_foci(test_input)
        raised_exit = False
    except SystemExit:
        raised_exit = True
    assert raised_exit


def test_filter_list_simple_select_active_():
    input_data = InputData(
        changelists=read_xml(get_simple_changelist_xml()),
        changelist_name=None,
    )
    result = _filter_list(input_data)[0]
    assert result.name == 'Simple'
    assert result.comment == 'Main Program Files'
    assert result.id == '9f60fda2-421e-4a4b-bd0f-4c8f83a47c88'
    assert len(result.changes) == 1
    change = result.changes[0]
    assert change.before_path == change.after_path
    assert change.before_dir == change.after_dir


def test_filter_list_simple_select_simple_():
    input_data = InputData(
        changelists=read_xml(get_simple_changelist_xml()),
        changelist_name='Simple',
    )
    result = _filter_list(input_data)[0]
    assert result.name == 'Simple'
    assert result.comment == 'Main Program Files'
    assert result.id == '9f60fda2-421e-4a4b-bd0f-4c8f83a47c88'
    assert len(result.changes) == 1
    change = result.changes[0]
    assert change.before_path == change.after_path
    assert change.before_dir == change.after_dir


def test_filter_list_simple_select_():
    input_data = InputData(
        changelists=read_xml(get_simple_changelist_xml()),
        changelist_name='Simple',
    )
    result = _filter_list(input_data)[0]
    assert result.name == 'Simple'
    assert result.comment == 'Main Program Files'
    assert result.id == '9f60fda2-421e-4a4b-bd0f-4c8f83a47c88'
    assert len(result.changes) == 1
    change = result.changes[0]
    assert change.before_path == change.after_path
    assert change.before_dir == change.after_dir


def test_filter_list_multi_select_active_():
    input_data = InputData(
        changelists=read_xml(get_multi_changelist_xml()),
    )
    result = _filter_list(input_data)[0]
    assert result.name == 'Main'
    assert result.comment == 'Main Program Files'
    assert result.id == 'af84ea1b-1b24-407d-970f-9f3a2835e933'
    assert len(result.changes) == 2
    change1 = result.changes[0]
    assert change1.before_path == '/history.py'
    assert not change1.before_dir
    assert change1.after_path is None
    assert change1.after_dir is None
    change2 = result.changes[1]
    assert change2.before_path == '/main.py'
    assert not change2.before_dir 
    assert change1.after_path is None
    assert change1.after_dir is None
