# -*- coding: utf-8 -*-
"""
Edit Transaction Modal Template for the Therapy Bookkeeping Application.
This file contains the HTML template for the Edit Transaction modal.
"""

EDIT_TRANSACTION_MODAL = """<!-- Edit Transaction Modal -->
<div class="modal fade" id="editTransactionModal" tabindex="-1" aria-labelledby="editTransactionModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="editTransactionModalLabel">Edit Transaction</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form id="editTransactionForm" action="{{ url_for('edit_transaction', transaction_id=0) }}" method="post">
                <div class="modal-body">
                    <input type="hidden" id="edit_transaction_id" name="transaction_id">
                    <div class="mb-3">
                        <label for="edit_date" class="form-label">Date</label>
                        <input type="date" class="form-control" id="edit_date" name="date" required>
                    </div>
                    <div class="mb-3">
                        <label for="edit_description" class="form-label">Description</label>
                        <input type="text" class="form-control" id="edit_description" name="description" >
                    </div>
                    <div class="mb-3">
                        <label for="edit_amount" class="form-label">Amount</label>
                        <div class="input-group">
                            <span class="input-group-text">$</span>
                            <input type="number" step="0.01" min="0.01" class="form-control" id="edit_amount" name="amount" required>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="edit_type" class="form-label">Type</label>
                        <select class="form-select" id="edit_type" name="type" required>
                            <option value="credit">Credit (Income)</option>
                            <option value="debit">Debit (Expense)</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="edit_classification" class="form-label">Classification</label>
                        <select class="form-select" id="edit_classification" name="classification" required>
                            {{ classification_options|safe }}
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="edit_code" class="form-label">Code</label>
                        <select class="form-select" id="edit_code" name="code" required>
                            {{ code_options|safe }}
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Save Changes</button>
                </div>
            </form>
        </div>
    </div>
</div>"""

# JavaScript to handle the Edit Transaction modal
EDIT_TRANSACTION_SCRIPT = """
// Set form values when edit modal is shown
document.addEventListener('DOMContentLoaded', function() {
    // Handle edit button clicks to load transaction data
    const editButtons = document.querySelectorAll('.edit-btn');
    for (let btn of editButtons) {
        btn.addEventListener('click', function() {
            const transactionId = this.getAttribute('data-transaction-id');
            loadTransactionData(transactionId);
        });
    }
    
    // Function to fetch and load transaction data
    async function loadTransactionData(id) {
        try {
            // Use the direct API endpoint instead of template variables
            const response = await fetch(`/api/transaction/${id}`);
            if (!response.ok) {
                throw new Error('Failed to fetch transaction data');
            }
            
            const transaction = await response.json();
            console.log('Loaded transaction data:', transaction);
            
            // Set form action
            const form = document.getElementById('editTransactionForm');
            form.action = form.action.replace('/0', '/' + id);
            
            // Set hidden id field
            document.getElementById('edit_transaction_id').value = id;
            
            // Set other form fields
            document.getElementById('edit_date').value = transaction.date;
            document.getElementById('edit_description').value = transaction.description;
            document.getElementById('edit_amount').value = transaction.amount;
            document.getElementById('edit_type').value = transaction.type;
            
            // Set dropdown values - need to match values precisely
            const classificationSelect = document.getElementById('edit_classification');
            const codeSelect = document.getElementById('edit_code');
            
            // Find and select the correct classification option
            for (let i = 0; i < classificationSelect.options.length; i++) {
                if (classificationSelect.options[i].value === transaction.classification) {
                    classificationSelect.selectedIndex = i;
                    break;
                }
            }
            
            // Find and select the correct code option
            for (let i = 0; i < codeSelect.options.length; i++) {
                if (codeSelect.options[i].value === transaction.code) {
                    codeSelect.selectedIndex = i;
                    break;
                }
            }
            
        } catch (error) {
            console.error('Error loading transaction data:', error);
            alert('Failed to load transaction data. Please try again.');
        }
    }
});
"""
