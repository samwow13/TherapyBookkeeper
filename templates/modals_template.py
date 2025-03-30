# -*- coding: utf-8 -*-
"""
Template Module for the Therapy Bookkeeping Application.
This file provides both template content for modals and template loading functionality.
"""

from jinja2 import BaseLoader, TemplateNotFound

# Import template strings from separate files
from templates.base_template import BASE_TEMPLATE
from templates.index_template import INDEX_TEMPLATE
from templates.print_template import PRINT_TEMPLATE
from templates.add_transaction_modal import ADD_TRANSACTION_MODAL, ADD_TRANSACTION_SCRIPT
from templates.edit_transaction_modal import EDIT_TRANSACTION_MODAL, EDIT_TRANSACTION_SCRIPT
from templates.delete_transaction_modal import DELETE_TRANSACTION_MODAL, DELETE_TRANSACTION_SCRIPT
from templates.print_modals import PRINT_MODALS_HTML, PRINT_MODALS_SCRIPT
from templates.edit_codes_modal import EDIT_CODES_MODAL, EDIT_CODES_SCRIPT
from templates.shutdown_modal import SHUTDOWN_MODAL, SHUTDOWN_SCRIPT

# Combine all modal HTML content - use string concatenation instead of f-string
# to avoid issues with Jinja2 templates
MODALS_TEMPLATE = ADD_TRANSACTION_MODAL + "\n" + EDIT_TRANSACTION_MODAL + "\n" + DELETE_TRANSACTION_MODAL + "\n" + PRINT_MODALS_HTML + "\n" + EDIT_CODES_MODAL + "\n" + SHUTDOWN_MODAL

# Collect all modal scripts to be included in the base template
ADD_TRANSACTION_SCRIPT_TEMPLATE = ADD_TRANSACTION_SCRIPT
EDIT_TRANSACTION_SCRIPT_TEMPLATE = EDIT_TRANSACTION_SCRIPT
DELETE_TRANSACTION_SCRIPT_TEMPLATE = DELETE_TRANSACTION_SCRIPT
PRINT_MODALS_SCRIPT_TEMPLATE = PRINT_MODALS_SCRIPT
EDIT_CODES_SCRIPT_TEMPLATE = EDIT_CODES_SCRIPT
SHUTDOWN_SCRIPT_TEMPLATE = SHUTDOWN_SCRIPT

class StringTemplateLoader(BaseLoader):
    """
    Custom Jinja2 template loader that loads templates from strings.
    """
    
    def __init__(self):
        """Initialize the template loader with template strings."""
        self.templates = {
            'base_template_string': BASE_TEMPLATE,
            'index.html': INDEX_TEMPLATE,
            'print.html': PRINT_TEMPLATE,
            'modals.html': MODALS_TEMPLATE,
            'add_transaction_modal.html': ADD_TRANSACTION_MODAL,
            'edit_codes_modal.html': EDIT_CODES_MODAL,
        }

    def get_source(self, environment, template):
        """
        Get the template source.
        
        Args:
            environment: Jinja2 environment
            template: Template name
            
        Returns:
            tuple: (source, name, uptodate_func)
            
        Raises:
            TemplateNotFound: If template is not found
        """
        # Handle direct reference and inheritance ('index.html' extends 'base_template_string')
        if template in self.templates:
            source = self.templates[template]
            return source, template, lambda: True  # Return template name as filename hint
        raise TemplateNotFound(template)
