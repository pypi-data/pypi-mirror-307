# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDoubleSpinBox

from confPy6.view.FieldView import FieldView


class FieldViewFloat(FieldView):
    value_changed = Signal(float)

    def __init__(self, parent_field):
        super().__init__(parent_field)

    def ui_field(self, view: QDoubleSpinBox = None) -> QDoubleSpinBox:
        """
        Returns a QLineEdit for the UI.
        The UI is automatically updated when the value is changed.
        """
        if view is None:
            dsp = QtWidgets.QDoubleSpinBox()
        else:
            dsp: QDoubleSpinBox = view
        dsp.setRange(self.parent_field._range[0], self.parent_field._range[1])
        dsp.setValue(self.parent_field.value)
        dsp.setDecimals(3)
        dsp.setToolTip(f"({self.parent_field.field_name}) {self.parent_field._description}")
        self.ui_edit_fields.append(dsp)
        self.ui_edit_fields[-1].valueChanged.connect(self._on_value_edited)

        return self.ui_edit_fields[-1]

    def _on_value_edited(self, value):
        self.parent_field.set(float(value))

    def _on_value_changed_partial(self, value):
        # print(f">>> {self.parent_field.name}: Value changed {value}")
        for edit in self.ui_edit_fields:
            edit.setValue(float(value))

    # ==================================================================================================================
    # Pyside functions
    # ==================================================================================================================
    def setSuffix(self, suffix: str):
        for edit in self.ui_edit_fields:
            edit.setSuffix(suffix)
