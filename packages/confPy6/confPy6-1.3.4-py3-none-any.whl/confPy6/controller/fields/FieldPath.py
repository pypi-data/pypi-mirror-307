# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

import pathlib
import re
from pathlib import Path

from confPy6.controller.Field import Field
from confPy6.view.fields.FieldViewPath import FieldViewPath


class FieldPath(Field):
    # value_changed = Signal(str)

    def __init__(self, value: str, friendly_name: str = None, description: str = None, env_var: str = None):
        super().__init__(value, friendly_name, description, env_var)
        self._input = self.value
        self._allowed_types = (Path, [pathlib.PurePosixPath, pathlib.PurePath,
                                      pathlib.PureWindowsPath,
                                      str])

    def _env_converter(self):
        return str(Path(self.get()).resolve().absolute().as_posix())

    def create_view(self):
        return FieldViewPath(self)

    # ==================================================================================================================
    # Getter and Setter for value retrival
    # ==================================================================================================================
    def get(self) -> pathlib.Path:
        return Path(self.replace_keywords(str(self.value)))

    def serialize(self):
        """Used for serializing instances. Returns the current field as a yaml-line."""
        expanded_val = str(self.get())
        if "{" in self._yaml_repr() and "}" in self._yaml_repr():
            return f"{self.field_name}: {self._yaml_repr()} # ({expanded_val}) {self.friendly_name}: {self.description}"

        return f"{self.field_name}: {self._yaml_repr()} # {self.friendly_name}: {self.description}"

    def _yaml_repr(self):
        return str('"@Path:<' + str(Path(self.value).as_posix()) + '>"')

    def _field_parser(self, val):
        # Overwritten function, to replace the @Path keyword
        match = re.findall(r'@Path:<([^>]*)>', val)
        if len(match) > 0:
            self._module_logger.info(f"Found @Path: {val}. Check syntax, multiple @Path: are not allowed in one field.")
            return {"value": Path(match[0])}
        elif len(match) == 0:
            self._module_logger.debug(f"No @Path: found in {val}. Please check field.")
            return {"value": Path('./')}

    def create_folder(self):
        print(f"Creating folder {self.get()}")
        # Check if path exists
        if not Path(self.get()).exists():
            Path(self.get()).mkdir(parents=True, exist_ok=True)
        # Check if path is now exists
        if Path(self.get()).exists():
            self._module_logger.info(f"Folder {self.get()} created.")
        else:
            self._module_logger.error(f"Folder {self.get()} could not be created.")
        self.csig_field_changed.emit()

    def __str__(self):
        return str(Path(self.value).as_posix())
