# -*- coding: utf-8 -*-
"""
Modals Template for the Therapy Bookkeeping Application.
This file imports all modal templates and constructs the rendered HTML.
"""

from templates.add_transaction_modal import ADD_TRANSACTION_MODAL, ADD_TRANSACTION_SCRIPT
from templates.edit_transaction_modal import EDIT_TRANSACTION_MODAL, EDIT_TRANSACTION_SCRIPT
from templates.delete_transaction_modal import DELETE_TRANSACTION_MODAL, DELETE_TRANSACTION_SCRIPT

# Combine all modal HTML content - use string concatenation instead of f-string
# to avoid issues with Jinja2 templates
MODALS_TEMPLATE = ADD_TRANSACTION_MODAL + "\n" + EDIT_TRANSACTION_MODAL + "\n" + DELETE_TRANSACTION_MODAL

# Collect all modal scripts to be included in the base template
ADD_TRANSACTION_SCRIPT_TEMPLATE = ADD_TRANSACTION_SCRIPT
EDIT_TRANSACTION_SCRIPT_TEMPLATE = EDIT_TRANSACTION_SCRIPT
DELETE_TRANSACTION_SCRIPT_TEMPLATE = DELETE_TRANSACTION_SCRIPT
