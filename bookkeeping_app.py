# -*- coding: utf-8 -*-
"""
Therapy Bookkeeping Application - Legacy Entry Point

This file now serves as a compatibility wrapper for the refactored application.
All functionality has been moved to main.py and related modules.
"""

import os
import sys
from flask import Flask, redirect, url_for

# Create a simple Flask app for redirection
app = Flask(__name__)

@app.route('/')
def redirect_to_main():
    """Redirect to the main application."""
    return "This application has been refactored. Please run main.py instead."

if __name__ == '__main__':
    # Print message about the refactoring
    print("=" * 80)
    print("NOTICE: This application has been refactored.")
    print("Please run main.py instead of bookkeeping_app.py.")
    print("=" * 80)
    
    # Import and run the main application
    try:
        # Add the current directory to the path to ensure imports work
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Import the main application
        from main import app as main_app
        
        # Run the main application
        host = '127.0.0.1'
        port = 5000
        print(f"Running the refactored application from main.py on http://{host}:{port}")
        main_app.run(host=host, port=port, debug=True)
    except ImportError as e:
        print(f"Error importing main application: {e}")
        print("Please ensure that main.py and all required modules are present.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running main application: {e}")
        sys.exit(1)
