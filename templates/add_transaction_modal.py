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
                        <input type="text" class="form-control" id="description" name="description">
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
    const addTransactionModalEl = document.getElementById('addTransactionModal');
    const addTransactionForm = document.getElementById('addTransactionForm');
    const codeSelect = document.getElementById('code');
    const amountField = document.getElementById('amount');
    const dateField = document.getElementById('date');
    const descriptionField = document.getElementById('description');
    const typeSelect = document.getElementById('type');
    const classificationSelect = document.getElementById('classification');

    if (addTransactionModalEl) {
        addTransactionModalEl.addEventListener('show.bs.modal', function(event) {
            // Check if modal was triggered by a button with data attributes (copy button)
            const button = event.relatedTarget;
            let isCopyOperation = false;
            
            if (button && button.classList.contains('copy-btn')) {
                isCopyOperation = true;
                
                // Fill in values from the data attributes
                if (dateField && button.dataset.date) {
                    dateField.value = button.dataset.date;
                }
                
                if (descriptionField && button.dataset.description) {
                    descriptionField.value = button.dataset.description;
                }
                
                if (amountField && button.dataset.amount) {
                    amountField.value = button.dataset.amount;
                }
                
                if (typeSelect && button.dataset.type) {
                    typeSelect.value = button.dataset.type;
                }
                
                if (classificationSelect && button.dataset.classification) {
                    classificationSelect.value = button.dataset.classification;
                }
                
                if (codeSelect && button.dataset.code) {
                    codeSelect.value = button.dataset.code;
                }
                
                // Change modal title to reflect copy operation
                const modalTitle = document.getElementById('addTransactionModalLabel');
                if (modalTitle) {
                    modalTitle.textContent = 'Copy Transaction';
                }
            }
            
            // If not a copy operation, use the default behavior
            if (!isCopyOperation) {
                // Log the state of the classification dropdown (optional, can be removed later)
                if (classificationSelect) {
                    console.log('--- Add Transaction Modal --- ');
                    console.log('Classification dropdown initial value before setting:', classificationSelect.value);
                    
                    // *** Force default value to "Client Income" ***
                    classificationSelect.value = "Client Income";
                    console.log('Classification dropdown value set to:', classificationSelect.value);
                } else {
                    console.error('Classification select element not found!');
                }

                // Set date field value with last used date or current date
                if (dateField) {
                    const lastDate = localStorage.getItem('lastTransactionDate');
                    dateField.value = lastDate || new Date().toISOString().split('T')[0];
                }

                // Set code field with last used code or default to "125"
                if (codeSelect) {
                    const lastCode = localStorage.getItem('lastTransactionCode');
                    if (lastCode) {
                        codeSelect.value = lastCode;
                        console.log('Using last used code:', lastCode);
                    } else {
                        // Default to code "125" if no last code found
                        const defaultOptions = Array.from(codeSelect.options);
                        const code125Option = defaultOptions.find(option => option.value === "125");
                        if (code125Option) {
                            codeSelect.value = "125";
                        }
                        console.log('No last code found, defaulting to 125');
                    }
                    
                    // Auto-fill amount field based on selected code
                    if (amountField && codeSelect.value) {
                        const numericCode = codeSelect.value.replace(/\\D/g, '');
                        if (numericCode) {
                            amountField.value = numericCode;
                        }
                    }
                }
            }
        });
    } else {
        console.error('Add Transaction Modal element not found!');
    }

    // Save date and code when form is submitted
    if (addTransactionForm) {
        addTransactionForm.addEventListener('submit', function() {
            // Save the date
            if (dateField && dateField.value) {
                localStorage.setItem('lastTransactionDate', dateField.value);
            } else {
                console.log('Could not save date on submit - field not found or empty');
            }
            
            // Save the code
            if (codeSelect && codeSelect.value) {
                localStorage.setItem('lastTransactionCode', codeSelect.value);
                console.log('Saved last used code:', codeSelect.value);
            } else {
                console.log('Could not save code on submit - field not found or empty');
            }
        });
    } else {
        console.error('Add Transaction Form element not found!');
    }

    // Auto-fill amount field when code is selected
    if (codeSelect) {
        codeSelect.addEventListener('change', function() {
            const selectedCode = codeSelect.value;
            if (selectedCode && amountField) {
                const numericCode = selectedCode.replace(/\\D/g, '');
                if (numericCode) {
                    amountField.value = numericCode;
                }
            }
        });
    } else {
        console.error('Code Select element not found!');
    }
});
"""
