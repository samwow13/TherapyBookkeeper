# -*- coding: utf-8 -*-
"""
Site Settings Modal for the Therapy Bookkeeping Application.
"""

SITE_SETTINGS_MODAL = """
<!-- Site Settings Modal -->
<div class="modal fade" id="siteSettingsModal" tabindex="-1" aria-labelledby="siteSettingsModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="siteSettingsModalLabel">Site Settings</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form id="siteSettingsForm" action="/save-settings" method="post">
                    <div class="mb-3">
                        <h6>Appearance Settings</h6>
                        <div class="form-check form-switch">
                            <!-- Use 'value="on"' to ensure the checkbox passes a value when checked -->
                            <input class="form-check-input" type="checkbox" id="clippy_enabled" name="clippy_enabled" value="on" {% if settings.get('clippy_enabled', True) %}checked{% endif %}>
                            <label class="form-check-label" for="clippy_enabled">Enable Clippy Assistant</label>
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary" id="saveSettingsBtn">Save Changes</button>
            </div>
        </div>
    </div>
</div>
"""

SITE_SETTINGS_SCRIPT = """
document.addEventListener('DOMContentLoaded', function() {
    // Handle Site Settings Form Submission
    const saveSettingsBtn = document.getElementById('saveSettingsBtn');
    if (saveSettingsBtn) {
        saveSettingsBtn.addEventListener('click', function() {
            const form = document.getElementById('siteSettingsForm');
            
            // Create standard URLSearchParams for form submission - this works better with Flask
            const formData = new URLSearchParams();
            const clippyEnabled = document.getElementById('clippy_enabled').checked;
            formData.append('clippy_enabled', clippyEnabled ? 'on' : 'off');
            
            console.log('Sending form data:', clippyEnabled);
            
            // Set up proper headers for form data
            fetch('/save-settings', {
                method: 'POST',
                body: formData,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log('Response from save-settings:', data);
                if (data.success) {
                    // Close modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('siteSettingsModal'));
                    if (modal) {
                        modal.hide();
                        console.log('Modal hidden');
                    } else {
                        console.warn('Modal instance not found');
                    }
                    
                    // Show success message
                    showToast('Settings saved successfully', 'success');
                    console.log('Toast shown, will reload page in 1 second');
                    
                    // Refresh the page to apply settings
                    setTimeout(() => {
                        console.log('Reloading page to apply settings...');
                        window.location.reload();
                    }, 1000);
                } else {
                    console.error('Error response:', data);
                    showToast('Error saving settings', 'danger');
                }
            })
            .catch(error => {
                console.error('Error saving settings:', error);
                showToast('Error saving settings', 'danger');
            });
        });
    }
    
    // Helper function to show toast notifications
    function showToast(message, type) {
        const toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            const container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(container);
        }
        
        const toastId = 'toast-' + Date.now();
        const html = `
            <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header bg-${type} text-white">
                    <strong class="me-auto">Notification</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;
        
        document.getElementById('toastContainer').insertAdjacentHTML('beforeend', html);
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Auto remove toast after it's hidden
        toastElement.addEventListener('hidden.bs.toast', function() {
            toastElement.remove();
        });
    }
});
"""
