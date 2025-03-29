"""
Therapy Bookkeeping Application
A Flask-based bookkeeping application for a solo therapist.
Features: Homepage listing transactions, modal for adding transactions,
          monthly and overall financial summaries.
"""
import os
from flask import Flask, request, redirect, url_for, g, flash, jsonify
from datetime import datetime

# Import modules
from database import DatabaseManager
from transaction_manager import TransactionManager
from code_manager import CodeManager
from classification_manager import ClassificationManager
from templates.modals_template import StringTemplateLoader
from config import DATABASE

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
    }

@app.context_processor
def inject_modal_data():
    """
    Inject modal data into all templates.
    This makes modal templates available in all templates rendered by the app.
    """
    from templates.modals_template import (
        MODALS_TEMPLATE, 
        ADD_TRANSACTION_SCRIPT_TEMPLATE, 
        EDIT_TRANSACTION_SCRIPT_TEMPLATE,
        DELETE_TRANSACTION_SCRIPT_TEMPLATE,
        PRINT_MODALS_SCRIPT_TEMPLATE,
        EDIT_CODES_SCRIPT_TEMPLATE
    )
    
    # Default empty options
    classification_options = ""
    code_options = ""
    
    # Only try to fetch data if database connection is available
    if hasattr(g, 'db'):
        try:
            db = g.db
            cursor = db.cursor()
            
            # Get classifications for dropdown
            cursor.execute("SELECT classification FROM classifications ORDER BY classification")
            classifications = [row['classification'] for row in cursor.fetchall()]
            classification_options = "".join([f'<option value="{c}">{c}</option>' for c in classifications])
            
            # Get codes for dropdown
            cursor.execute("SELECT code FROM codes ORDER BY code")
            codes = [row['code'] for row in cursor.fetchall()]
            code_options = "".join([f'<option value="{c}">{c}</option>' for c in codes])
        except Exception as e:
            # Log the error but don't crash
            print(f"Error fetching dropdown data: {e}")
    
    return {
        'modals_content': MODALS_TEMPLATE,
        'add_transaction_script': ADD_TRANSACTION_SCRIPT_TEMPLATE,
        'edit_transaction_script': EDIT_TRANSACTION_SCRIPT_TEMPLATE,
        'delete_transaction_script': DELETE_TRANSACTION_SCRIPT_TEMPLATE,
        'print_modals_script': PRINT_MODALS_SCRIPT_TEMPLATE,
        'edit_codes_script': EDIT_CODES_SCRIPT_TEMPLATE,
        'classification_options': classification_options,
        'code_options': code_options,
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
    """Handle the edit transaction form submission."""
    # Get form data
    date = request.form["date"]
    description = request.form["description"]
    amount = float(request.form["amount"])
    transaction_type = request.form["type"]
    classification = request.form["classification"]
    code = request.form["code"]
    
    # Update the transaction in the database
    transaction_manager.update_transaction(
        transaction_id, date, description, amount, 
        transaction_type, classification, code
    )
    
    flash(f"Transaction '{description}' was updated successfully!", "success")
    return redirect(url_for("index"))

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
    """API endpoint to get transaction data for editing."""
    transaction = transaction_manager.get_transaction(transaction_id)
    if transaction:
        return jsonify(transaction)
    else:
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