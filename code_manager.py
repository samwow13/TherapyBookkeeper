# -*- coding: utf-8 -*-
"""
Code Manager Module
Handles transaction code operations for the Therapy Bookkeeping Application.
"""

from flask import request, redirect, url_for, flash, jsonify

class CodeManager:
    """
    Manages transaction codes for the application.
    """
    
    def __init__(self, db_manager):
        """
        Initialize the code manager.
        
        Args:
            db_manager: DatabaseManager instance
        """
        self.db_manager = db_manager
    
    def get_all_codes(self):
        """
        Gets all codes without pagination.
        
        Returns:
            list: All transaction codes
        """
        db = self.db_manager.get_db()
        cursor = db.cursor()
        cursor.execute("SELECT code FROM codes ORDER BY code")
        return [row[0] for row in cursor.fetchall()]
    
    def get_paginated_codes(self, page=1, per_page=10):
        """
        Get transaction codes from the database with pagination.
        
        Args:
            page: Page number (1-indexed)
            per_page: Number of items per page
            
        Returns:
            dict: Pagination information and codes
        """
        db = self.db_manager.get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM codes")
        total_count = cursor.fetchone()[0]
        
        # Calculate pagination values
        total_pages = (total_count + per_page - 1) // per_page  # Ceiling division
        page = max(1, min(page, total_pages))  # Ensure page is within bounds
        offset = (page - 1) * per_page
        
        # Get codes for current page
        cursor.execute("SELECT code FROM codes ORDER BY code LIMIT ? OFFSET ?", 
                      (per_page, offset))
        codes = [row[0] for row in cursor.fetchall()]
        
        return {
            'codes': codes,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': total_pages
            }
        }
    
    def add_code(self):
        """
        Handles adding a new transaction code via AJAX.

        Returns:
            JSON response indicating success or failure.
        """
        code = request.form.get('newCodeInput', '').strip()
        if not code:
            # Return JSON error
            return jsonify(success=False, message='Code cannot be empty.')

        db = self.db_manager.get_db()
        cursor = db.cursor()

        try:
            # Check if code already exists
            cursor.execute("SELECT 1 FROM codes WHERE code = ?", (code,))
            if cursor.fetchone():
                return jsonify(success=False, message=f'Code \"{code}\" already exists.')

            cursor.execute("INSERT INTO codes (code) VALUES (?)", (code,))
            db.commit()
            # Return JSON success
            return jsonify(success=True, message=f'Code \"{code}\" added successfully!')
        except Exception as e:
            # Log the error for debugging
            print(f"Database error adding code: {e}") # Consider proper logging
            db.rollback() # Rollback changes on error
            # Return JSON error
            return jsonify(success=False, message=f'Error adding code. Please try again later.')
    
    def delete_code(self, code):
        """
        Handles deleting a transaction code.
        
        Args:
            code: Code to delete
            
        Returns:
            Redirect to the index page with a flash message
        """
        db = self.db_manager.get_db()
        cursor = db.cursor()
        
        # Check if code is in use
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE code = ?", (code,))
        if cursor.fetchone()[0] > 0:
            flash(f'Cannot delete code "{code}" because it is in use by transactions.', 'danger')
            return redirect(url_for('index'))
        
        try:
            cursor.execute("DELETE FROM codes WHERE code = ?", (code,))
            db.commit()
            if cursor.rowcount > 0:
                flash(f'Code "{code}" deleted successfully!', 'success')
            else:
                flash(f'Code "{code}" not found.', 'warning')
        except Exception as e:
            flash(f'Error deleting code: {e}', 'danger')
        
        return redirect(url_for('index'))
    
    def check_usage(self, code):
        """
        Check if a code is in use by any transactions.
        
        Args:
            code: Code to check
            
        Returns:
            JSON response with usage information
        """
        db = self.db_manager.get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE code = ?", (code,))
        count = cursor.fetchone()[0]
        return jsonify({'code': code, 'in_use': count > 0, 'count': count})
    
    def get_page(self, page):
        """
        Get a page of transaction codes.
        
        Args:
            page: Page number (1-indexed)
            
        Returns:
            JSON response with codes and pagination information
        """
        result = self.get_paginated_codes(page)
        return jsonify(result)
