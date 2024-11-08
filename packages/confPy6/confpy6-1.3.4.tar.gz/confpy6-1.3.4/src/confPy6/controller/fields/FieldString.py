# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from confPy6.controller.Field import Field
from confPy6.view.fields.FieldViewString import FieldViewString


class FieldString(Field):
    def __init__(self, value, friendly_name: str = None, description: str = None, env_var: str = None):
        super().__init__(value, friendly_name, description, env_var)
        self._value_replaced_keywords = self.replace_keywords(self.value)

        self._allowed_types = (str, [])

    def create_view(self):
        return FieldViewString(self)

    def serialize(self):
        """Used for serializing instances. Returns the current field as a yaml-line."""
        expanded_val = str(self.get())
        if "{" in self._yaml_repr() and "}" in self._yaml_repr():
            return f"{self.field_name}: {self._yaml_repr()} # ({expanded_val}) {self.friendly_name}: {self.description}"

        return f"{self.field_name}: {self._yaml_repr()} # {self.friendly_name}: {self.description}"

    def _yaml_repr(self):
        return f"\"{self.value}\""
