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
        <div class="rainbow-band rainbow-band-8"></div> <div class="rainbow-band rainbow-band-9"></div> <div class="rainbow-band rainbow-band-10"></div>
        <div class="rainbow-band rainbow-band-11"></div> <div class="rainbow-band rainbow-band-12"></div> <div class="rainbow-band rainbow-band-13"></div>
        <div class="rainbow-band rainbow-band-14"></div> <div class="rainbow-band rainbow-band-15"></div>
    </div>
    <div class="rainbow-container rainbow-right">
        <div class="rainbow-band rainbow-band-1"></div> <div class="rainbow-band rainbow-band-2"></div> <div class="rainbow-band rainbow-band-3"></div> <div class="rainbow-band rainbow-band-4"></div> <div class="rainbow-band rainbow-band-5"></div> <div class="rainbow-band rainbow-band-6"></div> <div class="rainbow-band rainbow-band-7"></div>
        <div class="rainbow-band rainbow-band-8"></div> <div class="rainbow-band rainbow-band-9"></div> <div class="rainbow-band rainbow-band-10"></div> <div class="rainbow-band rainbow-band-11"></div> <div class="rainbow-band rainbow-band-12"></div> <div class="rainbow-band rainbow-band-13"></div> <div class="rainbow-band rainbow-band-14"></div> <div class="rainbow-band rainbow-band-15"></div>
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

    <!-- Footer with decreased importance in the stacking context -->
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
    <script>
        {{ edit_codes_script|safe }}
    </script>
    <script>
        {{ shutdown_script_template|safe }}
    </script>

    <!-- Minimal Modal Cleanup Script -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            document.body.addEventListener('hidden.bs.modal', function (event) {
                if (!document.querySelector('.modal.show')) {
                    document.body.classList.remove('modal-open');
                    const backdrops = document.querySelectorAll('.modal-backdrop');
                    backdrops.forEach(backdrop => {
                        backdrop.remove();
                    });
                    document.body.style.overflow = '';
                    document.body.style.paddingRight = '';
                }
            }, true);
        });
    </script>
    
    <!-- Page-specific JavaScript -->
    {% block scripts %}{% endblock %}

</body>
</html>
"""
