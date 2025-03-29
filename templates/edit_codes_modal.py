# -*- coding: utf-8 -*-
"""
Edit Codes and Classifications Modal Template for the Therapy Bookkeeping Application.
This file contains the HTML template for managing transaction codes and classifications.
"""

EDIT_CODES_MODAL = """
<!-- Edit Codes and Classifications Modal -->
<div class="modal fade" id="editCodesModal" tabindex="-1" aria-labelledby="editCodesModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="editCodesModalLabel">Manage Codes and Classifications</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <ul class="nav nav-tabs" id="codesClassificationsTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="codes-tab" data-bs-toggle="tab" data-bs-target="#codes-content" 
                                type="button" role="tab" aria-controls="codes-content" aria-selected="true">
                            Codes
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="classifications-tab" data-bs-toggle="tab" data-bs-target="#classifications-content" 
                                type="button" role="tab" aria-controls="classifications-content" aria-selected="false">
                            Classifications
                        </button>
                    </li>
                </ul>
                
                <div class="tab-content" id="codesClassificationsContent">
                    <!-- Codes Tab -->
                    <div class="tab-pane fade show active" id="codes-content" role="tabpanel" aria-labelledby="codes-tab">
                        <div class="row mt-3">
                            <div class="col-md-6">
                                <form action="/add_code" method="post" id="addCodeForm" class="mb-4">
                                    <div class="d-flex">
                                        <input type="text" class="form-control me-2" id="code" name="code" placeholder="New Code" required>
                                        <button type="submit" class="btn btn-primary">Add Code</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                        <div class="codes-list mt-2">
                            <div class="list-group" id="codesList">
                                <div class="d-flex justify-content-center">
                                    <div class="spinner-border text-primary" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>
                                </div>
                            </div>
                            <nav aria-label="Codes pagination" class="mt-3">
                                <ul class="pagination justify-content-center" id="codesPagination"></ul>
                            </nav>
                        </div>
                    </div>
                    
                    <!-- Classifications Tab -->
                    <div class="tab-pane fade" id="classifications-content" role="tabpanel" aria-labelledby="classifications-tab">
                        <div class="row mt-3">
                            <div class="col-md-6">
                                <form action="/add_classification" method="post" id="addClassificationForm" class="mb-4">
                                    <div class="d-flex">
                                        <input type="text" class="form-control me-2" id="classification" name="classification" placeholder="New Classification" required>
                                        <button type="submit" class="btn btn-primary">Add Classification</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                        <div class="classifications-list mt-2">
                            <div class="list-group" id="classificationsList">
                                <div class="d-flex justify-content-center">
                                    <div class="spinner-border text-primary" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>
                                </div>
                            </div>
                            <nav aria-label="Classifications pagination" class="mt-3">
                                <ul class="pagination justify-content-center" id="classificationsPagination"></ul>
                            </nav>
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

<!-- Delete Code Confirmation Modal -->
<div class="modal fade" id="deleteCodeModal" tabindex="-1" aria-labelledby="deleteCodeModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="deleteCodeModalLabel">Confirm Deletion</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <p>Are you sure you want to delete this code?</p>
                <input type="hidden" id="codeToDelete">
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-danger" id="confirmDeleteCode">Delete</button>
            </div>
        </div>
    </div>
</div>

<!-- Delete Classification Confirmation Modal -->
<div class="modal fade" id="deleteClassificationModal" tabindex="-1" aria-labelledby="deleteClassificationModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="deleteClassificationModalLabel">Confirm Deletion</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <p>Are you sure you want to delete this classification?</p>
                <input type="hidden" id="classificationToDelete">
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-danger" id="confirmDeleteClassification">Delete</button>
            </div>
        </div>
    </div>
</div>

<!-- Code Usage Warning Modal -->
<div class="modal fade" id="codeUsageWarningModal" tabindex="-1" aria-labelledby="codeUsageWarningModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="codeUsageWarningModalLabel">Cannot Delete Code</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <div class="alert alert-warning">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    <span id="codeUsageWarningText"></span>
                </div>
                <p>Please update or delete these transactions first before deleting this code.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Understood</button>
            </div>
        </div>
    </div>
</div>

<!-- Classification Usage Warning Modal -->
<div class="modal fade" id="classificationUsageWarningModal" tabindex="-1" aria-labelledby="classificationUsageWarningModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="classificationUsageWarningModalLabel">Cannot Delete Classification</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <div class="alert alert-warning">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    <span id="classificationUsageWarningText"></span>
                </div>
                <p>Please update or delete these transactions first before deleting this classification.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Understood</button>
            </div>
        </div>
    </div>
</div>

"""

# JavaScript functions related to the Edit Codes and Classifications modal
EDIT_CODES_SCRIPT = """
document.addEventListener('DOMContentLoaded', function() {
    // Initialize modals
    const editCodesModal = document.getElementById('editCodesModal');
    const deleteCodeModal = document.getElementById('deleteCodeModal');
    const deleteClassificationModal = document.getElementById('deleteClassificationModal');
    const codeUsageWarningModal = document.getElementById('codeUsageWarningModal');
    const classificationUsageWarningModal = document.getElementById('classificationUsageWarningModal');
    
    // Convert to Bootstrap modal objects
    const editCodesModalObj = new bootstrap.Modal(editCodesModal);
    const deleteCodeModalObj = new bootstrap.Modal(deleteCodeModal, {
        backdrop: 'static'  // Prevent clicks outside modal from closing it
    });
    const deleteClassificationModalObj = new bootstrap.Modal(deleteClassificationModal, {
        backdrop: 'static'  // Prevent clicks outside modal from closing it
    });
    const codeUsageWarningModalObj = new bootstrap.Modal(codeUsageWarningModal, {
        backdrop: 'static'  // Prevent clicks outside modal from closing it
    });
    const classificationUsageWarningModalObj = new bootstrap.Modal(classificationUsageWarningModal, {
        backdrop: 'static'  // Prevent clicks outside modal from closing it
    });
    
    // Handle initial data loading
    editCodesModal.addEventListener('show.bs.modal', function() {
        loadCodesPage(1);
        loadClassificationsPage(1);
    });
    
    // Modal event listeners - handle backdrop stacking for nested modals
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            // When opening a new modal, check if there's already an open modal
            const openModals = document.querySelectorAll('.modal.show');
            if (openModals.length > 0) {
                // Add additional z-index to handle stacking properly
                const backdropZ = parseInt(window.getComputedStyle(document.querySelector('.modal-backdrop')).zIndex, 10);
                document.querySelector('.modal-backdrop:last-child').style.zIndex = backdropZ + 2;
                this.style.zIndex = backdropZ + 10;
            }
        });
        
        modal.addEventListener('hidden.bs.modal', function() {
            // Remove modal-open class and any lingering backdrops
            const openModals = document.querySelectorAll('.modal.show');
            if (openModals.length === 0) {
                document.body.classList.remove('modal-open');
                document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
                    backdrop.remove();
                });
            } else {
                // If there are still modals open, make sure body remains modal-open
                document.body.classList.add('modal-open');
            }
        });
    });
    
    // Function to load codes with pagination
    function loadCodesPage(page) {
        fetch(`/api/codes/page/${page}`)
            .then(response => response.json())
            .then(data => {
                const codesList = document.getElementById('codesList');
                const codesPagination = document.getElementById('codesPagination');
                
                // Clear existing content
                codesList.innerHTML = '';
                codesPagination.innerHTML = '';
                
                // Handle empty codes list
                if (data.codes.length === 0) {
                    codesList.innerHTML = '<div class="alert alert-info">No codes available. Add your first code above.</div>';
                    return;
                }
                
                // Add codes to the list
                data.codes.forEach(code => {
                    const codeItem = document.createElement('div');
                    codeItem.className = 'list-group-item list-group-item-action d-flex justify-content-between align-items-center';
                    
                    // Create code text
                    const codeText = document.createElement('span');
                    codeText.textContent = code;
                    codeItem.appendChild(codeText);
                    
                    // Create delete button
                    const deleteBtn = document.createElement('button');
                    deleteBtn.className = 'btn btn-sm btn-outline-danger delete-code-btn';
                    deleteBtn.innerHTML = '<i class="bi bi-trash"></i>';
                    deleteBtn.setAttribute('data-code', code);
                    deleteBtn.addEventListener('click', function() {
                        checkCodeUsage(code);
                    });
                    codeItem.appendChild(deleteBtn);
                    
                    codesList.appendChild(codeItem);
                });
                
                // Add pagination
                if (data.pagination.total_pages > 1) {
                    // Previous button
                    const prevLi = document.createElement('li');
                    prevLi.className = `page-item ${data.pagination.page === 1 ? 'disabled' : ''}`;
                    const prevLink = document.createElement('a');
                    prevLink.className = 'page-link';
                    prevLink.href = '#';
                    prevLink.textContent = 'Previous';
                    if (data.pagination.page > 1) {
                        prevLink.addEventListener('click', function(e) {
                            e.preventDefault();
                            loadCodesPage(data.pagination.page - 1);
                        });
                    }
                    prevLi.appendChild(prevLink);
                    codesPagination.appendChild(prevLi);
                    
                    // Page buttons
                    for (let i = 1; i <= data.pagination.total_pages; i++) {
                        const pageLi = document.createElement('li');
                        pageLi.className = `page-item ${i === data.pagination.page ? 'active' : ''}`;
                        const pageLink = document.createElement('a');
                        pageLink.className = 'page-link';
                        pageLink.href = '#';
                        pageLink.textContent = i;
                        pageLink.addEventListener('click', function(e) {
                            e.preventDefault();
                            loadCodesPage(i);
                        });
                        pageLi.appendChild(pageLink);
                        codesPagination.appendChild(pageLi);
                    }
                    
                    // Next button
                    const nextLi = document.createElement('li');
                    nextLi.className = `page-item ${data.pagination.page === data.pagination.total_pages ? 'disabled' : ''}`;
                    const nextLink = document.createElement('a');
                    nextLink.className = 'page-link';
                    nextLink.href = '#';
                    nextLink.textContent = 'Next';
                    if (data.pagination.page < data.pagination.total_pages) {
                        nextLink.addEventListener('click', function(e) {
                            e.preventDefault();
                            loadCodesPage(data.pagination.page + 1);
                        });
                    }
                    nextLi.appendChild(nextLink);
                    codesPagination.appendChild(nextLi);
                }
            })
            .catch(error => {
                console.error('Error loading codes:', error);
                document.getElementById('codesList').innerHTML = '<div class="alert alert-danger">Error loading codes. Please try again later.</div>';
            });
    }
    
    // Function to load classifications with pagination
    function loadClassificationsPage(page) {
        fetch(`/api/classifications/page/${page}`)
            .then(response => response.json())
            .then(data => {
                const classificationsList = document.getElementById('classificationsList');
                const classificationsPagination = document.getElementById('classificationsPagination');
                
                // Clear existing content
                classificationsList.innerHTML = '';
                classificationsPagination.innerHTML = '';
                
                // Handle empty classifications list
                if (data.classifications.length === 0) {
                    classificationsList.innerHTML = '<div class="alert alert-info">No classifications available. Add your first classification above.</div>';
                    return;
                }
                
                // Add classifications to the list
                data.classifications.forEach(classification => {
                    const classificationItem = document.createElement('div');
                    classificationItem.className = 'list-group-item list-group-item-action d-flex justify-content-between align-items-center';
                    
                    // Create classification text
                    const classificationText = document.createElement('span');
                    classificationText.textContent = classification;
                    classificationItem.appendChild(classificationText);
                    
                    // Create delete button
                    const deleteBtn = document.createElement('button');
                    deleteBtn.className = 'btn btn-sm btn-outline-danger delete-classification-btn';
                    deleteBtn.innerHTML = '<i class="bi bi-trash"></i>';
                    deleteBtn.setAttribute('data-classification', classification);
                    deleteBtn.addEventListener('click', function() {
                        checkClassificationUsage(classification);
                    });
                    classificationItem.appendChild(deleteBtn);
                    
                    classificationsList.appendChild(classificationItem);
                });
                
                // Add pagination
                if (data.pagination.total_pages > 1) {
                    // Previous button
                    const prevLi = document.createElement('li');
                    prevLi.className = `page-item ${data.pagination.page === 1 ? 'disabled' : ''}`;
                    const prevLink = document.createElement('a');
                    prevLink.className = 'page-link';
                    prevLink.href = '#';
                    prevLink.textContent = 'Previous';
                    if (data.pagination.page > 1) {
                        prevLink.addEventListener('click', function(e) {
                            e.preventDefault();
                            loadClassificationsPage(data.pagination.page - 1);
                        });
                    }
                    prevLi.appendChild(prevLink);
                    classificationsPagination.appendChild(prevLi);
                    
                    // Page buttons
                    for (let i = 1; i <= data.pagination.total_pages; i++) {
                        const pageLi = document.createElement('li');
                        pageLi.className = `page-item ${i === data.pagination.page ? 'active' : ''}`;
                        const pageLink = document.createElement('a');
                        pageLink.className = 'page-link';
                        pageLink.href = '#';
                        pageLink.textContent = i;
                        pageLink.addEventListener('click', function(e) {
                            e.preventDefault();
                            loadClassificationsPage(i);
                        });
                        pageLi.appendChild(pageLink);
                        classificationsPagination.appendChild(pageLi);
                    }
                    
                    // Next button
                    const nextLi = document.createElement('li');
                    nextLi.className = `page-item ${data.pagination.page === data.pagination.total_pages ? 'disabled' : ''}`;
                    const nextLink = document.createElement('a');
                    nextLink.className = 'page-link';
                    nextLink.href = '#';
                    nextLink.textContent = 'Next';
                    if (data.pagination.page < data.pagination.total_pages) {
                        nextLink.addEventListener('click', function(e) {
                            e.preventDefault();
                            loadClassificationsPage(data.pagination.page + 1);
                        });
                    }
                    nextLi.appendChild(nextLink);
                    classificationsPagination.appendChild(nextLi);
                }
            })
            .catch(error => {
                console.error('Error loading classifications:', error);
                document.getElementById('classificationsList').innerHTML = '<div class="alert alert-danger">Error loading classifications. Please try again later.</div>';
            });
    }
    
    // Function to check if a code is in use before deleting
    function checkCodeUsage(code) {
        // Hide the edit codes modal first before showing the new modal
        editCodesModalObj.hide();
        
        fetch(`/api/check_code_usage/${encodeURIComponent(code)}`)
            .then(response => response.json())
            .then(data => {
                if (data.in_use) {
                    // Code is in use, show warning modal
                    document.getElementById('codeUsageWarningText').textContent = 
                        `Cannot delete code "${code}" because it is in use by ${data.count} transaction(s).`;
                    codeUsageWarningModalObj.show();
                } else {
                    // Code is not in use, show confirmation modal
                    document.getElementById('deleteCodeModalLabel').textContent = `Delete Code: ${code}`;
                    document.getElementById('codeToDelete').value = code;
                    deleteCodeModalObj.show();
                }
            })
            .catch(error => {
                console.error('Error checking code usage:', error);
                showToast('Error', 'Error checking code usage. Please try again later.', 'danger');
                // Show the edit codes modal again if there's an error
                editCodesModalObj.show();
            });
    }
    
    // Function to check if a classification is in use before deleting
    function checkClassificationUsage(classification) {
        // Hide the edit codes modal first before showing the new modal
        editCodesModalObj.hide();
        
        fetch(`/api/check_classification_usage/${encodeURIComponent(classification)}`)
            .then(response => response.json())
            .then(data => {
                if (data.in_use) {
                    // Classification is in use, show warning modal
                    document.getElementById('classificationUsageWarningText').textContent = 
                        `Cannot delete classification "${classification}" because it is in use by ${data.count} transaction(s).`;
                    classificationUsageWarningModalObj.show();
                } else {
                    // Classification is not in use, show confirmation modal
                    document.getElementById('deleteClassificationModalLabel').textContent = `Delete Classification: ${classification}`;
                    document.getElementById('classificationToDelete').value = classification;
                    deleteClassificationModalObj.show();
                }
            })
            .catch(error => {
                console.error('Error checking classification usage:', error);
                showToast('Error', 'Error checking classification usage. Please try again later.', 'danger');
                // Show the edit codes modal again if there's an error
                editCodesModalObj.show();
            });
    }
    
    // Set up event listeners for delete confirmations
    document.getElementById('confirmDeleteCode').addEventListener('click', function() {
        const codeToDelete = document.getElementById('codeToDelete').value;
        
        // Send delete request
        fetch(`/api/delete_code/${encodeURIComponent(codeToDelete)}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            // Hide the delete confirmation modal
            deleteCodeModalObj.hide();
            
            if (data.success) {
                // Show success message
                showToast('Success', `Code "${codeToDelete}" has been deleted.`, 'success');
                // Show the edit codes modal again after successful deletion
                editCodesModalObj.show();
                // Reload the codes list
                loadCodesPage(1);
            } else {
                // Show error message
                showToast('Error', data.message || 'Failed to delete code.', 'danger');
                // Show the edit codes modal again
                editCodesModalObj.show();
            }
        })
        .catch(error => {
            console.error('Error deleting code:', error);
            deleteCodeModalObj.hide();
            showToast('Error', 'Error deleting code. Please try again later.', 'danger');
            // Show the edit codes modal again
            editCodesModalObj.show();
        });
    });
    
    document.getElementById('confirmDeleteClassification').addEventListener('click', function() {
        const classificationToDelete = document.getElementById('classificationToDelete').value;
        
        // Send delete request
        fetch(`/api/delete_classification/${encodeURIComponent(classificationToDelete)}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            // Hide the delete confirmation modal
            deleteClassificationModalObj.hide();
            
            if (data.success) {
                // Show success message
                showToast('Success', `Classification "${classificationToDelete}" has been deleted.`, 'success');
                // Show the edit codes modal again after successful deletion
                editCodesModalObj.show();
                // Reload the classifications list
                loadClassificationsPage(1);
            } else {
                // Show error message
                showToast('Error', data.message || 'Failed to delete classification.', 'danger');
                // Show the edit codes modal again
                editCodesModalObj.show();
            }
        })
        .catch(error => {
            console.error('Error deleting classification:', error);
            deleteClassificationModalObj.hide();
            showToast('Error', 'Error deleting classification. Please try again later.', 'danger');
            // Show the edit codes modal again
            editCodesModalObj.show();
        });
    });
    
    // Additional event handlers for usage warning and confirmation modals
    codeUsageWarningModal.addEventListener('hidden.bs.modal', function() {
        // Re-open edit codes modal after closing the warning
        editCodesModalObj.show();
    });
    
    classificationUsageWarningModal.addEventListener('hidden.bs.modal', function() {
        // Re-open edit codes modal after closing the warning
        editCodesModalObj.show();
    });
    
    // If user cancels deletion, re-open the edit codes modal
    document.querySelectorAll('.modal .btn-secondary[data-bs-dismiss="modal"]').forEach(btn => {
        btn.addEventListener('click', function() {
            setTimeout(() => {
                // Give time for the current modal to close before showing the edit codes modal
                if (!document.querySelector('.modal.show')) {
                    editCodesModalObj.show();
                }
            }, 300);
        });
    });
    
    // Helper function to show Bootstrap toasts
    function showToast(title, message, type = 'primary') {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            // Create toast container if it doesn't exist
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(container);
        }
        
        const toastId = 'toast-' + Date.now();
        const toastHTML = `
            <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header bg-${type} text-white">
                    <strong class="me-auto">${title}</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;
        
        document.getElementById('toast-container').insertAdjacentHTML('beforeend', toastHTML);
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, { autohide: true, delay: 5000 });
        toast.show();
        
        // Remove the toast from DOM after it's hidden
        toastElement.addEventListener('hidden.bs.toast', function () {
            toastElement.remove();
        });
    }
});

"""
