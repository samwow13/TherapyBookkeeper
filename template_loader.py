# -*- coding: utf-8 -*-
"""
Template Loader Module
Provides custom template loading functionality for the Therapy Bookkeeping Application.
"""

from jinja2 import BaseLoader, TemplateNotFound

# Import template strings from separate files
from templates.base_template import BASE_TEMPLATE
from templates.index_template import INDEX_TEMPLATE
from templates.print_template import PRINT_TEMPLATE
from templates.modals_template import MODALS_TEMPLATE
from templates.add_transaction_modal import ADD_TRANSACTION_MODAL

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
