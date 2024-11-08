# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""
import pathlib

from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog

import confPy6
from confPy6.controller.CObject import CObject
from confPy6.view.ConfigEditor import ConfigEditor


class ConfigView(QObject, CObject):
    keywords_changed = Signal(dict)

    def __init__(self, parent: confPy6.ConfigNode):
        super().__init__()
        CObject.__init__(self, name=f"{parent.__class__.__name__}.{self.__class__.__name__}")
        self.parent = parent
        self.keywords = {}
        self.config_editor: ConfigEditor = None
        self._module_logger.debug(f"Initialising {self.__class__.__name__} for class {self.parent.__class__.__name__}")

    # ==================================================================================================================
    # UI handling
    # ==================================================================================================================
    def init_config_editor(self):
        self.config_editor = ConfigEditor(self)

    def widget(self, max_level=1):
        self.parent._module_logger.debug("Creating widget for config view.")
        widget = QWidget()
        widget.setLayout(self._create_config_layout(max_level))
        return widget

    def keyword_widget(self):
        ''' Table widget with key and value'''
        widget = QtWidgets.QTableWidget()
        widget.setColumnCount(2)
        widget.setHorizontalHeaderLabels(["Keyword", "Value"])
        widget.setRowCount(len(self.parent.keywords))
        for i, (key, value) in enumerate(self.parent.keywords.items()):
            widget.setItem(i, 0, QtWidgets.QTableWidgetItem(key))
            widget.setItem(i, 1, QtWidgets.QTableWidgetItem(value))
        return widget

    def ui_tree_widget_item(self, tree_widget, max_level=1):
        top_item = QtWidgets.QTreeWidgetItem()
        top_item.setText(0, f"{self.parent.name}")
        top_item.setIcon(0, QIcon(":/icons-bw/icons/single-color/cli-settings.svg"))
        for attr, val in self.parent.fields.items():
            item, le = val.view.ui_tree_widget_item()
            top_item.addChild(item)
            tree_widget.setItemWidget(item, 1, le)

        for attr, val in self.parent.configs.items():
            val: confPy6.ConfigNode
            if val.level <= max_level:
                top_item.addChild(val.view.ui_tree_widget_item(tree_widget))

        # Create
        if self.parent.level == 0:
            top_item.addChild(self._autosave_widget())

        return top_item

    def _autosave_widget(self):
        """
        Creates a widget for the autosave option.
        :return:
        """
        widget = QtWidgets.QTreeWidgetItem()
        #layout = QtWidgets.QHBoxLayout()
        #widget.setLayout(layout)

        #lbl = QLabel("Autosave")
        #layout.addWidget(lbl)

        cbx = QtWidgets.QCheckBox()
        #cbx.setChecked(self.parent._autosave)
        #cbx.stateChanged.connect(self.parent._on_autosave_changed)
        widget.setText(0, f"Config Settings")
        widget.addChild(
         QtWidgets.QTreeWidgetItem(
                ["File:", str(self.parent.config_file), None, None],
         )
        )
        widget.addChild(
         QtWidgets.QTreeWidgetItem(
                ["Autosave:", str(self.parent.autosave_enable), None, None],
         )
        )
        return widget

    def _create_config_layout(self, max_level):
        """ Creates a pyside 6 layout based on the fields of the class."""
        grd_layout = QtWidgets.QGridLayout()
        row = 0
        # iterate through all class attributes
        for attr, val in self.parent.fields.items():
            grd_layout.addWidget(QLabel(val.friendly_name), row, 0)
            grd_layout.addWidget(val.view.ui_field(), row, 1)
            row += 1

        for attr, val in self.parent.configs.items():
            val: confPy6.ConfigNode
            if val.level <= max_level:
                gbox = QtWidgets.QGroupBox(val.name)
                gbox.setLayout(val.view._create_config_layout(max_level))
                grd_layout.addWidget(gbox, row, 0, 1, 2)
                row += 1

        return grd_layout

    def save_file_dialog(self, default_path: str):
        # Create a file save dialog
        file_name, _ = QFileDialog.getSaveFileName(
            None,
            "Save Config File",
            str(default_path),
            "Config Files (*.yaml)",
        )

        return pathlib.Path(file_name)