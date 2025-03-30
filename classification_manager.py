# -*- coding: utf-8 -*-
"""
Classification Manager Module
Handles transaction classification operations for the Therapy Bookkeeping Application.
"""

from flask import request, redirect, url_for, flash, jsonify
from urllib.parse import parse_qs

class ClassificationManager:
    """
    Manages transaction classifications for the application.
    """
    
    def __init__(self, db_manager):
        """
        Initialize the classification manager.
        
        Args:
            db_manager: DatabaseManager instance
        """
        self.db_manager = db_manager
    
    def get_all_classifications(self):
        """
        Gets all classifications without pagination.
        
        Returns:
            list: All transaction classifications
        """
        db = self.db_manager.get_db()
        cursor = db.cursor()
        cursor.execute("SELECT classification FROM classifications ORDER BY classification")
        return [row[0] for row in cursor.fetchall()]
    
    def get_paginated_classifications(self, page=1, per_page=10):
        """
        Get transaction classifications from the database with pagination.
        
        Args:
            page: Page number (1-indexed)
            per_page: Number of items per page
            
        Returns:
            dict: Pagination information and classifications
        """
        db = self.db_manager.get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM classifications")
        total_count = cursor.fetchone()[0]
        
        # Calculate pagination values
        total_pages = (total_count + per_page - 1) // per_page  # Ceiling division
        page = max(1, min(page, total_pages))  # Ensure page is within bounds
        offset = (page - 1) * per_page
        
        # Get classifications for current page
        cursor.execute("SELECT classification FROM classifications ORDER BY classification LIMIT ? OFFSET ?", 
                      (per_page, offset))
        classifications = [row[0] for row in cursor.fetchall()]
        
        return {
            'classifications': classifications,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': total_pages
            }
        }
    
    def add_classification(self):
        """
        Handles adding a new transaction classification via AJAX.

        Returns:
            JSON response indicating success or failure.
        """
        # --- DEBUGGING: Read raw data instead of request.form ---
        raw_data = request.get_data(as_text=True)
        #print(f"DEBUG: Raw request body: {raw_data!r}")
        parsed_data = parse_qs(raw_data)
        #print(f"DEBUG: Parsed request body: {parsed_data}")
        classification_values = parsed_data.get('classification', [])
        classification = classification_values[0].strip() if classification_values else ''
        #print(f"DEBUG: Manually parsed classification: {classification!r}")
        # --- END DEBUGGING ---

        if not classification:
            # Return JSON error instead of flashing and redirecting
            return jsonify(success=False, message='Classification cannot be empty.')

        db = self.db_manager.get_db()
        cursor = db.cursor()

        # --- DEBUGGING START ---
        #print(f"DEBUG: Received classification from form: {classification!r}")
        # --- DEBUGGING END ---

        try:
            # Check if classification already exists (optional but good practice)
            cursor.execute("SELECT 1 FROM classifications WHERE classification = ?", (classification,))
            # --- DEBUGGING START ---
            exists_result = cursor.fetchone()
            #print(f"DEBUG: Result of SELECT check (exists?): {exists_result}")
            # --- DEBUGGING END ---
            if exists_result:
                return jsonify(success=False, message=f'Classification \"{classification}\" already exists.')

            cursor.execute("INSERT INTO classifications (classification) VALUES (?)", (classification,))
            db.commit()
            # Return JSON success
            return jsonify(success=True, message=f'Classification \"{classification}\" added successfully!')
        except Exception as e:
            # Log the error for debugging
            #print(f"Database error adding classification: {e}") # Consider proper logging
            db.rollback() # Rollback changes on error
            # Return JSON error
            return jsonify(success=False, message=f'Error adding classification. Please try again later.')
    
    def delete_classification(self, classification):
        """
        Handles deleting a transaction classification.
        
        Args:
            classification: Classification to delete
            
        Returns:
            Redirect to the index page with a flash message
        """
        db = self.db_manager.get_db()
        cursor = db.cursor()
        
        # Check if classification is in use
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE classification = ?", (classification,))
        if cursor.fetchone()[0] > 0:
            flash(f'Cannot delete classification "{classification}" because it is in use by transactions.', 'danger')
            return redirect(url_for('index'))
        
        try:
            cursor.execute("DELETE FROM classifications WHERE classification = ?", (classification,))
            db.commit()
            if cursor.rowcount > 0:
                flash(f'Classification "{classification}" deleted successfully!', 'success')
            else:
                flash(f'Classification "{classification}" not found.', 'warning')
        except Exception as e:
            flash(f'Error deleting classification: {e}', 'danger')
        
        return redirect(url_for('index'))
    
    def check_usage(self, classification):
        """
        Check if a classification is in use by any transactions.
        
        Args:
            classification: Classification to check
            
        Returns:
            JSON response with usage information
        """
        db = self.db_manager.get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE classification = ?", (classification,))
        count = cursor.fetchone()[0]
        return jsonify({'classification': classification, 'in_use': count > 0, 'count': count})
    
    def get_page(self, page):
        """
        Get a page of transaction classifications.
        
        Args:
            page: Page number (1-indexed)
            
        Returns:
            JSON response with classifications and pagination information
        """
        result = self.get_paginated_classifications(page)
        return jsonify(result)
