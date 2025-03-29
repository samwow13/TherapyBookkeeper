# -*- coding: utf-8 -*-
"""
Add Transaction Modal Template for the Therapy Bookkeeping Application.
This file contains the HTML template for the Add New Transaction modal.
"""

ADD_TRANSACTION_MODAL = """<!-- Add Transaction Modal -->
<div class="modal fade" id="addTransactionModal" tabindex="-1" aria-labelledby="addTransactionModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="addTransactionModalLabel">Add New Transaction</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form action="{{ url_for('add_transaction') }}" method="post">
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="date" class="form-label">Date</label>
                        <input type="date" class="form-control" id="date" name="date" required value="{{ suggested_date }}">
                    </div>
                    <div class="mb-3">
                        <label for="description" class="form-label">Description</label>
                        <input type="text" class="form-control" id="description" name="description" required>
                    </div>
                    <div class="mb-3">
                        <label for="amount" class="form-label">Amount</label>
                        <div class="input-group">
                            <span class="input-group-text">$</span>
                            <input type="number" step="0.01" min="0.01" class="form-control" id="amount" name="amount" required>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="type" class="form-label">Type</label>
                        <select class="form-select" id="type" name="type" required>
                            <option value="credit">Credit (Income)</option>
                            <option value="debit">Debit (Expense)</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="classification" class="form-label">Classification</label>
                        <select class="form-select" id="classification" name="classification" required>
                            {% for classification in classifications %}
                            <option value="{{ classification }}">{{ classification }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="code" class="form-label">Code</label>
                        <select class="form-select" id="code" name="code" required>
                            {% for code in codes %}
                            <option value="{{ code }}">{{ code }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Add Transaction</button>
                </div>
            </form>
        </div>
    </div>
</div>"""

# JavaScript functions related to the Add Transaction modal
ADD_TRANSACTION_SCRIPT = """
// Store last used date in localStorage when a transaction is added
const addTransactionForm = document.querySelector('#addTransactionModal form');
if (addTransactionForm) {
    addTransactionForm.addEventListener('submit', function() {
        // Get the date value from the form
        const dateValue = document.getElementById('date').value;
        if (dateValue) {
            // Store it in localStorage
            localStorage.setItem('lastTransactionDate', dateValue);
            console.log('Saved date to localStorage:', dateValue);
        }
    });
}

// Set date field when the add transaction modal is opened
const addTransactionModal = document.getElementById('addTransactionModal');
if (addTransactionModal) {
    addTransactionModal.addEventListener('show.bs.modal', function() {
        // Get the stored date from localStorage
        const lastDate = localStorage.getItem('lastTransactionDate');
        const dateField = document.getElementById('date');
        
        if (lastDate && dateField) {
            // Set the date field to the stored date
            dateField.value = lastDate;
            console.log('Restored date from localStorage:', lastDate);
        } else if (dateField) {
            // If no stored date, use today
            const today = new Date().toISOString().split('T')[0];
            dateField.value = today;
            console.log('No saved date, using today:', today);
        }
    });
}
"""
