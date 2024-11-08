import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from .controller.Field import Field
from .controller.Field import T
from .controller.ConfigNode import ConfigNode
from .view.ConfigView import ConfigView
from .view.FieldView import FieldView


# custom types

from .controller.SelectableList import SelectableList
from .controller.fields.FieldSelectableList import FieldSelectableList
from .view.fields.FieldViewSelectableList import FieldViewSelectableList

# define a tree view header
def tree_view_header():
    return ["Name", "Value", "Description", "Type", "Value (expanded)"]


global_module_log_level = logging.WARNING
global_module_log_enabled = True