# -*- coding: utf-8 -*-
"""
Add Transaction Modal Template for the Therapy Bookkeeping Application.
This file contains the HTML template for the Add New Transaction modal.
"""

ADD_TRANSACTION_MODAL = """
<!-- Add Transaction Modal -->
<div class="modal fade" id="addTransactionModal" tabindex="-1" aria-labelledby="addTransactionModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="addTransactionModalLabel">Add New Transaction</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form action="/add" method="post" id="addTransactionForm">
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="date" class="form-label">Date</label>
                        <input type="date" class="form-control" id="date" name="date" required>
                    </div>
                    <div class="mb-3">
                        <label for="description" class="form-label">Description</label>
                        <input type="text" class="form-control" id="description" name="description" required>
                    </div>
                    <div class="mb-3">
                        <label for="code" class="form-label">Code</label>
                        <select class="form-select" id="code" name="code" required>
                            {{ code_options|safe }}
                        </select>
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
                            {{ classification_options|safe }}
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
    // Set date when modal is shown
    const addTransactionModal = document.getElementById('addTransactionModal');
    if (addTransactionModal) {
        addTransactionModal.addEventListener('show.bs.modal', function() {
            const dateField = document.getElementById('date');
            if (dateField) {
                const lastDate = localStorage.getItem('lastTransactionDate');
                dateField.value = lastDate || new Date().toISOString().split('T')[0];
            }
            
            // Auto-fill amount field based on default selected code when modal opens
            const codeSelect = document.getElementById('code');
            const amountField = document.getElementById('amount');
            
            if (codeSelect && amountField && codeSelect.value) {
                // Extract the numeric part of the code
                const numericCode = codeSelect.value.replace(/\D/g, '');
                if (numericCode) {
                    amountField.value = numericCode;
                }
            }
        });
    }
    
    // Save date when form is submitted
    const addTransactionForm = document.getElementById('addTransactionForm');
    if (addTransactionForm) {
        addTransactionForm.addEventListener('submit', function() {
            const dateValue = document.getElementById('date').value;
            if (dateValue) {
                localStorage.setItem('lastTransactionDate', dateValue);
            }
        });
    }
    
    // Auto-fill amount field when code is selected
    const codeSelect = document.getElementById('code');
    if (codeSelect) {
        codeSelect.addEventListener('change', function() {
            const selectedCode = codeSelect.value;
            const amountField = document.getElementById('amount');
            
            if (selectedCode && amountField) {
                // Extract the numeric part of the code
                const numericCode = selectedCode.replace(/\D/g, '');
                if (numericCode) {
                    amountField.value = numericCode;
                }
            }
        });
    }
});
"""
