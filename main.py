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
from templates.add_transaction_modal import ADD_TRANSACTION_MODAL, ADD_TRANSACTION_SCRIPT
from templates.edit_transaction_modal import EDIT_TRANSACTION_MODAL, EDIT_TRANSACTION_SCRIPT
from templates.print_modals import PRINT_MODALS_HTML, PRINT_MODALS_SCRIPT
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

# Add global variables for date in modal - either most recent transaction date or today
@app.context_processor
def inject_date_context():
    today = datetime.now().strftime('%Y-%m-%d')  # Today's date formatted as YYYY-MM-DD
    
    # Get the most recent transaction date if available
    recent_date = None
    try:
        recent_date = transaction_manager.get_most_recent_transaction_date()
        print(f"DEBUG - Most recent transaction date: {recent_date}")
    except Exception as e:
        # If any error occurs, default to today's date
        app.logger.error(f"Error getting recent transaction date: {e}")
        print(f"DEBUG - Error getting recent date: {e}")
    
    # Use recent_date if available, otherwise use today
    suggested_date = recent_date if recent_date else today
    print(f"DEBUG - Using date for form: {suggested_date}")
    
    return {
        'now': datetime.now(),  # Keep the original now variable
        'today_date': today,    # Today's date formatted as YYYY-MM-DD
        'suggested_date': suggested_date,  # Either recent transaction date or today
        'add_transaction_modal': ADD_TRANSACTION_MODAL,  # Add the transaction modal HTML
        'add_transaction_script': ADD_TRANSACTION_SCRIPT,  # Add the transaction modal script
        'edit_transaction_modal': EDIT_TRANSACTION_MODAL,  # Add the edit transaction modal HTML
        'edit_transaction_script': EDIT_TRANSACTION_SCRIPT,  # Add the edit transaction modal script
        'print_modals_html': PRINT_MODALS_HTML,  # Add the print modals HTML
        'print_modals_script': PRINT_MODALS_SCRIPT  # Add the print modals script
    }

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

@app.route('/delete/<int:transaction_id>', methods=['GET', 'POST'])
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

@app.route('/api/transaction/<int:transaction_id>')
def get_transaction(transaction_id):
    """Get a single transaction by its ID."""
    transaction = transaction_manager.get_transaction_by_id(transaction_id)
    if transaction:
        return jsonify(transaction)
    return jsonify({"error": "Transaction not found"}), 404

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