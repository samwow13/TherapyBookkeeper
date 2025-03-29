# -*- coding: utf-8 -*-
"""
Configuration module for the Therapy Bookkeeping Application.
Contains constants and configuration settings.
"""

# Database configuration
DATABASE = 'therapist_bookkeeping.db'

# Define transaction classifications (customize as needed)
CLASSIFICATIONS = [
    'Client Income',
    'Supervision Income',
    'Consulting Income',
    'Rent/Office Space',
    'Utilities',
    'Software/Subscriptions',
    'Professional Development/Training',
    'Licensing/Insurance',
    'Supplies',
    'Marketing',
    'Bank Fees',
    'Taxes',
    'Other Expense',
    'Owner Draw',  # Often treated differently, but included for tracking
]

# Define transaction codes
CODES = [
    '125',
    '200',
    '225',
    '275',
    '325',
]
