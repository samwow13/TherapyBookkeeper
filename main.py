# -*- coding: utf-8 -*-
"""
Therapy Bookkeeping Application
A Flask-based bookkeeping application for a solo therapist.
Features: Homepage listing transactions, modal for adding transactions,
          monthly and overall financial summaries.
"""

import sqlite3
import os
from flask import Flask, render_template_string, request, redirect, url_for, g, flash, jsonify
from datetime import datetime
from collections import defaultdict
from jinja2 import BaseLoader, Environment, TemplateNotFound

# Import modules
from database import DatabaseManager
from transaction_manager import TransactionManager
from code_manager import CodeManager
from classification_manager import ClassificationManager
from template_loader import StringTemplateLoader, BASE_TEMPLATE, INDEX_TEMPLATE, PRINT_TEMPLATE
from config import DATABASE, CLASSIFICATIONS, CODES

# --- Flask App Setup ---
app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)  # Needed for flashing messages

# Initialize managers
db_manager = DatabaseManager(app, DATABASE)
transaction_manager = TransactionManager(app, db_manager)
code_manager = CodeManager(db_manager)
classification_manager = ClassificationManager(db_manager)

# Replace default loader and ensure environment uses it
app.jinja_loader = StringTemplateLoader()

# Add a global variable for 'now' to pre-fill date in modal
@app.context_processor
def inject_now():
    return {'now': datetime.now()}  # Use local time for default date

# --- Routes ---
@app.route('/')
@app.route('/month/<month>')
def index(month=None):
    """Homepage: Displays transactions and financial summary."""
    return transaction_manager.index_view(month)

@app.route('/print/month/<month>')
def print_transactions(month):
    """Renders a print-friendly view of transactions for a given month."""
    return transaction_manager.print_month_view(month)

@app.route('/print/all')
def print_all_transactions():
    """Renders a print-friendly view of all transactions with pagination."""
    return transaction_manager.print_all_view()

@app.route('/print/year/<year>')
def print_year_transactions(year):
    """Renders a print-friendly view of transactions for a specific year."""
    return transaction_manager.print_year_view(year)

@app.route('/add', methods=['POST'])
def add_transaction():
    """Handles adding a new transaction."""
    return transaction_manager.add_transaction()

@app.route('/edit/<int:transaction_id>', methods=['POST'])
def edit_transaction(transaction_id):
    """Handles editing an existing transaction."""
    return transaction_manager.edit_transaction(transaction_id)

@app.route('/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    """Handles deleting a transaction."""
    return transaction_manager.delete_transaction(transaction_id)

@app.route('/add_code', methods=['POST'])
def add_code():
    """Handles adding a new transaction code."""
    return code_manager.add_code()

@app.route('/add_classification', methods=['POST'])
def add_classification():
    """Handles adding a new transaction classification."""
    return classification_manager.add_classification()

@app.route('/delete_code/<code>', methods=['POST'])
def delete_code(code):
    """Handles deleting a transaction code."""
    return code_manager.delete_code(code)

@app.route('/delete_classification/<classification>', methods=['POST'])
def delete_classification(classification):
    """Handles deleting a transaction classification."""
    return classification_manager.delete_classification(classification)

# AJAX Endpoints
@app.route('/api/check_code_usage/<code>')
def check_code_usage(code):
    """Check if a code is in use by any transactions."""
    return code_manager.check_usage(code)

@app.route('/api/check_classification_usage/<classification>')
def check_classification_usage(classification):
    """Check if a classification is in use by any transactions."""
    return classification_manager.check_usage(classification)

@app.route('/api/codes/page/<int:page>')
def get_codes_page(page):
    """Get a page of transaction codes."""
    return code_manager.get_page(page)

@app.route('/api/classifications/page/<int:page>')
def get_classifications_page(page):
    """Get a page of transaction classifications."""
    return classification_manager.get_page(page)

@app.route('/init_db')
def init_db_route():
    """Route to initialize the database manually via browser."""
    return db_manager.init_db_route()

@app.route('/update_db')
def update_db_route():
    """Route to update the database schema manually via browser."""
    return db_manager.update_db_route()

# --- Main Execution ---
if __name__ == '__main__':
    print("Starting Flask app...")
    with app.app_context():
        db_manager.init_db_schema()  # Ensure tables exist
        db_manager.update_db_schema()  # Add columns if needed, ensure defaults

    host = '127.0.0.1'
    port = 5000
    print(f"Flask app ready. Running on http://{host}:{port}")
    print("Access the app in your browser.")
    # Set debug=False for a cleaner console, True for development error pages
    app.run(host=host, port=port, debug=True)