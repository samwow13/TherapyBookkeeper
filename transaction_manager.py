# -*- coding: utf-8 -*-
"""
Transaction Manager Module for the Therapy Bookkeeping Application.

This module handles all transaction-related operations including:
- Adding new transactions
- Editing existing transactions
- Deleting transactions
- Retrieving transaction data with various filters
- Calculating financial summaries
"""

import sqlite3
from datetime import datetime
from collections import defaultdict
from flask import request, redirect, url_for, flash, g
from database import DatabaseManager
from template_loader import INDEX_TEMPLATE, PRINT_TEMPLATE

class TransactionManager:
    """
    Manages all transaction-related operations for the Therapy Bookkeeping application.
    """
    
    def __init__(self, app, db_manager):
        """
        Initialize the TransactionManager with the Flask app and database manager.
        
        Args:
            app: The Flask application instance
            db_manager: The DatabaseManager instance for database operations
        """
        self.app = app
        self.db_manager = db_manager
        
    def get_db(self):
        """
        Get a database connection.
        
        Returns:
            A database connection object
        """
        return self.db_manager.get_db()
    
    def add_transaction(self):
        """
        Handle adding a new transaction.
        
        Returns:
            A redirect to the index page
        """
        if request.method == 'POST':
            date = request.form.get('date')
            description = request.form.get('description')
            amount = request.form.get('amount')
            transaction_type = request.form.get('type')
            code = request.form.get('code')
            classification = request.form.get('classification')
            
            # Validate inputs
            if not date or not description or not amount or not transaction_type:
                flash('All fields are required.', 'danger')
                return redirect(url_for('index'))
            
            try:
                # Convert amount to float for validation
                amount = float(amount)
                if amount <= 0:
                    flash('Amount must be greater than zero.', 'danger')
                    return redirect(url_for('index'))
                
                # Insert transaction into database
                db = self.get_db()
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO transactions (date, description, amount, type, code, classification) VALUES (?, ?, ?, ?, ?, ?)",
                    (date, description, amount, transaction_type, code, classification)
                )
                db.commit()
                
                flash('Transaction added successfully!', 'success')
            except ValueError:
                flash('Invalid amount format.', 'danger')
            except sqlite3.Error as e:
                flash(f'Database error: {e}', 'danger')
                
        return redirect(url_for('index'))
    
    def edit_transaction(self, transaction_id):
        """
        Handle editing an existing transaction.
        
        Args:
            transaction_id: ID of the transaction to edit
            
        Returns:
            A redirect to the index page
        """
        if request.method == 'POST':
            date = request.form.get('date')
            description = request.form.get('description')
            amount = request.form.get('amount')
            transaction_type = request.form.get('type')
            code = request.form.get('code')
            classification = request.form.get('classification')
            
            # Validate inputs
            if not date or not description or not amount or not transaction_type:
                flash('All fields are required.', 'danger')
                return redirect(url_for('index'))
            
            try:
                # Convert amount to float for validation
                amount = float(amount)
                if amount <= 0:
                    flash('Amount must be greater than zero.', 'danger')
                    return redirect(url_for('index'))
                
                # Update transaction in database
                db = self.get_db()
                cursor = db.cursor()
                cursor.execute(
                    "UPDATE transactions SET date=?, description=?, amount=?, type=?, code=?, classification=? WHERE id=?",
                    (date, description, amount, transaction_type, code, classification, transaction_id)
                )
                db.commit()
                
                if cursor.rowcount > 0:
                    flash('Transaction updated successfully!', 'success')
                else:
                    flash('Transaction not found.', 'warning')
            except ValueError:
                flash('Invalid amount format.', 'danger')
            except sqlite3.Error as e:
                flash(f'Database error: {e}', 'danger')
                
        return redirect(url_for('index'))
    
    def delete_transaction(self, transaction_id):
        """
        Handle deleting a transaction.
        
        Args:
            transaction_id: ID of the transaction to delete
            
        Returns:
            A redirect to the index page
        """
        # Process the deletion regardless of request method (GET or POST)
        try:
            # Delete transaction from database
            db = self.get_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
            db.commit()
            
            if cursor.rowcount > 0:
                flash('Transaction deleted successfully!', 'success')
            else:
                flash('Transaction not found.', 'warning')
        except sqlite3.Error as e:
            flash(f'Database error: {e}', 'danger')
                
        return redirect(url_for('index'))
    
    def get_all_transactions(self):
        """
        Get all transactions from the database.
        
        Returns:
            A list of all transactions
        """
        db = self.get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        return cursor.fetchall()
    
    def get_recent_transactions(self, limit=50):
        """
        Get the most recent transactions.
        
        Args:
            limit: Maximum number of transactions to return
            
        Returns:
            A list of recent transactions
        """
        db = self.get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC LIMIT ?", (limit,))
        return cursor.fetchall()
    
    def get_transactions_by_month(self, month):
        """
        Get transactions for a specific month.
        
        Args:
            month: Month in format 'YYYY-MM'
            
        Returns:
            A list of transactions for the specified month
        """
        db = self.get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM transactions WHERE date LIKE ? ORDER BY date DESC",
            (f"{month}%",)
        )
        return cursor.fetchall()
    
    def get_transactions_by_year(self, year):
        """
        Get transactions for a specific year.
        
        Args:
            year: Year in format 'YYYY'
            
        Returns:
            A list of transactions for the specified year
        """
        db = self.get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM transactions WHERE date LIKE ? ORDER BY date DESC",
            (f"{year}%",)
        )
        return cursor.fetchall()
    
    def get_paginated_transactions(self, page=1, per_page=50):
        """
        Get transactions with pagination.
        
        Args:
            page: Page number (1-indexed)
            per_page: Number of transactions per page
            
        Returns:
            A tuple of (transactions, pagination_info)
        """
        db = self.get_db()
        cursor = db.cursor()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM transactions")
        total_count = cursor.fetchone()[0]
        
        # Calculate pagination values
        total_pages = (total_count + per_page - 1) // per_page  # Ceiling division
        page = max(1, min(page, total_pages))  # Ensure page is within bounds
        offset = (page - 1) * per_page
        
        # Get transactions for current page
        cursor.execute(
            "SELECT * FROM transactions ORDER BY date DESC LIMIT ? OFFSET ?",
            (per_page, offset)
        )
        transactions = cursor.fetchall()
        
        # Pagination info
        pagination = {
            'page': page,
            'per_page': per_page,
            'total_count': total_count,
            'total_pages': total_pages
        }
        
        return transactions, pagination
    
    def calculate_overall_totals(self):
        """
        Calculate overall financial totals.
        
        Returns:
            A tuple of (income, expense, net)
        """
        db = self.get_db()
        cursor = db.cursor()
        
        # Calculate total income
        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE type='credit'"
        )
        income = cursor.fetchone()[0] or 0
        
        # Calculate total expense
        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE type='debit'"
        )
        expense = cursor.fetchone()[0] or 0
        
        # Calculate net income
        net = income - expense
        
        return income, expense, net
    
    def calculate_monthly_totals(self):
        """
        Calculate financial totals grouped by month.
        
        Returns:
            A list of monthly totals with income, expense, and net values
        """
        db = self.get_db()
        cursor = db.cursor()
        
        # Get all transactions
        cursor.execute("SELECT date, amount, type, code FROM transactions ORDER BY date DESC")
        transactions = cursor.fetchall()
        
        # Group transactions by month
        monthly_data = defaultdict(lambda: {'income': 0, 'expense': 0, 'net': 0, 'codes': defaultdict(lambda: {'income': 0, 'expense': 0, 'net': 0})})
        
        for tx in transactions:
            # Extract year and month from date (format: YYYY-MM-DD)
            if not tx['date']:
                continue
                
            date_parts = tx['date'].split('-')
            if len(date_parts) < 2:
                continue
                
            year_month = f"{date_parts[0]}-{date_parts[1]}"
            month_display = datetime.strptime(year_month, '%Y-%m').strftime('%B %Y')
            
            # Update monthly totals
            amount = float(tx['amount'])
            if tx['type'] == 'credit':
                monthly_data[year_month]['income'] += amount
                monthly_data[year_month]['net'] += amount
                
                # Update code totals if code exists
                if tx['code']:
                    monthly_data[year_month]['codes'][tx['code']]['income'] += amount
                    monthly_data[year_month]['codes'][tx['code']]['net'] += amount
            else:  # debit
                monthly_data[year_month]['expense'] += amount
                monthly_data[year_month]['net'] -= amount
                
                # Update code totals if code exists
                if tx['code']:
                    monthly_data[year_month]['codes'][tx['code']]['expense'] += amount
                    monthly_data[year_month]['codes'][tx['code']]['net'] -= amount
        
        # Convert to list and add month display name
        monthly_totals = []
        for month_key, data in sorted(monthly_data.items(), reverse=True):
            month_obj = datetime.strptime(month_key, '%Y-%m')
            month_display = month_obj.strftime('%B %Y')
            
            monthly_totals.append({
                'month_key': month_key,
                'month': month_display,
                'income': data['income'],
                'expense': data['expense'],
                'net': data['net'],
                'codes': data['codes']
            })
        
        return monthly_totals
    
    def calculate_code_totals(self):
        """
        Calculate financial totals grouped by transaction code.
        
        Returns:
            A dictionary of code totals with income, expense, and net values
        """
        db = self.get_db()
        cursor = db.cursor()
        
        # Get all transactions with codes
        cursor.execute("SELECT amount, type, code FROM transactions WHERE code IS NOT NULL AND code != ''")
        transactions = cursor.fetchall()
        
        # Group transactions by code
        code_totals = defaultdict(lambda: {'income': 0, 'expense': 0, 'net': 0})
        
        for tx in transactions:
            amount = float(tx['amount'])
            code = tx['code']
            
            if tx['type'] == 'credit':
                code_totals[code]['income'] += amount
                code_totals[code]['net'] += amount
            else:  # debit
                code_totals[code]['expense'] += amount
                code_totals[code]['net'] -= amount
        
        return dict(code_totals)
    
    def get_transactions_by_month_dict(self):
        """
        Get all transactions organized by month.
        
        Returns:
            A dictionary with month_key as the key and transaction list for that month as value
        """
        db = self.get_db()
        cursor = db.cursor()
        
        # Get all transactions
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        transactions = cursor.fetchall()
        
        # Group transactions by month
        transactions_by_month = {}
        
        for tx in transactions:
            # Extract year and month from date (format: YYYY-MM-DD)
            if not tx['date']:
                continue
                
            date_parts = tx['date'].split('-')
            if len(date_parts) < 2:
                continue
                
            year_month = f"{date_parts[0]}-{date_parts[1]}"
            month_obj = datetime.strptime(year_month, '%Y-%m')
            month_display = month_obj.strftime('%B %Y')
            
            # Initialize month data if not exists
            if year_month not in transactions_by_month:
                transactions_by_month[year_month] = {
                    'month_name': month_display,
                    'transactions': []
                }
            
            # Add transaction to the month
            transactions_by_month[year_month]['transactions'].append(tx)
        
        # Sort the months by date (most recent first)
        return dict(sorted(transactions_by_month.items(), reverse=True))
    
    def index_view(self, month=None):
        """
        Render the index view with transactions and financial summary.
        
        Args:
            month: Optional month filter in format 'YYYY-MM'
            
        Returns:
            Rendered HTML for the index page
        """
        from flask import render_template_string
        
        # Get all codes and classifications for dropdowns
        db = self.get_db()
        cursor = db.cursor()
        
        # Get codes and classifications
        cursor.execute("SELECT code FROM codes ORDER BY code")
        codes = [row['code'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT classification FROM classifications ORDER BY classification")
        classifications = [row['classification'] for row in cursor.fetchall()]
        
        # Get transactions based on month filter
        if month:
            # Filter transactions by month
            cursor.execute(
                "SELECT * FROM transactions WHERE date LIKE ? ORDER BY date DESC",
                (f"{month}%",)
            )
            transactions = cursor.fetchall()
            
            # Calculate totals for this month
            cursor.execute(
                "SELECT SUM(amount) FROM transactions WHERE date LIKE ? AND type='credit'",
                (f"{month}%",)
            )
            income = cursor.fetchone()[0] or 0
            
            cursor.execute(
                "SELECT SUM(amount) FROM transactions WHERE date LIKE ? AND type='debit'",
                (f"{month}%",)
            )
            expenses = cursor.fetchone()[0] or 0
        else:
            # Get recent transactions (default view)
            cursor.execute(
                "SELECT * FROM transactions ORDER BY date DESC LIMIT 50"
            )
            transactions = cursor.fetchall()
            
            # Calculate overall totals
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='credit'")
            income = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='debit'")
            expenses = cursor.fetchone()[0] or 0
        
        # Calculate net income
        net_income = income - expenses
        
        # Get monthly summaries
        monthly_totals = self.calculate_monthly_totals()
        
        # Get code summaries
        code_totals = self.calculate_code_totals()
        
        # Get all transactions organized by month for the "All Transactions" section
        transactions_by_month = self.get_transactions_by_month_dict()
        
        # Get all transactions for fallback if needed
        all_transactions = self.get_all_transactions()
        
        # Calculate overall totals for summary cards
        overall_income, overall_expense, overall_net = self.calculate_overall_totals()
        
        # Render the template
        return render_template_string(
            INDEX_TEMPLATE,
            transactions=transactions,
            codes=codes,
            classifications=classifications,
            income=income,
            expenses=expenses,
            net_income=net_income,
            monthly_totals=monthly_totals,
            code_totals=code_totals,
            overall_income=overall_income,
            overall_expense=overall_expense,
            overall_net=overall_net,
            selected_month=month,
            transactions_by_month=transactions_by_month,
            all_transactions=all_transactions,
            monthly_transactions=transactions if month else None
        )
        
    def print_month_view(self, month):
        """
        Render a print-friendly view of transactions for a given month.
        
        Args:
            month: Month in format 'YYYY-MM'
            
        Returns:
            Rendered HTML for the print page
        """
        from flask import render_template_string
        
        # Get transactions for the specified month
        transactions = self.get_transactions_by_month(month)
        
        # Calculate totals for this month
        db = self.get_db()
        cursor = db.cursor()
        
        # Calculate income
        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE date LIKE ? AND type='credit'",
            (f"{month}%",)
        )
        income = cursor.fetchone()[0] or 0
        
        # Calculate expenses
        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE date LIKE ? AND type='debit'",
            (f"{month}%",)
        )
        expenses = cursor.fetchone()[0] or 0
        
        # Calculate net income
        net_income = income - expenses
        
        # Format month for display
        month_display = datetime.strptime(month, '%Y-%m').strftime('%B %Y')
        
        # Render the template
        return render_template_string(
            PRINT_TEMPLATE,
            transactions=transactions,
            summary={'total_income': income, 'total_expenses': expenses, 'net_income': net_income},
            period_type='month',
            month_name=month_display,
            year=month.split('-')[0]
        )
        
    def print_all_view(self):
        """
        Render a print-friendly view of all transactions with pagination.
        
        Returns:
            Rendered HTML for the print page
        """
        from flask import render_template_string, request
        
        # Get page parameter
        page = request.args.get('page', 1, type=int)
        per_page = 100  # More transactions per page for print view
        
        # Get paginated transactions
        transactions, pagination = self.get_paginated_transactions(page, per_page)
        
        # Calculate overall totals
        income, expenses, net_income = self.calculate_overall_totals()
        
        # Render the template
        return render_template_string(
            PRINT_TEMPLATE,
            transactions=transactions,
            summary={'total_income': income, 'total_expenses': expenses, 'net_income': net_income},
            period_type='all',
            pagination=pagination
        )
        
    def print_year_view(self, year):
        """
        Render a print-friendly view of transactions for a specific year.
        
        Args:
            year: Year in format 'YYYY'
            
        Returns:
            Rendered HTML for the print page
        """
        from flask import render_template_string
        
        # Get transactions for the specified year
        transactions = self.get_transactions_by_year(year)
        
        # Calculate totals for this year
        db = self.get_db()
        cursor = db.cursor()
        
        # Calculate income
        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE date LIKE ? AND type='credit'",
            (f"{year}%",)
        )
        income = cursor.fetchone()[0] or 0
        
        # Calculate expenses
        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE date LIKE ? AND type='debit'",
            (f"{year}%",)
        )
        expenses = cursor.fetchone()[0] or 0
        
        # Calculate net income
        net_income = income - expenses
        
        # Render the template
        return render_template_string(
            PRINT_TEMPLATE,
            transactions=transactions,
            summary={'total_income': income, 'total_expenses': expenses, 'net_income': net_income},
            period_type='year',
            year=year
        )
