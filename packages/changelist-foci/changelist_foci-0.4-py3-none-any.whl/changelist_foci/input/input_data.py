"""Valid Input Data Class.
"""
from dataclasses import dataclass

from changelist_data.changelist import Changelist

from changelist_foci.format_options import FormatOptions


@dataclass(frozen=True)
class InputData:
    """A Data Class Containing Program Input.

    Fields:
    - changelists (list[Changelist]): The list of changelist data to process.
    - changelist_name (str): The name of the Changelist, or None.
    - format_options (FormatOptions): The options for output formatting.
    - all_changes (bool): Flag for printing all changes in any Changelist.
    """
    changelists: list[Changelist]
    changelist_name: str | None = None
    format_options: FormatOptions = FormatOptions()
    all_changes: bool = False
