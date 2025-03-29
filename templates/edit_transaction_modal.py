# -*- coding: utf-8 -*-
"""
Edit Transaction Modal Template for the Therapy Bookkeeping Application.
This file contains the HTML template and scripts for the Edit Transaction modal.
"""

EDIT_TRANSACTION_MODAL = """<!-- Edit Transaction Modal -->
<div class="modal fade" id="editTransactionModal" tabindex="-1" aria-labelledby="editTransactionModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="editTransactionModalLabel">Edit Transaction</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form id="editTransactionForm" action="" method="post">
                <div class="modal-body">
                    <input type="hidden" id="edit_transaction_id" name="transaction_id">
                    <div class="mb-3">
                        <label for="edit_date" class="form-label">Date</label>
                        <input type="date" class="form-control" id="edit_date" name="date" required>
                    </div>
                    <div class="mb-3">
                        <label for="edit_description" class="form-label">Description</label>
                        <input type="text" class="form-control" id="edit_description" name="description" required>
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
                            {% for classification in classifications %}
                            <option value="{{ classification }}">{{ classification }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="edit_code" class="form-label">Code</label>
                        <select class="form-select" id="edit_code" name="code" required>
                            {% for code in codes %}
                            <option value="{{ code }}">{{ code }}</option>
                            {% endfor %}
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

# JavaScript functions related to the Edit Transaction modal
EDIT_TRANSACTION_SCRIPT = """
// Set up editing transaction functionality
document.addEventListener('DOMContentLoaded', function() {
    // Find all edit buttons and attach event listeners
    const editButtons = document.querySelectorAll('.edit-btn');
    
    editButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Get transaction ID from button attribute
            const transactionId = this.getAttribute('data-transaction-id');
            
            if (!transactionId) {
                console.error('No transaction ID provided');
                return;
            }
            
            console.log('Edit button clicked for transaction ID:', transactionId);
            
            // Fetch transaction data from API
            fetch(`/api/transaction/${transactionId}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(transaction => {
                    console.log('Transaction data loaded:', transaction);
                    
                    // Set form values from API data
                    document.getElementById('edit_transaction_id').value = transaction.id;
                    document.getElementById('edit_date').value = transaction.date;
                    document.getElementById('edit_description').value = transaction.description;
                    document.getElementById('edit_amount').value = transaction.amount;
                    document.getElementById('edit_type').value = transaction.type;
                    
                    // Select the correct classification option
                    const classificationSelect = document.getElementById('edit_classification');
                    for (let i = 0; i < classificationSelect.options.length; i++) {
                        if (classificationSelect.options[i].value === transaction.classification) {
                            classificationSelect.selectedIndex = i;
                            break;
                        }
                    }
                    
                    // Select the correct code option
                    const codeSelect = document.getElementById('edit_code');
                    for (let i = 0; i < codeSelect.options.length; i++) {
                        if (codeSelect.options[i].value === transaction.code) {
                            codeSelect.selectedIndex = i;
                            break;
                        }
                    }
                    
                    // Set the form action URL
                    document.getElementById('editTransactionForm').action = "/edit/" + transaction.id;
                })
                .catch(error => {
                    console.error('Error fetching transaction data:', error);
                    alert('Failed to load transaction data. Please try again.');
                });
        });
    });
    
    // Set up modal event handler for when the edit modal is shown
    const editTransactionModal = document.getElementById('editTransactionModal');
    if (editTransactionModal) {
        editTransactionModal.addEventListener('show.bs.modal', function(event) {
            // Get the button that triggered the modal
            const button = event.relatedTarget;
            
            if (button && button.classList.contains('edit-btn')) {
                // Get transaction ID from button attribute
                const transactionId = button.getAttribute('data-transaction-id');
                
                if (!transactionId) {
                    console.error('No transaction ID provided');
                    return;
                }
                
                console.log('Modal shown for transaction ID:', transactionId);
                
                // Fetch transaction data from API
                fetch(`/api/transaction/${transactionId}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(transaction => {
                        console.log('Transaction data loaded:', transaction);
                        
                        // Set form values from API data
                        document.getElementById('edit_transaction_id').value = transaction.id;
                        document.getElementById('edit_date').value = transaction.date;
                        document.getElementById('edit_description').value = transaction.description;
                        document.getElementById('edit_amount').value = transaction.amount;
                        document.getElementById('edit_type').value = transaction.type;
                        
                        // Select the correct classification option
                        const classificationSelect = document.getElementById('edit_classification');
                        for (let i = 0; i < classificationSelect.options.length; i++) {
                            if (classificationSelect.options[i].value === transaction.classification) {
                                classificationSelect.selectedIndex = i;
                                break;
                            }
                        }
                        
                        // Select the correct code option
                        const codeSelect = document.getElementById('edit_code');
                        for (let i = 0; i < codeSelect.options.length; i++) {
                            if (codeSelect.options[i].value === transaction.code) {
                                codeSelect.selectedIndex = i;
                                break;
                            }
                        }
                        
                        // Set the form action URL
                        document.getElementById('editTransactionForm').action = "/edit/" + transaction.id;
                    })
                    .catch(error => {
                        console.error('Error fetching transaction data:', error);
                        alert('Failed to load transaction data. Please try again.');
                    });
            }
        });
        
        // Reset form when modal is hidden
        editTransactionModal.addEventListener('hidden.bs.modal', function() {
            document.getElementById('editTransactionForm').reset();
        });
    }
});
"""
