""" Testing FOCI Writer Module Methods.
"""
from changelist_foci.foci_writer import get_file_subject, generate_foci
from changelist_foci.format_options import FormatOptions

from test.provider import get_cl0, get_cl1, get_before_cd, get_after_cd, new_cd, REL_FILE_PATH_1, get_both_cd, get_move_cd, \
    REL_FILE_PATH_2, ODD_FILE_EXT, ODD_FILE_EXT2


def test_generate_foci_0_returns_error():
    result = generate_foci(get_cl0())
    assert result == ":\n"


def test_generate_foci_1_returns_str():
    result = generate_foci(get_cl1())
    assert result == "ChangeList:\n* Create module/file.txt"


def test_generate_foci_1_full_path_returns_str():
    result = generate_foci(get_cl1(), FormatOptions(full_path=True))
    assert result == "ChangeList:\n* Create /module/file.txt"


def test_generate_foci_1_no_file_ext_returns_str():
    result = generate_foci(get_cl1(), FormatOptions(no_file_ext=True))
    assert result == "ChangeList:\n* Create module/file"


def test_generate_foci_1_filename_returns_str():
    result = generate_foci(get_cl1(), FormatOptions(file_name=True))
    assert result == "ChangeList:\n* Create file.txt"


def test_generate_foci_1_filename_plus_no_file_ext_returns_str():
    result = generate_foci(get_cl1(), FormatOptions(file_name=True, no_file_ext=True))
    assert result == "ChangeList:\n* Create file"


def test_get_file_subject_before_returns_str():
    result = get_file_subject(get_before_cd())
    assert result == f'Remove {REL_FILE_PATH_1}'


def test_get_file_subject_after_returns_str():
    result = get_file_subject(get_after_cd())
    assert result == f'Create {REL_FILE_PATH_1}'


def test_get_file_subject_both_returns_str():
    result = get_file_subject(get_both_cd())
    assert result == f'Update {REL_FILE_PATH_1}'


def test_get_file_subject_move_returns_str():
    result = get_file_subject(get_move_cd())
    assert result == f'Move {REL_FILE_PATH_2} to {REL_FILE_PATH_1}'


def test_get_file_subject_format_no_file_ext_returns_str():
    result = get_file_subject(get_before_cd(), FormatOptions(no_file_ext=True))
    assert result == "Remove main_package/__main__"


def test_get_file_subject_remove_format_no_file_ext_returns_str():
    result = get_file_subject(get_before_cd(), FormatOptions(no_file_ext=True))
    assert result == "Remove main_package/__main__"


def test_get_file_subject_create_format_no_file_ext_returns_str():
    result = get_file_subject(get_after_cd(), FormatOptions(no_file_ext=True))
    assert result == "Create main_package/__main__"


def test_get_file_subject_update_format_no_file_ext_returns_str():
    result = get_file_subject(get_both_cd(), FormatOptions(no_file_ext=True))
    assert result == "Update main_package/__main__"


def test_get_file_subject_move_format_no_file_ext_returns_str():
    result = get_file_subject(get_move_cd(), FormatOptions(no_file_ext=True))
    assert result == "Move main_package/__init__ to main_package/__main__"


def test_get_file_subject_create_format_full_path_no_file_ext_returns_str():
    result = get_file_subject(get_after_cd(), FormatOptions(full_path=True, no_file_ext=True))
    assert result == "Create /main_package/__main__"


def test_get_file_subject_create_odd_file_ext_full_path_no_file_ext_returns_str():
    test_input = new_cd(after_path=ODD_FILE_EXT,)
    result = get_file_subject(test_input, FormatOptions(full_path=True, no_file_ext=True))
    assert result == "Create /resources/img/file.png"


def test_get_file_subject_create_odd_file_ext2_full_path_no_file_ext_returns_str():
    test_input = new_cd(after_path=ODD_FILE_EXT2,)
    result = get_file_subject(test_input, FormatOptions(full_path=True, no_file_ext=True))
    assert result == "Create /resources/img/file-123-8.png.jpg"


def test_get_file_subject_create_odd_file_ext_full_path_filename_no_file_ext_returns_str():
    test_input = new_cd(after_path=ODD_FILE_EXT,)
    # The Following Format Options are not compatible
    f_options = FormatOptions(full_path=True, no_file_ext=True, file_name=True)
    result = get_file_subject(test_input, f_options)
    # The filename is overridden by the full_path flag
    assert result == "Create /resources/img/file.png"


def test_get_file_subject_create_odd_file_ext_filename_no_file_ext_returns_str():
    test_input = new_cd(after_path=ODD_FILE_EXT,)
    # These Format Options are a likely combination
    f_options = FormatOptions(no_file_ext=True, file_name=True)
    result = get_file_subject(test_input, f_options)
    assert result == "Create file.png"


