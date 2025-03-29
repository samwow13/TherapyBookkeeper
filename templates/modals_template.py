# -*- coding: utf-8 -*-
"""
Modals Template for the Therapy Bookkeeping Application.
"""

# Import the add transaction modal
from templates.add_transaction_modal import ADD_TRANSACTION_MODAL, ADD_TRANSACTION_SCRIPT

MODALS_TEMPLATE = """
<!-- Add Transaction Modal -->
{{ add_transaction_modal|safe }}

<!-- Edit Transaction Modal -->
<div class="modal fade" id="editTransactionModal" tabindex="-1" aria-labelledby="editTransactionModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="editTransactionModalLabel">Edit Transaction</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form id="editTransactionForm" action="/edit/" method="post">
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
</div>

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
                <form id="deleteTransactionForm" method="post">
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

<!-- Print Year Modal -->
<div class="modal fade" id="printYearModal" tabindex="-1" aria-labelledby="printYearModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="printYearModalLabel">Print Year Report</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form action="{{ url_for('print_year_transactions', year=0) }}" method="get" id="printYearForm">
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="print_year" class="form-label">Select Year</label>
                        <select class="form-select" id="print_year" name="year" required>
                            {% for year in available_years %}
                            <option value="{{ year }}">{{ year }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Generate Report</button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Modal Scripts -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Add transaction modal scripts
    {{ add_transaction_script|safe }}
    
    // Set up editing transaction
    const editButtons = document.querySelectorAll('.edit-transaction');
    for (let btn of editButtons) {
        btn.addEventListener('click', function() {
            const transactionId = this.getAttribute('data-id');
            const date = this.getAttribute('data-date');
            const description = this.getAttribute('data-description');
            const amount = this.getAttribute('data-amount');
            const type = this.getAttribute('data-type');
            const classification = this.getAttribute('data-classification');
            const code = this.getAttribute('data-code');
            
            document.getElementById('edit_transaction_id').value = transactionId;
            document.getElementById('edit_date').value = date;
            document.getElementById('edit_description').value = description;
            document.getElementById('edit_amount').value = amount;
            document.getElementById('edit_type').value = type;
            document.getElementById('edit_classification').value = classification;
            document.getElementById('edit_code').value = code;
            
            // Set the form action correctly
            document.getElementById('editTransactionForm').action = "{{ url_for('edit_transaction', transaction_id=0) }}".replace('0', transactionId);
        });
    }
    
    // Set up deleting transaction
    const deleteButtons = document.querySelectorAll('.delete-transaction');
    for (let btn of deleteButtons) {
        btn.addEventListener('click', function() {
            const transactionId = this.getAttribute('data-id');
            const description = this.getAttribute('data-description');
            
            document.getElementById('delete_transaction_id').value = transactionId;
            document.getElementById('delete_transaction_description').textContent = description;
            
            // Set the form action correctly
            document.getElementById('deleteTransactionForm').action = "{{ url_for('delete_transaction', transaction_id=0) }}".replace('0', transactionId);
        });
    }
    
    // Set up print year form
    document.getElementById('printYearForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const year = document.getElementById('print_year').value;
        this.action = "{{ url_for('print_year_transactions', year=0) }}".replace('0', year);
        this.submit();
    });
    
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
