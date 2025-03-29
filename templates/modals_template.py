# -*- coding: utf-8 -*-
"""
Modals Template for the Therapy Bookkeeping Application.
"""

MODALS_TEMPLATE = """{% block modals %}
<!-- Add Transaction Modal -->
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
                        <input type="date" class="form-control" id="date" name="date" required value="{{ today_date }}">
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
</div>

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
                <form id="deleteTransactionForm" action="/delete/" method="post">
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
                        {% if codes %}
                        <div class="table-responsive">
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>Code</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody id="codes-list">
                                    {% for code in codes %}
                                    <tr>
                                        <td>{{ code }}</td>
                                        <td>
                                            <form action="{{ url_for('delete_code', code=code) }}" method="post" class="d-inline delete-code-form" data-code="{{ code }}">
                                                <button type="button" class="btn btn-sm btn-outline-danger check-code-usage">Delete</button>
                                            </form>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                        {% else %}
                        <p class="text-muted">No codes defined yet.</p>
                        {% endif %}
                        <div class="alert alert-info mt-3">
                            <i class="bi bi-info-circle me-2"></i> Codes that are in use by existing transactions cannot be deleted.
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
                        {% if classifications %}
                        <div class="table-responsive">
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>Classification</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody id="classifications-list">
                                    {% for classification in classifications %}
                                    <tr>
                                        <td>{{ classification }}</td>
                                        <td>
                                            <form action="{{ url_for('delete_classification', classification=classification) }}" method="post" class="d-inline delete-classification-form" data-classification="{{ classification }}">
                                                <button type="button" class="btn btn-sm btn-outline-danger check-classification-usage">Delete</button>
                                            </form>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                        {% else %}
                        <p class="text-muted">No classifications defined yet.</p>
                        {% endif %}
                        <div class="alert alert-info mt-3">
                            <i class="bi bi-info-circle me-2"></i> Classifications that are in use by existing transactions cannot be deleted.
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
{% endblock %}

{% block scripts %}
<script>
// Initialize edit transaction modal with data
document.addEventListener('DOMContentLoaded', function() {
    const editTransactionModal = document.getElementById('editTransactionModal');
    if (editTransactionModal) {
        editTransactionModal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;
            
            // Extract data from button attributes
            const id = button.getAttribute('data-transaction-id');
            const date = button.getAttribute('data-date');
            const description = button.getAttribute('data-description');
            const amount = button.getAttribute('data-amount');
            const type = button.getAttribute('data-type');
            const code = button.getAttribute('data-code');
            const classification = button.getAttribute('data-classification');
            
            // Set values in form
            document.getElementById('edit_transaction_id').value = id;
            document.getElementById('edit_date').value = date;
            document.getElementById('edit_description').value = description;
            document.getElementById('edit_amount').value = amount;
            document.getElementById('edit_type').value = type;
            document.getElementById('edit_code').value = code;
            document.getElementById('edit_classification').value = classification;
            
            // Update the form action with the correct transaction ID
            const form = document.getElementById('editTransactionForm');
            form.action = '/edit/' + id;
        });
    }
    
    // Initialize delete transaction modal with data
    const deleteTransactionModal = document.getElementById('deleteTransactionModal');
    if (deleteTransactionModal) {
        deleteTransactionModal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;
            
            // Extract data from button attributes
            const id = button.getAttribute('data-transaction-id');
            const description = button.getAttribute('data-description');
            
            // Set values in form
            document.getElementById('delete_transaction_id').value = id;
            document.getElementById('delete_transaction_description').textContent = description;
            
            // Update the form action with the correct transaction ID
            const form = document.getElementById('deleteTransactionForm');
            form.action = '/delete/' + id;
        });
    }
});
</script>
{% endblock %}
"""
