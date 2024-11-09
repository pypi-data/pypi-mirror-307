""" Package Methods.
"""
from changelist_data.changelist import Changelist

from changelist_foci.foci_writer import generate_foci
from changelist_foci.input.input_data import InputData


def get_changelist_foci(
    input_data: InputData,
) -> str:
    """
    Processes InputData, returning the FOCI.

    Parameters:
    - input_data (InputData): The program input data.

    Returns:
    str - The FOCI formatted output.
    """
    return '\n\n'.join(
        generate_foci(cl, input_data.format_options)
        for cl in _filter_list(input_data)
    )


def _filter_list(
    input_data: InputData,
) -> list[Changelist]:
    """
    Filter the Changelists based on InputData, to determine which changes to output.
    """
    if input_data.all_changes:
        return list(
            filter(lambda x: len(x.changes) > 0, input_data.changelists)
        )
    if input_data.changelist_name not in ["None", None]:
        return _get_changelist_by_name(
            input_data.changelists,
            input_data.changelist_name,
        )
    return _get_active_changelist(input_data.changelists)


def _get_active_changelist(
    cl_list: list[Changelist],
) -> list[Changelist]:
    """
    Find the Active Changelist, or the only changelist.
    """
    if len(cl_list) == 1:
        return [cl_list[0]]
    return list(filter(lambda x: x.is_default, cl_list))


def _get_changelist_by_name(
    cl_list: list[Changelist],
    changelist_name: str,
) -> list[Changelist]:
    """
    Find a Changelist that starts with the given name.
    """
    cl = list(filter(lambda x: x.name.startswith(changelist_name), cl_list))
    if len(cl) == 0:
        exit(f"Specified Changelist {changelist_name} not present.")
    return cl
