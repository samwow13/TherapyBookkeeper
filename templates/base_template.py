# -*- coding: utf-8 -*-
"""
Base Template for the Therapy Bookkeeping Application.
"""

BASE_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Therapy Bookkeeping | {{ title }}</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <!-- Global CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/global.css') }}">
</head>
<body>
    <!-- Rainbow containers -->
    <div class="rainbow-container rainbow-left">
        <div class="rainbow-band rainbow-band-1"></div> <div class="rainbow-band rainbow-band-2"></div> <div class="rainbow-band rainbow-band-3"></div>
        <div class="rainbow-band rainbow-band-4"></div> <div class="rainbow-band rainbow-band-5"></div> <div class="rainbow-band rainbow-band-6"></div>
        <div class="rainbow-band rainbow-band-7"></div>
    </div>
    <div class="rainbow-container rainbow-right">
         <div class="rainbow-band rainbow-band-1"></div> <div class="rainbow-band rainbow-band-2"></div> <div class="rainbow-band rainbow-band-3"></div>
        <div class="rainbow-band rainbow-band-4"></div> <div class="rainbow-band rainbow-band-5"></div> <div class="rainbow-band rainbow-band-6"></div>
        <div class="rainbow-band rainbow-band-7"></div>
    </div>

    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg">
        <div class="container">
            <div class="navbar-container">
                <a class="navbar-brand" href="{{ url_for('index') }}">
                    <img src="{{ url_for('static', filename='images/logo.png') }}" alt="Therapy Logo">
                    <h1 class="navbar-title">Angela's Therapy Bookkeeping System</h1>
                    <img src="{{ url_for('static', filename='images/logo.png') }}" alt="Therapy Logo">
                </a>
            </div>
        </div>
    </nav>

    <div class="container">
        <!-- Flash Messages -->
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="alert alert-{{ category if category != 'message' else 'info' }} alert-dismissible fade show flash-message" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>

    <!-- Modal Templates -->
    {{ modals_content|safe }}

    <!-- Footer -->
    <footer class="footer mt-auto py-3 bg-light">
        <div class="container">
            <span class="text-muted">Therapy Bookkeeping Application &copy; 2023</span>
        </div>
    </footer>

    <!-- Bootstrap JS Bundle (includes Popper) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- Modal Scripts -->
    <script>
        {{ add_transaction_script|safe }}
    </script>
    <script>
        {{ edit_transaction_script|safe }}
    </script>
    <script>
        {{ delete_transaction_script|safe }}
    </script>
    <script>
        {{ print_modals_script|safe }}
    </script>

    <!-- Global Script -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Fix for any modal issues
            const fixModals = function() {
                // Remove any stale backdrops
                document.querySelectorAll('.modal-backdrop').forEach(function(backdrop) {
                    backdrop.remove();
                });
                
                // Reset body classes
                document.body.classList.remove('modal-open');
                document.body.style.removeProperty('overflow');
                document.body.style.removeProperty('padding-right');
                
                // Make sure all modals have proper event handling
                document.querySelectorAll('.modal').forEach(function(modalEl) {
                    // Ensure modal is properly initialized with Bootstrap
                    if (!bootstrap.Modal.getInstance(modalEl)) {
                        new bootstrap.Modal(modalEl);
                    }
                    
                    modalEl.addEventListener('hidden.bs.modal', function() {
                        // Clean up after modal is closed
                        document.querySelectorAll('.modal-backdrop').forEach(function(backdrop) {
                            backdrop.remove();
                        });
                        document.body.classList.remove('modal-open');
                        document.body.style.removeProperty('overflow');
                        document.body.style.removeProperty('padding-right');
                    });
                });
                
                // Fix any buttons that trigger modals
                document.querySelectorAll('[data-bs-toggle="modal"]').forEach(function(button) {
                    button.addEventListener('click', function(e) {
                        e.preventDefault(); // Prevent default action
                        
                        // Get the target modal ID
                        const targetModalId = this.getAttribute('data-bs-target');
                        if (!targetModalId) return;
                        
                        // Find the modal element
                        const modalEl = document.querySelector(targetModalId);
                        if (!modalEl) return;
                        
                        // Remove any existing backdrop
                        document.querySelectorAll('.modal-backdrop').forEach(function(backdrop) {
                            backdrop.remove();
                        });
                        
                        // Ensure modal is properly initialized with Bootstrap
                        const modalInstance = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
                        
                        // Show the modal
                        modalInstance.show();
                    });
                });
            };
            
            // Run the fix immediately and after a short delay (for dynamic content)
            fixModals();
            setTimeout(fixModals, 500);
            
            // Initialize tooltips and popovers if any
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function(tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        });
    </script>
    
    <!-- Page-specific JavaScript -->
    {% block scripts %}{% endblock %}
</body>
</html>
"""
