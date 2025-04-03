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
    <title>Angela's Therapy Bookkeeping | {{ title }}</title>
    <!-- Favicon - Clippy icon for browser tab -->
    <link rel="icon" type="image/png" href="{{ url_for('static', filename='images/logo.png') }}">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <!-- Global CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/global.css') }}">
    <style>
        /* Clippy Animation Styles */
        .clippy-container {
            position: fixed;
            right: 220px;
            top: 50%;
            transform: translateY(-50%);
            width: 300px;
            height: 200px;
            z-index: 1000;
            pointer-events: none; /* Allow interaction with elements behind clippy */
        }
        .clippy-image {
            position: absolute;
            top: 10px;
            right: 0;
            width: 80px;
            height: auto;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .clippy-textbox {
            position: absolute;
            top: -140px;
            right: -30px;
            width: 200px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .clippy-visible {
            opacity: 1;
        }
    </style>
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
    
    <!-- Clippy Animation Container - Now positioned on the right side of the page -->
    {% if settings.get('clippy_enabled', True) %}
    <div class="clippy-container">
        <img id="clippy-1" class="clippy-image" src="{{ url_for('static', filename='images/ClippyImages/clippy_1.png') }}" alt="Clippy">
        <img id="clippy-2" class="clippy-image" src="{{ url_for('static', filename='images/ClippyImages/clippy_2.png') }}" alt="Clippy">
        <img id="clippy-3" class="clippy-image" src="{{ url_for('static', filename='images/ClippyImages/clippy_3.png') }}" alt="Clippy">
        <img id="clippy-textbox" class="clippy-textbox" src="{{ url_for('static', filename='images/ClippyImages/clippy_textbox.png') }}" alt="Clippy Textbox">
    </div>
    {% endif %}

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
    
    <!-- Clippy Animation Script - Now in a loop every 5 seconds -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Check if Clippy is enabled by seeing if the elements exist
            const clippy1 = document.getElementById('clippy-1');
            const clippy2 = document.getElementById('clippy-2');
            const clippy3 = document.getElementById('clippy-3');
            const clippyTextbox = document.getElementById('clippy-textbox');
            
            if (clippy1 && clippy2 && clippy3 && clippyTextbox) {
                console.log('Clippy elements found, animation will start.');
            
            // Function to run the complete animation sequence
            function runClippyAnimation() {
                // Reset state
                clippy1.classList.remove('clippy-visible');
                clippy2.classList.remove('clippy-visible');
                clippy3.classList.remove('clippy-visible');
                clippyTextbox.classList.remove('clippy-visible');
                
                // Start animation
                setTimeout(function() {
                    // Show first Clippy
                    clippy1.classList.add('clippy-visible');
                    
                    // After 1 second, show second Clippy
                    setTimeout(function() {
                        clippy1.classList.remove('clippy-visible');
                        clippy2.classList.add('clippy-visible');
                        
                        // After 1 more second, show third Clippy and textbox
                        setTimeout(function() {
                            clippy2.classList.remove('clippy-visible');
                            clippy3.classList.add('clippy-visible');
                            clippyTextbox.classList.add('clippy-visible');
                            
                            // After 5 seconds, hide all Clippy elements
                            setTimeout(function() {
                                clippy3.classList.remove('clippy-visible');
                                clippyTextbox.classList.remove('clippy-visible');
                            }, 5000);
                        }, 1000);
                    }, 1000);
                }, 0);
            }
            
            // Run the animation immediately once
            runClippyAnimation();
            
                // Then run it every 12 seconds (5s display + 7s pause)
                setInterval(runClippyAnimation, 12000);
            } else {
                console.log('Clippy is disabled or elements not found.');
            }
        });
    </script>
    
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
    <script>
        {{ site_settings_script|safe }}
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
