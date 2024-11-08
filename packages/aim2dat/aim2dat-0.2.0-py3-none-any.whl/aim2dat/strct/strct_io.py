"""Module to handle internal functions to read and write structures."""

# Standard library imports
import pkgutil
import importlib
from inspect import getmembers, isfunction
from typing import Union
import re

# internal library imports
import aim2dat.io as internal_io


def get_structure_from_file(
    file_path: str, file_format: str, kwargs: dict = {}
) -> Union[dict, list]:
    """Get function to read structure file."""
    found_func = False
    if file_format is not None:
        ff_split = file_format.split("-")
        m_name = ff_split[0]
        f_name = "read_structure"
        if len(ff_split) > 1:
            f_name = f"read_{ff_split[1]}_structure"
        func = getattr(importlib.import_module("aim2dat.io." + m_name), f_name)
        found_func = True
    else:
        m_names = [x.name for x in pkgutil.iter_modules(internal_io.__path__)]
        for m_name in m_names:
            if m_name.startswith("base") or m_name == "utils":
                continue
            module = importlib.import_module("aim2dat.io." + m_name)
            for f_name, func in getmembers(module, isfunction):
                if getattr(func, "_is_read_structure_method", False):
                    if re.search(func._pattern, file_path):
                        found_func = True
                        break
            if found_func:
                break

    if not found_func:
        # TODO check if we can give a better error message...
        raise ValueError("File format is not supported.")
    kwargs.update(func._preset_kwargs)
    output = func(file_path, **kwargs)
    if isinstance(output, dict) and "structures" in output:
        return output["structures"]
    return output
