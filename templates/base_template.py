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
    <style>
        body { padding-bottom: 40px; background-color: #f8f9fa; }
        .container { max-width: 1100px; position: relative; z-index: 1; }
        .table td, .table th { vertical-align: middle; }
        .credit { color: #198754; font-weight: bold; } /* Bootstrap success green */
        .debit { color: #dc3545; font-weight: bold; } /* Bootstrap danger red */
        .summary-card { margin-bottom: 20px; }
        .summary-value { font-size: 1.5rem; font-weight: bold; }
        .monthly-summary { margin-bottom: 30px; }
        .modal-body .form-label { margin-bottom: 0.3rem; }
        .flash-message { margin-top: 15px; }

        /* Navigation bar styling */
        .navbar {
            background-color: #ffdac1 !important; /* Light peachy color matching monthlySummaryHeader */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        .navbar-brand { display: flex; align-items: center; margin: 0 auto; }
        .navbar-brand img { height: 60px; margin: 0 15px; }
        .navbar-title { font-size: 1.5rem; font-weight: bold; color: #333; margin-bottom: 0; }
        .navbar-container { display: flex; justify-content: center; width: 100%; }

        /* Rainbow colors for dropdown headers */
        #codeSummaryHeader, #monthlySummaryHeader, #allTransactionsHeader { transition: background-color 0.3s ease; }
        #codeSummaryHeader button, #monthlySummaryHeader button, #allTransactionsHeader button { color: #000 !important; font-weight: bold; }
        #codeSummaryHeader { background-color: #ff9aa2 !important; } /* Red-pink */
        #monthlySummaryHeader { background-color: #ffdac1 !important; } /* Light orange */
        #allTransactionsHeader { background-color: #b5ead7 !important; } /* Mint green */

        /* Hover effects */
        #codeSummaryHeader:hover { background-color: #ff7a85 !important; }
        #monthlySummaryHeader:hover { background-color: #ffcaa0 !important; }
        #allTransactionsHeader:hover { background-color: #9ddfc8 !important; }

        /* Accordion headers in monthly summary */
        .accordion-button { transition: background-color 0.3s ease; }
        .accordion-button:not(.collapsed) { background-color: #c7ceea !important; color: #000 !important; }
        .accordion-button:hover { background-color: #c7ceea !important; }

        /* Actions card styling */
        #actionsHeader { background-color: #c7ceea !important; transition: background-color 0.3s ease; }
        #actionsHeader h5 { color: #000 !important; font-weight: bold; }
        #actionsHeader:hover { background-color: #b5b9d4 !important; }

        /* Rainbow buttons in Actions card */
        .btn-edit-codes { background-color: #ff9aa2 !important; border-color: #ff9aa2 !important; color: #000 !important; font-weight: bold; transition: all 0.3s ease; }
        .btn-edit-codes:hover { background-color: #ff7a85 !important; border-color: #ff7a85 !important; }
        .btn-add-transaction { background-color: #b5ead7 !important; border-color: #b5ead7 !important; color: #000 !important; font-weight: bold; transition: all 0.3s ease; }
        .btn-add-transaction:hover { background-color: #9ddfc8 !important; border-color: #9ddfc8 !important; }

        /* Rainbow animation styles */
        .rainbow-container { position: fixed; top: 0; bottom: 0; width: 50px; /* Narrower */ z-index: 0; overflow: hidden; pointer-events: none; }
        .rainbow-left { left: 0; }
        .rainbow-right { right: 0; }
        .rainbow-band { position: absolute; height: 100%; width: 10px; /* Narrower */ opacity: 0.4; /* Subtler */ animation-duration: 15s; animation-timing-function: linear; animation-iteration-count: infinite; }
        .rainbow-left .rainbow-band { animation-name: slideVerticalLeft; }
        .rainbow-right .rainbow-band { animation-name: slideVerticalRight; }

        /* Colors and delays */
        .rainbow-band-1 { background: red; animation-delay: 0s; }
        .rainbow-band-2 { background: orange; animation-delay: -2.1s; } /* Negative delays for staggered start */
        .rainbow-band-3 { background: yellow; animation-delay: -4.2s; }
        .rainbow-band-4 { background: green; animation-delay: -6.3s; }
        .rainbow-band-5 { background: blue; animation-delay: -8.4s; }
        .rainbow-band-6 { background: indigo; animation-delay: -10.5s; }
        .rainbow-band-7 { background: violet; animation-delay: -12.6s; }

        /* Rainbow animation keyframes */
        @keyframes slideVerticalLeft {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
        }
        @keyframes slideVerticalRight {
            0% { transform: translateY(100%); }
            100% { transform: translateY(-100%); }
        }

        /* MODAL CSS FIXES */
        .modal {
            z-index: 1060 !important; /* Modal container */
            overflow-y: auto; /* Ensure modal itself can scroll if content is long */
        }
        .modal-dialog {
             z-index: 1070 !important; /* Dialog needs to be above modal container */
             pointer-events: auto !important; /* Crucial: Ensure clicks go to dialog */
        }
        .modal-content {
            pointer-events: auto !important; /* Ensure clicks go to content */
        }

        /* Modal transition fixes */
        .modal.fade .modal-dialog {
            transition: transform 0.3s ease-out;
            transform: translate(0, -50px);
        }
        .modal.show .modal-dialog {
            transform: none;
        }
        body.modal-open {
             overflow: hidden; /* Prevent body scrolling */
             /* Remove Bootstrap's default padding-right adjustment if it causes issues */
             padding-right: 0 !important;
        }
        /* END MODAL CSS FIXES */

        /* Custom styling for the application */
        .account-summary-card {
            transition: all 0.3s;
        }
        
        .account-summary-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }
        
        .btn-add-transaction, .btn-edit-codes {
            padding: 10px 15px;
            border-radius: 50px;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .btn-add-transaction {
            background-color: #007bff;
            color: white;
            border: none;
        }
        
        .btn-edit-codes {
            background-color: #6c757d;
            color: white;
            border: none;
        }
        
        .btn-add-transaction:hover, .btn-edit-codes:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .modal-content {
            pointer-events: auto !important;
        }
        
        .modal-backdrop {
            opacity: 0.5 !important; 
            z-index: 1040 !important;
        }
        
        .modal {
            z-index: 1050 !important;
        }
        
        /* Ensure form elements are interactive */
        .modal-body .form-control,
        .modal-body .form-select,
        .modal-footer .btn {
            position: relative;
            z-index: 1051 !important;
            pointer-events: auto !important;
        }
        
        /* Fix for modal backdrop issue */
        body.modal-open {
            overflow: auto !important;
            padding-right: 0 !important;
        }
    </style>
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

    <!-- Footer -->
    <footer class="footer mt-auto py-3 bg-light">
        <div class="container">
            <span class="text-muted">Therapy Bookkeeping Application &copy; 2023</span>
        </div>
    </footer>

    <!-- Bootstrap JS Bundle (includes Popper) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- Modal Templates -->
    {{ modals_content|safe }}

    <!-- Custom styles to fix modal issues -->
    <style>
        /* Ensure modals are displayed on top of other elements */
        .modal {
            z-index: 1050 !important;
        }
        
        /* Fix modal backdrop */
        .modal-backdrop {
            z-index: 1040 !important;
        }
        
        /* Ensure input fields are clickable */
        .modal-content input,
        .modal-content select,
        .modal-content button {
            z-index: 1060 !important;
            position: relative;
        }
    </style>
    
    <!-- Modal-specific JavaScript -->
    <script>
        // Ensure the modal works correctly
        document.addEventListener('DOMContentLoaded', function() {
            // Remove any existing backdrops
            document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
            
            // Reset body classes that might be stuck
            document.body.classList.remove('modal-open');
            document.body.style.removeProperty('overflow');
            document.body.style.removeProperty('padding-right');
            
            // Direct fix: Override Bootstrap's modal backdrop click handling
            const fixModal = function() {
                // Remove any stale backdrops
                document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
                
                // Get buttons that open the add transaction modal
                const buttons = document.querySelectorAll('[data-bs-target="#addTransactionModal"]');
                
                buttons.forEach(button => {
                    button.addEventListener('click', function(e) {
                        // Prevent the default Bootstrap modal behavior
                        e.preventDefault();
                        e.stopPropagation();
                        
                        // Get the modal element
                        const modalEl = document.querySelector('#addTransactionModal');
                        
                        // Manually show the modal
                        if (modalEl) {
                            // Create a fresh backdrop
                            const backdropEl = document.createElement('div');
                            backdropEl.className = 'modal-backdrop fade show';
                            backdropEl.style.zIndex = '1040';
                            document.body.appendChild(backdropEl);
                            
                            // Show the modal
                            modalEl.style.display = 'block';
                            modalEl.classList.add('show');
                            modalEl.setAttribute('aria-modal', 'true');
                            modalEl.removeAttribute('aria-hidden');
                            
                            // Make sure the modal is on top and interactive
                            modalEl.style.zIndex = '1050';
                            
                            // Ensure inputs are clickable
                            modalEl.querySelectorAll('input, select, button').forEach(el => {
                                el.style.zIndex = '1060';
                                el.style.position = 'relative';
                                el.style.pointerEvents = 'auto';
                            });
                            
                            // Add listener for close button
                            modalEl.querySelectorAll('[data-bs-dismiss="modal"]').forEach(closeBtn => {
                                closeBtn.addEventListener('click', function() {
                                    modalEl.style.display = 'none';
                                    modalEl.classList.remove('show');
                                    modalEl.setAttribute('aria-hidden', 'true');
                                    modalEl.removeAttribute('aria-modal');
                                    
                                    // Remove the backdrop
                                    document.querySelectorAll('.modal-backdrop').forEach(bd => bd.remove());
                                });
                            });
                            
                            // Set form values
                            const dateField = modalEl.querySelector('#date');
                            if (dateField) {
                                const lastDate = localStorage.getItem('lastTransactionDate');
                                if (lastDate) {
                                    dateField.value = lastDate;
                                } else {
                                    const today = new Date().toISOString().split('T')[0];
                                    dateField.value = today;
                                }
                            }
                        }
                    });
                });
            };
            
            // Run the fix immediately and also after a short delay (for dynamic content)
            fixModal();
            setTimeout(fixModal, 500);
        });
        
        {{ add_transaction_script|safe }}
        {{ edit_transaction_script|safe }}
        {{ delete_transaction_script|safe }}
        
        // Additional global scripts
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Therapy Bookkeeping App initialized');
        });
    </script>
    
    <!-- Page-specific JavaScript -->
    {% block scripts %}{% endblock %}
</body>
</html>
"""
