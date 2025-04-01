"""
Therapy Bookkeeping Application
A Flask-based bookkeeping application for a solo therapist.
Features: Homepage listing transactions, modal for adding transactions,
          monthly and overall financial summaries.
"""
import os
import sys
from flask import Flask, request, redirect, url_for, g, flash, jsonify, session
from datetime import datetime
import webbrowser
import threading
import logging

# Helper function to find resources (needed for PyInstaller)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Import modules
from database import DatabaseManager
from transaction_manager import TransactionManager
from code_manager import CodeManager
from classification_manager import ClassificationManager
from templates.modals_template import StringTemplateLoader
from config import DATABASE

# --- Flask App Setup ---
# Use resource_path to set template and static folders correctly for PyInstaller
template_folder = resource_path('templates')
static_folder = resource_path('static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.secret_key = os.urandom(24)  # Needed for flashing messages

# Set logging level to DEBUG
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

# Load config: Need to handle path for PyInstaller too
config_path = resource_path('config.py')
try:
    app.config.from_pyfile(config_path)
except FileNotFoundError:
    # Fallback or error handling if config.py isn't found even with resource_path
    # This might indicate an issue with --add-data in PyInstaller
    print(f"ERROR: Configuration file not found at {config_path}")
    # Depending on criticality, you might exit or use default settings
    # For now, we'll proceed, but Flask might complain if config is essential
    pass 

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
        #print(f"DEBUG - Most recent transaction date: {recent_date}")
    except Exception as e:
        # If any error occurs, default to today's date
        app.logger.error(f"Error getting recent transaction date: {e}")
       # print(f"DEBUG - Error getting recent date: {e}")
    
    # Use recent_date if available, otherwise use today
    suggested_date = recent_date if recent_date else today
    #print(f"DEBUG - Using date for form: {suggested_date}")
    
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
        EDIT_CODES_SCRIPT_TEMPLATE,
        SHUTDOWN_SCRIPT_TEMPLATE
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
            classification_options = ""
            for c in classifications:
                selected_attr = ' selected' if c == "Client Income" else ''
                classification_options += f'<option value="{c}"{selected_attr}>{c}</option>'
            
            # Get codes for dropdown
            cursor.execute("SELECT code FROM codes ORDER BY code")
            codes = [row['code'] for row in cursor.fetchall()]
            code_options = "<option value=\"\">No Code</option>" + "".join([f'<option value="{c}">{c}</option>' for c in codes])
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
        'shutdown_script_template': SHUTDOWN_SCRIPT_TEMPLATE,
        'classification_options': classification_options,
        'code_options': code_options,
    }

# --- Routes ---
@app.route('/')
@app.route('/month/<month>')
def index(month=None):
    """Homepage: Displays transactions and financial summary."""
    # Ensure ui_state exists in session
    if 'ui_state' not in session:
        session['ui_state'] = {}
    
    return transaction_manager.index_view(month, ui_state=session.get('ui_state', {}))

@app.route('/get_summary/<int:year>')
def get_summary(year):
    """API endpoint to get overall summary totals for a specific year."""
    summary_data = transaction_manager.get_overall_totals_by_year(year)
    app.logger.debug(f"Summary data for year {year} before jsonify: {summary_data}")
    if 'error' in summary_data:
        # Return a JSON error response with an appropriate status code
        app.logger.error(f"Error returned for year {year}: {summary_data['error']}")
        return jsonify(summary_data), 400 # Or 500 depending on error type
    return jsonify(summary_data)

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

@app.route('/api/delete_code/<path:code>', methods=['DELETE'])
def api_delete_code(code):
    """API endpoint for deleting a transaction code."""
    db = db_manager.get_db()
    cursor = db.cursor()
    
    # Check if code is in use
    cursor.execute("SELECT COUNT(*) FROM transactions WHERE code = ?", (code,))
    if cursor.fetchone()[0] > 0:
        return jsonify({
            'success': False,
            'message': f'Cannot delete code "{code}" because it is in use by transactions.'
        })
    
    try:
        cursor.execute("DELETE FROM codes WHERE code = ?", (code,))
        db.commit()
        if cursor.rowcount > 0:
            return jsonify({
                'success': True,
                'message': f'Code "{code}" deleted successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Code "{code}" not found.'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error deleting code: {str(e)}'
        })

@app.route('/delete_classification/<classification>', methods=['POST'])
def delete_classification(classification):
    """Handles deleting a transaction classification."""
    return classification_manager.delete_classification(classification)

@app.route('/api/delete_classification/<path:classification>', methods=['DELETE'])
def api_delete_classification(classification):
    """API endpoint for deleting a transaction classification."""
    db = db_manager.get_db()
    cursor = db.cursor()
    
    # Check if classification is in use
    cursor.execute("SELECT COUNT(*) FROM transactions WHERE classification = ?", (classification,))
    if cursor.fetchone()[0] > 0:
        return jsonify({
            'success': False,
            'message': f'Cannot delete classification "{classification}" because it is in use by transactions.'
        })
    
    try:
        cursor.execute("DELETE FROM classifications WHERE classification = ?", (classification,))
        db.commit()
        if cursor.rowcount > 0:
            return jsonify({
                'success': True,
                'message': f'Classification "{classification}" deleted successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Classification "{classification}" not found.'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error deleting classification: {str(e)}'
        })

@app.route('/save_ui_state', methods=['POST'])
def save_ui_state():
    """Save the expanded/collapsed state of UI elements to the session."""
    data = request.get_json()
    if not data or 'id' not in data or 'state' not in data:
        return jsonify(success=False, error="Invalid data"), 400

    element_id = data['id']
    state = data['state']

    # Basic validation (optional: add more specific checks if needed)
    allowed_prefixes = ('allTransactionsCollapse', 'monthCollapse-', 'codeSummaryCollapse', 'monthlySummaryCollapse', 'selected_month', 'codeSummaryActiveTab')
    if not element_id or not any(element_id.startswith(p) for p in allowed_prefixes):
         return jsonify(success=False, error="Invalid element ID"), 400
    
    # Different validation for different types of elements
    if element_id == 'selected_month':
        # For selected_month, the state is a month key (format: YYYY-MM)
        if not state or not isinstance(state, str):
            return jsonify(success=False, error="Invalid month key"), 400
    elif element_id == 'codeSummaryActiveTab':
        # For codeSummaryActiveTab, the state is a tab ID
        if state not in ('code-totals', 'classification-totals'):
            return jsonify(success=False, error="Invalid tab ID"), 400
    else:
        # For collapse elements, state must be 'show' or 'hide'
        if state not in ('show', 'hide'):
            return jsonify(success=False, error="Invalid state"), 400

    if 'ui_state' not in session:
        session['ui_state'] = {}

    session['ui_state'][element_id] = state
    session.modified = True  # Mark session as modified
    
    app.logger.debug(f"Saved UI State: {element_id} = {state}")
    app.logger.debug(f"Full UI State: {session['ui_state']}")

    # print(f"Saved UI State: {session['ui_state']}") # Debugging
    return jsonify(success=True)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    # Basic security: Only allow shutdown requests from localhost
    print(f"DEBUG: Shutdown request received from {request.remote_addr}") # DEBUG
    if request.remote_addr != '127.0.0.1':
        # Maybe log this attempt or return a forbidden error
        print(f"WARN: Shutdown attempt from non-local address: {request.remote_addr}") # DEBUG
        return jsonify(success=False, message="Forbidden"), 403

    print("DEBUG: Shutdown request is from localhost. Attempting to stop server...") # DEBUG
    try:
        # Try Werkzeug's shutdown function first
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func:
            print("DEBUG: Found Werkzeug shutdown function. Calling it...") # DEBUG
            shutdown_func()
            print("DEBUG: Werkzeug shutdown initiated.") # DEBUG
            # Return success, even though the server might stop before sending
            return jsonify(success=True, message="Server shutting down via Werkzeug.")
        else:
            # Fallback for non-Werkzeug environments (like packaged app)
            print("WARN: Werkzeug shutdown function not found. Falling back to os._exit(0).") # DEBUG
            # We need to send a response *before* exiting, but this is tricky.
            # The best we can do is schedule the exit after a tiny delay, 
            # hoping the response gets sent.
            # A cleaner solution might involve a separate thread or process management.
            def delayed_exit():
                import time
                time.sleep(0.1) # Short delay to allow response sending
                os._exit(0) # Force exit
            
            import threading
            threading.Thread(target=delayed_exit).start()
            
            return jsonify(success=True, message="Shutdown initiated via os._exit.")

    except Exception as e:
        print(f"ERROR: Exception during shutdown attempt: {e}") # DEBUG
        # If even the attempt fails, return an error
        return jsonify(success=False, message=f"Error during shutdown: {str(e)}"), 500

# AJAX Endpoints
@app.route('/api/check_code_usage/<path:code>')
def check_code_usage(code):
    """Check if a code is in use by any transactions."""
    return code_manager.check_usage(code)

@app.route('/api/check_classification_usage/<path:classification>')
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
    url = f"http://{host}:{port}"

    # Function to open the browser
    def open_browser():
        print(f"Attempting to open browser at {url}")
        webbrowser.open_new(url)

    print(f"Flask app ready. Running on {url}")
    print("Will attempt to open the app in your default browser shortly...")
    
    # Run the browser opening in a separate thread after a delay
    # This gives the server time to start up before trying to open the browser
    threading.Timer(1.5, open_browser).start() 

    # Set debug=False for production/distribution
    app.run(host=host, port=port, debug=False)