# -*- coding: utf-8 -*-
"""
Modals Template for the Therapy Bookkeeping Application.
"""

# Import the add transaction modal
from templates.add_transaction_modal import ADD_TRANSACTION_MODAL, ADD_TRANSACTION_SCRIPT
# Import edit transaction modal
from templates.edit_transaction_modal import EDIT_TRANSACTION_MODAL, EDIT_TRANSACTION_SCRIPT
# Import print modals
from templates.print_modals import PRINT_MODALS_HTML, PRINT_MODALS_SCRIPT

MODALS_TEMPLATE = """
<!-- Add Transaction Modal -->
{{ add_transaction_modal|safe }}

<!-- Edit Transaction Modal -->
{{ edit_transaction_modal|safe }}

<!-- Delete Transaction Modal -->
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
</div>

<!-- Edit Codes Modal -->
<div class="modal fade" id="editCodesModal" tabindex="-1" aria-labelledby="editCodesModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="editCodesModalLabel">Edit Codes & Classifications</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <ul class="nav nav-tabs" id="codesTab" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="codes-tab" data-bs-toggle="tab" data-bs-target="#codes-content" type="button" role="tab" aria-controls="codes-content" aria-selected="true">Transaction Codes</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="classifications-tab" data-bs-toggle="tab" data-bs-target="#classifications-content" type="button" role="tab" aria-controls="classifications-content" aria-selected="false">Classifications</button>
                    </li>
                </ul>
                <div class="tab-content mt-3" id="codesTabContent">
                    <!-- Codes Tab -->
                    <div class="tab-pane fade show active" id="codes-content" role="tabpanel" aria-labelledby="codes-tab">
                        <div class="row mb-3">
                            <div class="col-md-8">
                                <form action="{{ url_for('add_code') }}" method="post" class="d-flex">
                                    <input type="text" class="form-control me-2" name="new_code" placeholder="New Code" required>
                                    <button type="submit" class="btn btn-primary">Add</button>
                                </form>
                            </div>
                        </div>
                        
                        <div id="codes-container">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <h6 class="mb-0">Transaction Codes</h6>
                                <div>
                                    <button class="btn btn-sm btn-outline-secondary codes-prev-page" disabled>
                                        <i class="bi bi-arrow-left"></i>
                                    </button>
                                    <span class="mx-2 codes-page-info">Page 1</span>
                                    <button class="btn btn-sm btn-outline-secondary codes-next-page">
                                        <i class="bi bi-arrow-right"></i>
                                    </button>
                                </div>
                            </div>
                            
                            <ul class="list-group codes-list">
                                {% for code in codes %}
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    {{ code }}
                                    <button type="button" class="btn btn-sm btn-outline-danger delete-code" data-code="{{ code }}">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </li>
                                {% endfor %}
                            </ul>
                        </div>
                    </div>
                    
                    <!-- Classifications Tab -->
                    <div class="tab-pane fade" id="classifications-content" role="tabpanel" aria-labelledby="classifications-tab">
                        <div class="row mb-3">
                            <div class="col-md-8">
                                <form action="{{ url_for('add_classification') }}" method="post" class="d-flex">
                                    <input type="text" class="form-control me-2" name="new_classification" placeholder="New Classification" required>
                                    <button type="submit" class="btn btn-primary">Add</button>
                                </form>
                            </div>
                        </div>
                        
                        <div id="classifications-container">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <h6 class="mb-0">Transaction Classifications</h6>
                                <div>
                                    <button class="btn btn-sm btn-outline-secondary classifications-prev-page" disabled>
                                        <i class="bi bi-arrow-left"></i>
                                    </button>
                                    <span class="mx-2 classifications-page-info">Page 1</span>
                                    <button class="btn btn-sm btn-outline-secondary classifications-next-page">
                                        <i class="bi bi-arrow-right"></i>
                                    </button>
                                </div>
                            </div>
                            
                            <ul class="list-group classifications-list">
                                {% for classification in classifications %}
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    {{ classification }}
                                    <button type="button" class="btn btn-sm btn-outline-danger delete-classification" data-classification="{{ classification }}">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </li>
                                {% endfor %}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            </div>
        </div>
    </div>
</div>

<!-- Print Modals -->
{{ print_modals_html|safe }}

<!-- Modal Scripts -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Add transaction modal scripts
    {{ add_transaction_script|safe }}
    
    // Edit transaction modal scripts
    {{ edit_transaction_script|safe }}
    
    // Print modals scripts
    {{ print_modals_script|safe }}
    
    // Set up deleting transaction
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
    
    // Code deletion
    const deleteCodeButtons = document.querySelectorAll('.delete-code');
    deleteCodeButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const code = this.getAttribute('data-code');
            
            // First check if the code is in use
            try {
                const response = await fetch(`{{ url_for('check_code_usage', code='PLACEHOLDER') }}`.replace('PLACEHOLDER', encodeURIComponent(code)));
                const data = await response.json();
                
                if (data.in_use) {
                    alert(`Cannot delete code "${code}" because it is being used by ${data.count} transaction(s).`);
                    return;
                }
                
                // Not in use, proceed with deletion confirmation
                if (confirm(`Are you sure you want to delete the code "${code}"?`)) {
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = `{{ url_for('delete_code', code='PLACEHOLDER') }}`.replace('PLACEHOLDER', encodeURIComponent(code));
                    document.body.appendChild(form);
                    form.submit();
                }
            } catch (error) {
                console.error("Error checking code usage:", error);
                alert("An error occurred while checking if the code is in use.");
            }
        });
    });
    
    // Classification deletion
    const deleteClassificationButtons = document.querySelectorAll('.delete-classification');
    deleteClassificationButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const classification = this.getAttribute('data-classification');
            
            // First check if the classification is in use
            try {
                const response = await fetch(`{{ url_for('check_classification_usage', classification='PLACEHOLDER') }}`.replace('PLACEHOLDER', encodeURIComponent(classification)));
                const data = await response.json();
                
                if (data.in_use) {
                    alert(`Cannot delete classification "${classification}" because it is being used by ${data.count} transaction(s).`);
                    return;
                }
                
                // Not in use, proceed with deletion confirmation
                if (confirm(`Are you sure you want to delete the classification "${classification}"?`)) {
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = `{{ url_for('delete_classification', classification='PLACEHOLDER') }}`.replace('PLACEHOLDER', encodeURIComponent(classification));
                    document.body.appendChild(form);
                    form.submit();
                }
            } catch (error) {
                console.error("Error checking classification usage:", error);
                alert("An error occurred while checking if the classification is in use.");
            }
        });
    });
});
</script>
"""
