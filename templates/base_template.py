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
    <title>Therapist Bookkeeping</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
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

        @keyframes slideVerticalLeft {
            0% { transform: translateY(-100%); } /* Start above */
            100% { transform: translateY(100%); } /* End below */
        }
        @keyframes slideVerticalRight {
            0% { transform: translateY(100%); } /* Start below */
            100% { transform: translateY(-100%); } /* End above */
        }


        /* MODAL CSS FIXES */
        .modal-backdrop {
            z-index: 1050 !important; /* Backdrop behind modal */
        }
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

    <!-- Bootstrap JS Bundle (includes Popper) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
    {% block scripts %}{% endblock %} {# Placeholder for page-specific scripts #}
</body>
</html>
"""
