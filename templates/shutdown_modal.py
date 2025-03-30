# -*- coding: utf-8 -*-
"""
Modal and script for confirming application shutdown.
"""

SHUTDOWN_MODAL = """
<!-- Shutdown Confirmation Modal -->
<div class="modal fade" id="shutdownConfirmModal" tabindex="-1" aria-labelledby="shutdownConfirmModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="shutdownConfirmModalLabel">Confirm Shutdown</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <p>Are you sure you want to shut down the application server?</p>
                <p>This will stop the background process. You will need to run the application again to restart it.</p>
                <p id="shutdown-message" class="text-info"></p> 
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-danger" id="confirmShutdownBtn">Confirm Shutdown</button>
            </div>
        </div>
    </div>
</div>
"""

SHUTDOWN_SCRIPT = """
document.addEventListener('DOMContentLoaded', function() {
    const confirmBtn = document.getElementById('confirmShutdownBtn');
    const shutdownModalElement = document.getElementById('shutdownConfirmModal');
    const shutdownMessage = document.getElementById('shutdown-message');

    if (confirmBtn && shutdownModalElement) {
        console.log('Shutdown modal elements found and listener being attached.'); // DEBUG
        const shutdownModal = new bootstrap.Modal(shutdownModalElement);

        confirmBtn.addEventListener('click', function() {
            console.log('Confirm Shutdown button clicked.'); // DEBUG
            // Disable button to prevent multiple clicks
            confirmBtn.disabled = true;
            shutdownMessage.textContent = 'Sending shutdown signal...';

            console.log('Sending fetch request to /shutdown...'); // DEBUG
            fetch('/shutdown', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Add any other headers if needed, e.g., CSRF token
                },
                body: JSON.stringify({}) // Send empty body or specific data if needed
            })
            .then(response => {
                console.log('Received response from /shutdown:', response.status, response.statusText); // DEBUG
                return response.json();
            })
            .then(data => {
                console.log('Parsed shutdown response data:', data); // DEBUG
                if (data.success) {
                    shutdownMessage.textContent = 'Shutdown signal sent successfully. You can close this window now.';
                    console.log('Shutdown successful:', data.message);
                    // Optionally try to close the window (may be blocked by browser)
                    // Adding a small delay before closing
                    setTimeout(function() {
                         window.close();
                         // shutdownMessage.textContent += ' Please close this browser tab manually.'; // Commented out for now
                     }, 1500); // Delay 1.5 seconds
                } else {
                    shutdownMessage.textContent = 'Failed to send shutdown signal: ' + (data.message || 'Unknown error');
                    console.error('Shutdown failed:', data.message);
                    confirmBtn.disabled = false; // Re-enable button on failure
                }
            })
            .catch(error => {
                shutdownMessage.textContent = 'Error sending shutdown signal: ' + error;
                console.error('!!! Error during shutdown fetch:', error); // DEBUG: Added emphasis
                confirmBtn.disabled = false; // Re-enable button on error
            });
        });

        // Reset message when modal is hidden
        shutdownModalElement.addEventListener('hidden.bs.modal', function () {
             shutdownMessage.textContent = '';
             confirmBtn.disabled = false;
        });
    } else {
        console.error('!!! Could not find shutdown modal elements.'); // DEBUG: Added emphasis
    }
});
"""
