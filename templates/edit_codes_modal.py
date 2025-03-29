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
"""

# JavaScript functions related to the Edit Codes and Classifications modal
EDIT_CODES_SCRIPT = """
document.addEventListener('DOMContentLoaded', function() {
    const editCodesModal = document.getElementById('editCodesModal');
    if (editCodesModal) {
        editCodesModal.addEventListener('show.bs.modal', function() {
            // Load initial data when modal is shown
            loadCodesPage(1);
            loadClassificationsPage(1);
        });
    }
    
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
        fetch(`/api/check_code_usage/${encodeURIComponent(code)}`)
            .then(response => response.json())
            .then(data => {
                if (data.in_use) {
                    // Code is in use, show warning
                    alert(`Cannot delete code "${code}" because it is in use by ${data.count} transaction(s).`);
                } else {
                    // Code is not in use, confirm deletion
                    if (confirm(`Are you sure you want to delete code "${code}"?`)) {
                        // Redirect to delete code route
                        window.location.href = `/delete_code/${encodeURIComponent(code)}`;
                    }
                }
            })
            .catch(error => {
                console.error('Error checking code usage:', error);
                alert('Error checking code usage. Please try again later.');
            });
    }
    
    // Function to check if a classification is in use before deleting
    function checkClassificationUsage(classification) {
        fetch(`/api/check_classification_usage/${encodeURIComponent(classification)}`)
            .then(response => response.json())
            .then(data => {
                if (data.in_use) {
                    // Classification is in use, show warning
                    alert(`Cannot delete classification "${classification}" because it is in use by ${data.count} transaction(s).`);
                } else {
                    // Classification is not in use, confirm deletion
                    if (confirm(`Are you sure you want to delete classification "${classification}"?`)) {
                        // Redirect to delete classification route
                        window.location.href = `/delete_classification/${encodeURIComponent(classification)}`;
                    }
                }
            })
            .catch(error => {
                console.error('Error checking classification usage:', error);
                alert('Error checking classification usage. Please try again later.');
            });
    }
});
"""
