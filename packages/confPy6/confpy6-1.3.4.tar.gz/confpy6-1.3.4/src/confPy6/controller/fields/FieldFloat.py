# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from confPy6.controller.Field import Field
from confPy6.view.fields.FieldViewFloat import FieldViewFloat


class FieldFloat(Field):
    def __init__(self, value: float, friendly_name: str = None, description: str = None, env_var: str = None,
                 range: tuple = (-10e6, 10e6)):
        super().__init__(value, friendly_name, description, env_var)
        self._allowed_types = (float, [int])
        self._range = range

    def create_view(self):
        return FieldViewFloat(self)

    def _yaml_repr(self):
        return float(self.value)

    def __float__(self):
        # return str(self.as_dataframe())
        return float(self.get())