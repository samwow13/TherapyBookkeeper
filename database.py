# -*- coding: utf-8 -*-
"""
Database Manager Module
Handles database connections and schema management for the Therapy Bookkeeping Application.
"""

import sqlite3
from flask import g, redirect, url_for, flash
from config import CLASSIFICATIONS, CODES

class DatabaseManager:
    """
    Manages database connections and schema for the application.
    """
    
    def __init__(self, app, database_path):
        """
        Initialize the database manager.
        
        Args:
            app: Flask application instance
            database_path: Path to the SQLite database file
        """
        self.app = app
        self.database_path = database_path
        
        # Set up teardown context
        @app.teardown_appcontext
        def close_connection(exception):
            """Closes the database at the end of the request."""
            db = getattr(g, '_database', None)
            if db is not None:
                db.close()
    
    def get_db(self):
        """
        Connects to the specific database.
        
        Returns:
            SQLite database connection with row factory set
        """
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self.database_path)
            db.row_factory = sqlite3.Row  # Return rows as dictionary-like objects
        return db
    
    def init_db_schema(self):
        """
        Initializes the database schema.
        Creates necessary tables if they don't exist.
        """
        db = self.get_db()
        cursor = db.cursor()
        
        # Create transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('credit', 'debit')),
                code TEXT,
                classification TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create table for transaction codes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE
            )
        ''')

        # Create table for transaction classifications
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                classification TEXT NOT NULL UNIQUE
            )
        ''')

        # Add default codes if codes table is empty
        cursor.execute("SELECT COUNT(*) FROM codes")
        if cursor.fetchone()[0] == 0:
            for code in CODES:
                try:
                    cursor.execute("INSERT INTO codes (code) VALUES (?)", (code,))
                except sqlite3.IntegrityError:
                    pass  # Ignore if code already exists (e.g., during re-init)

        # Add default classifications if classifications table is empty
        cursor.execute("SELECT COUNT(*) FROM classifications")
        if cursor.fetchone()[0] == 0:
            for classification in CLASSIFICATIONS:
                try:
                    cursor.execute("INSERT INTO classifications (classification) VALUES (?)", (classification,))
                except sqlite3.IntegrityError:
                    pass  # Ignore if classification already exists

        db.commit()
        print("Database tables created or already exist.")
    
    def update_db_schema(self):
        """
        Updates the database schema if needed.
        Adds columns or tables that might be missing from older versions.
        
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            db = self.get_db()
            cursor = db.cursor()

            # Check if code column exists
            cursor.execute("PRAGMA table_info(transactions)")
            columns = [column[1] for column in cursor.fetchall()]

            if 'code' not in columns:
                # Add the code column if it doesn't exist
                cursor.execute("ALTER TABLE transactions ADD COLUMN code TEXT")
                db.commit()
                print("Added 'code' column to transactions table")

            # Check if codes table exists and populate if needed (idempotent)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='codes'")
            if not cursor.fetchone():
                cursor.execute('''
                    CREATE TABLE codes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        code TEXT NOT NULL UNIQUE
                    )
                ''')
                print("Created 'codes' table.")
                
            # Ensure default codes exist
            for code in CODES:
                try:
                    cursor.execute("INSERT OR IGNORE INTO codes (code) VALUES (?)", (code,))
                except sqlite3.IntegrityError:  # Should be handled by IGNORE, but belt-and-suspenders
                    pass

            # Check if classifications table exists and populate if needed (idempotent)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='classifications'")
            if not cursor.fetchone():
                cursor.execute('''
                    CREATE TABLE classifications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        classification TEXT NOT NULL UNIQUE
                    )
                ''')
                print("Created 'classifications' table.")
                
            # Ensure default classifications exist
            for classification in CLASSIFICATIONS:
                try:
                    cursor.execute("INSERT OR IGNORE INTO classifications (classification) VALUES (?)", (classification,))
                except sqlite3.IntegrityError:
                    pass

            db.commit()
            print("Database schema checked/updated.")
            return True  # Indicate successful check/update

        except Exception as e:
            print(f"Error updating database schema: {e}")
            return False
    
    def init_db_route(self):
        """
        Route handler to initialize the database manually via browser.
        
        Returns:
            Redirect to the index page with a flash message
        """
        self.init_db_schema()
        flash('Database initialized successfully!', 'success')
        return redirect(url_for('index'))
    
    def update_db_route(self):
        """
        Route handler to update the database schema manually via browser.
        
        Returns:
            Redirect to the index page with a flash message
        """
        success = self.update_db_schema()
        if success:
            flash('Database schema updated successfully!', 'success')
        else:
            flash('Error updating database schema. Check server logs.', 'danger')
        return redirect(url_for('index'))
