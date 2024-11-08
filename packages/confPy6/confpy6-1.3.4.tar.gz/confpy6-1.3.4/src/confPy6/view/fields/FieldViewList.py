# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLineEdit, QComboBox

from confPy6.view.FieldView import FieldView


class FieldViewList(FieldView):
    value_changed = Signal(tuple)

    def __init__(self, parent_field: 'FieldList'):
        super().__init__(parent_field)

    def ui_field(self, view: QLineEdit = None) -> QLineEdit:
        """

        """
        if view is None:
            le = QLineEdit(str(self.parent_field.value))
        else:
            le: QLineEdit = view
        le.setToolTip(f"({self.parent_field.field_name}) {self.parent_field._description}")

        self.ui_edit_fields.append(le)
        self.ui_edit_fields[-1].textEdited.connect(self._on_text_edited)
        # self.ui_edit_fields[-1] : QtWidgets.QLineEdit
        self.ui_edit_fields[-1].editingFinished.connect(self._on_edited_finished)
        # new
        return self.ui_edit_fields[-1]

    def _on_text_edited(self, value):
        self.parent_field.set(value)

    def _on_value_changed_partial(self, value):
        for edit in self.ui_edit_fields:
            edit.setText(str(value))

    def _input_validation(self, value):
        # First check if an ',' is present
        if isinstance(value, str) and "," in value:
            # Remove brackets if present
            tv = value.replace('[', '').replace(']', '').replace(' ', '')
            # Split by comma
            tv_split = tv.split(",")
            tup = []
            item_type = None
            first_item_type = None
            for it, t in enumerate(tv_split):
                if t.isnumeric() and float(t).is_integer():
                    first_item_type = int if it == 0 else first_item_type
                    item_type = int
                    if item_type == first_item_type:
                        tup.append(int(t))
                    else:
                        raise ValueError(f"Invalid input. First type {first_item_type} does "
                                         f"not match preceding type {item_type}")
                elif t.isnumeric():
                    first_item_type = float if it == 0 else first_item_type
                    item_type = float
                    if item_type == first_item_type:
                        tup.append(float(t))
                    else:
                        raise ValueError(f"Invalid input. First type {first_item_type} does "
                                         f"not match preceding type {item_type}")
                else:
                    first_item_type = str if it == 0 else first_item_type
                    item_type = str
                    if item_type == first_item_type:
                        tup.append(str(t))
                    else:
                        raise ValueError(f"Invalid input. First type {first_item_type} does "
                                         f"not match preceding type {item_type}")
            return list(tup)
        elif isinstance(value, list):
            return value
        else:
            raise ValueError("Invalid input or unknown type (not str or list)")

    def _on_edited_finished(self):
        # print(f"edited finished: {self.parent_field.value} of type {type(self.parent_field.value)}")
        try:
            conv_value = self._input_validation(self.parent_field.value)
            # print(f"converted value: {conv_value} of type {type(conv_value)}")
            self.parent_field.set(conv_value)
            for edit in self.ui_edit_fields:
                edit: QLineEdit
                print(edit.styleSheet())
                edit.setStyleSheet(None)
        except Exception as e:
            self._display_error(e)
            self.parent_field.set(self.parent_field.value)
