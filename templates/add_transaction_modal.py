# -*- coding: utf-8 -*-
"""
Add Transaction Modal Template for the Therapy Bookkeeping Application.
This file contains the HTML template for the Add New Transaction modal.
"""

ADD_TRANSACTION_MODAL = """
<div class="modal fade" id="addTransactionModal" tabindex="-1" aria-labelledby="addTransactionModalLabel" aria-hidden="true" style="z-index: 1050 !important;">
    <div class="modal-dialog">
        <div class="modal-content" style="pointer-events: auto !important;">
            <div class="modal-header">
                <h5 class="modal-title" id="addTransactionModalLabel">Add New Transaction</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form action="/add_transaction" method="post" id="addTransactionForm">
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="date" class="form-label">Date</label>
                        <input type="date" class="form-control" id="date" name="date" required style="pointer-events: auto !important; z-index: 1060 !important;">
                    </div>
                    <div class="mb-3">
                        <label for="description" class="form-label">Description</label>
                        <input type="text" class="form-control" id="description" name="description" required style="pointer-events: auto !important; z-index: 1060 !important;">
                    </div>
                    <div class="mb-3">
                        <label for="amount" class="form-label">Amount</label>
                        <div class="input-group">
                            <span class="input-group-text">$</span>
                            <input type="number" step="0.01" min="0.01" class="form-control" id="amount" name="amount" required style="pointer-events: auto !important; z-index: 1060 !important;">
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="type" class="form-label">Type</label>
                        <select class="form-select" id="type" name="type" required style="pointer-events: auto !important; z-index: 1060 !important;">
                            <option value="credit">Credit (Income)</option>
                            <option value="debit">Debit (Expense)</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="classification" class="form-label">Classification</label>
                        <select class="form-select" id="classification" name="classification" required style="pointer-events: auto !important; z-index: 1060 !important;">
                            {{ classification_options|safe }}
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="code" class="form-label">Code</label>
                        <select class="form-select" id="code" name="code" required style="pointer-events: auto !important; z-index: 1060 !important;">
                            {{ code_options|safe }}
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
</div>
"""

# JavaScript functions related to the Add Transaction modal
ADD_TRANSACTION_SCRIPT = """
document.addEventListener('DOMContentLoaded', function() {
    // Make sure modal is properly initialized
    const addTransactionModal = document.getElementById('addTransactionModal');
    if (addTransactionModal) {
        // Remove any event listeners to prevent conflicts
        const newModal = addTransactionModal.cloneNode(true);
        addTransactionModal.parentNode.replaceChild(newModal, addTransactionModal);
        
        // Ensure the form submission still works
        const addTransactionForm = document.getElementById('addTransactionForm');
        if (addTransactionForm) {
            addTransactionForm.addEventListener('submit', function() {
                const dateValue = document.getElementById('date').value;
                if (dateValue) {
                    localStorage.setItem('lastTransactionDate', dateValue);
                }
            });
        }
        
        // Properly initialize the modal
        const modal = new bootstrap.Modal(newModal);
        
        // Fix any buttons that trigger this modal
        document.querySelectorAll('[data-bs-target="#addTransactionModal"]').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Clean up any existing backdrops
                document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
                
                // Set date field
                const dateField = document.getElementById('date');
                if (dateField) {
                    const lastDate = localStorage.getItem('lastTransactionDate');
                    if (lastDate) {
                        dateField.value = lastDate;
                    } else {
                        const today = new Date().toISOString().split('T')[0];
                        dateField.value = today;
                    }
                }
                
                // Show the modal
                modal.show();
            });
        });
    }
});
"""
