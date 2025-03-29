# -*- coding: utf-8 -*-
"""
Delete Transaction Modal Template for the Therapy Bookkeeping Application.
This file contains the HTML template for the Delete Transaction modal.
"""

DELETE_TRANSACTION_MODAL = """<!-- Delete Transaction Modal -->
<div class="modal fade" id="deleteTransactionModal" tabindex="-1" aria-labelledby="deleteTransactionModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="deleteTransactionModalLabel">Confirm Delete</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <p>Are you sure you want to delete the transaction: <span id="delete_transaction_description" class="fw-bold"></span>?</p>
                <p class="text-danger"><i class="bi bi-exclamation-triangle-fill me-2"></i>This action cannot be undone.</p>
            </div>
            <div class="modal-footer">
                <form id="deleteTransactionForm" method="post" action="{{ url_for('delete_transaction', transaction_id=0) }}">
                    <input type="hidden" id="delete_transaction_id" name="transaction_id">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-danger">Delete Transaction</button>
                </form>
            </div>
        </div>
    </div>
</div>"""

# JavaScript to handle the Delete Transaction modal
DELETE_TRANSACTION_SCRIPT = """
// Set up delete transaction functionality
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    for (let btn of deleteButtons) {
        btn.addEventListener('click', function() {
            const transactionId = this.getAttribute('data-transaction-id');
            const description = this.getAttribute('data-description');
            
            document.getElementById('delete_transaction_id').value = transactionId;
            document.getElementById('delete_transaction_description').textContent = description;
            
            // Set the form action correctly with the transaction ID
            const form = document.getElementById('deleteTransactionForm');
            form.action = form.action.replace('/0', '/' + transactionId);
        });
    }
});
"""
