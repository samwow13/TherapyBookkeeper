# -*- coding: utf-8 -*-
"""
Index Template for the Therapy Bookkeeping Application.
"""

INDEX_TEMPLATE = """
{% extends 'base_template_string' %}

{% block content %}

<!-- Overall Summary Cards -->
<div class="row text-center summary-card">
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Total Income</h5>
                <p class="card-text summary-value credit">{{ '{:,.2f}'.format(overall_income) }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Total Expense</h5>
                <p class="card-text summary-value debit">{{ '{:,.2f}'.format(overall_expense) }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Net Income</h5>
                <p class="card-text summary-value {% if overall_net >= 0 %}credit{% else %}debit{% endif %}">
                    {{ '{:,.2f}'.format(overall_net) }}
                </p>
            </div>
        </div>
    </div>
</div>

<!-- Actions Card -->
<div class="card mb-4 mt-4">
    <div class="card-header bg-light" id="actionsHeader">
        <h5 class="mb-0">Actions</h5>
    </div>
    <div class="card-body">
        <div class="d-flex gap-2 mb-3">
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addTransactionModal">
                <i class="bi bi-plus-circle me-1"></i> Add Transaction
            </button>
            <button type="button" class="btn btn-secondary" data-bs-toggle="modal" data-bs-target="#editCodesModal">
                <i class="bi bi-gear me-1"></i> Edit Codes and Classifications
            </button>
        </div>
    </div>
</div>

<!-- Code Summary Section (Dropdown) -->
<div class="card mb-4">
    <div class="card-header bg-light" id="codeSummaryHeader">
        <button class="btn btn-link btn-block text-left d-flex justify-content-between align-items-center w-100 p-0 text-decoration-none collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#codeSummaryCollapse" aria-expanded="false" aria-controls="codeSummaryCollapse">
            <h5 class="mb-0 ms-3">Code Totals Summary</h5>
            <i class="bi bi-chevron-down me-3"></i>
        </button>
    </div>
    <div id="codeSummaryCollapse" class="collapse" aria-labelledby="codeSummaryHeader">
        <div class="card-body">
            {% if code_totals %}
                <div class="table-responsive">
                    <table class="table table-striped table-sm"> {# table-sm #}
                        <thead class="table-light">
                            <tr>
                                <th>Code</th>
                                <th>Income</th>
                                <th>Expense</th>
                                <th>Net</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for code, totals in code_totals.items() | sort %} {# Sort codes alphabetically #}
                                <tr>
                                    <td><strong>{{ code }}</strong></td>
                                    <td class="credit">{{ '{:,.2f}'.format(totals.income) }}</td>
                                    <td class="debit">{{ '{:,.2f}'.format(totals.expense) }}</td>
                                    <td class="{% if totals.net >= 0 %}credit{% else %}debit{% endif %}">
                                        {{ '{:,.2f}'.format(totals.net) }}
                                    </td>
                                </tr>
                            {% else %}
                             <tr><td colspan="4" class="text-center text-muted">No code data available yet.</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p class="text-muted">No code data available yet.</p>
            {% endif %}
        </div>
    </div>
</div>

<!-- Monthly Summary -->
<div class="card mb-4">
    <div class="card-header bg-light" id="monthlySummaryHeader">
         <button class="btn btn-link btn-block text-left d-flex justify-content-between align-items-center w-100 p-0 text-decoration-none collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#monthlySummaryCollapse" aria-expanded="false" aria-controls="monthlySummaryCollapse">
             <h5 class="mb-0 ms-3">Monthly Summary</h5>
             <i class="bi bi-chevron-down me-3"></i>
         </button>
    </div>
    <div id="monthlySummaryCollapse" class="collapse" aria-labelledby="monthlySummaryHeader">
        <div class="card-body">
            {% if monthly_totals %}
                <div class="accordion" id="monthlyAccordion">
                    {% for month_data in monthly_totals %}
                    <div class="accordion-item" data-month-key="{{ month_data.month_key }}">
                        <h2 class="accordion-header" id="heading{{ loop.index }}">
                            <button class="accordion-button {% if selected_month == month_data.month_key %}{% else %}collapsed{% endif %}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{{ loop.index }}" aria-expanded="{% if selected_month == month_data.month_key %}true{% else %}false{% endif %}" aria-controls="collapse{{ loop.index }}">
                                <div class="d-flex justify-content-between align-items-center w-100">
                                    <div class="fw-bold fs-5">{{ month_data.month }}</div>
                                    <div class="d-flex gap-3 text-end"> {# text-end for alignment #}
                                        <div class="text-success">
                                            <small class="d-block text-muted">Income</small>
                                            <span class="fw-bold">{{ '{:,.2f}'.format(month_data.income) }}</span>
                                        </div>
                                        <div class="text-danger">
                                            <small class="d-block text-muted">Expense</small>
                                            <span class="fw-bold">{{ '{:,.2f}'.format(month_data.expense) }}</span>
                                        </div>
                                        <div class="{% if month_data.net >= 0 %}text-success{% else %}text-danger{% endif %}">
                                            <small class="d-block text-muted">Net</small>
                                            <span class="fw-bold">{{ '{:,.2f}'.format(month_data.net) }}</span>
                                        </div>
                                    </div>
                                </div>
                            </button>
                        </h2>
                        <div id="collapse{{ loop.index }}" class="accordion-collapse collapse {% if selected_month == month_data.month_key %}show{% endif %}" aria-labelledby="heading{{ loop.index }}" data-bs-parent="#monthlyAccordion">
                            <div class="accordion-body">
                                <ul class="list-group list-group-flush">
                                    <li class="list-group-item">
                                        <div class="row align-items-center">
                                            <div class="col-8 text-start">Total Income:</div>
                                            <div class="col-4 text-end">
                                                <span class="badge bg-success rounded-pill fs-6 w-100">{{ '{:,.2f}'.format(month_data.income) }}</span>
                                            </div>
                                        </div>
                                    </li>
                                    <li class="list-group-item">
                                        <div class="row align-items-center">
                                            <div class="col-8 text-start">Total Expense:</div>
                                            <div class="col-4 text-end">
                                                <span class="badge bg-danger rounded-pill fs-6 w-100">{{ '{:,.2f}'.format(month_data.expense) }}</span>
                                            </div>
                                        </div>
                                    </li>
                                    <li class="list-group-item fw-bold">
                                        <div class="row align-items-center">
                                            <div class="col-8 text-start">Net Income:</div>
                                            <div class="col-4 text-end">
                                                <span class="badge {% if month_data.net >= 0 %}bg-success{% else %}bg-danger{% endif %} rounded-pill fs-6 w-100">{{ '{:,.2f}'.format(month_data.net) }}</span>
                                            </div>
                                        </div>
                                    </li>
                                    {% if month_data.codes %}
                                    <li class="list-group-item">
                                        <hr class="mt-2 mb-3">
                                        <h5 class="fw-bold text-primary mb-2"><i class="bi bi-tag-fill me-2"></i>Codes Summary for {{ month_data.month }}</h5>
                                        <div class="card bg-light">
                                            <div class="card-body py-2 px-3">
                                                {% for code, totals in month_data.codes.items() | sort %} {# Sort codes #}
                                                <div class="row align-items-center {% if not loop.last %}mb-2{% endif %}">
                                                    <div class="col-8 text-start">{{ code }}:</div>
                                                    <div class="col-4 text-end">
                                                        <span class="badge {% if totals.net >= 0 %}bg-success{% else %}bg-danger{% endif %} rounded-pill fs-6 w-100">
                                                            {{ '{:,.2f}'.format(totals.net) }}
                                                        </span>
                                                    </div>
                                                </div>
                                                {% else %}
                                                 <p class="text-muted mb-0">No code breakdown available.</p>
                                                {% endfor %}
                                            </div>
                                        </div>
                                    </li>
                                    {% endif %} {# End if month_data.codes #}
                                </ul>
                            </div>
                        </div>
                    </div>
                    {% else %}
                     <p class="text-muted">No monthly data available yet.</p>
                    {% endfor %}
                </div>
            {% else %}
                <p class="text-muted">No monthly data available yet.</p>
            {% endif %}
        </div>
    </div>
</div>

<!-- All Transactions Section (Always Displayed) -->
<div class="card mb-4">
    <div class="card-header bg-light" id="allTransactionsHeader">
        <button id="allTransactionsButton" class="btn btn-link btn-block text-left d-flex justify-content-between align-items-center w-100 p-0 text-decoration-none {% if ui_state.get('allTransactionsCollapse') != 'show' %}collapsed{% endif %}" type="button" data-bs-toggle="collapse" data-bs-target="#allTransactionsCollapse" aria-expanded="{{ 'true' if ui_state.get('allTransactionsCollapse') == 'show' else 'false' }}" aria-controls="allTransactionsCollapse">
            <h5 class="mb-0 ms-3">All Transactions</h5>
            <i class="bi bi-chevron-down me-3"></i>
        </button>
    </div>
    <div id="allTransactionsCollapse" class="collapse {% if ui_state.get('allTransactionsCollapse') == 'show' %}show{% endif %}" aria-labelledby="allTransactionsHeader">
        <div class="card-body">
            <!-- All Transactions Organized by Month -->
            {% if transactions_by_month %}
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h6 class="mb-0">Showing all transactions organized by month</h6>
                    <div class="d-flex">
                        <div class="input-group me-2" style="width: 200px;">
                            <input type="number" class="form-control" id="yearFilter" placeholder="Filter by Year" min="2000" max="2100" value="">
                            <button class="btn btn-outline-secondary" type="button" id="applyYearFilter">Filter</button>
                            <button class="btn btn-outline-secondary" type="button" id="clearYearFilter">Clear</button>
                        </div>
                        <a href="{{ url_for('print_all_transactions') }}" target="_blank" class="btn btn-sm btn-outline-secondary me-2"><i class="bi bi-printer"></i> Print All</a>
                        <button type="button" class="btn btn-sm btn-outline-secondary" data-bs-toggle="modal" data-bs-target="#printYearModal"><i class="bi bi-printer"></i> Print By Year</button>
                    </div>
                </div>
                
                <div class="accordion" id="transactionsByMonthAccordion">
                    {% for month_key, month_data in transactions_by_month.items() %}
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="monthHeading-{{ month_key }}"> 
                            <button id="monthButton-{{ month_key }}" class="accordion-button {% if ui_state.get('monthCollapse-' + month_key) != 'show' %}collapsed{% endif %}" type="button" data-bs-toggle="collapse" data-bs-target="#monthCollapse-{{ month_key }}" aria-expanded="{{ 'true' if ui_state.get('monthCollapse-' + month_key) == 'show' else 'false' }}" aria-controls="monthCollapse-{{ month_key }}"> 
                                <div class="d-flex justify-content-between align-items-center w-100">
                                    <div class="fw-bold fs-5">{{ month_data.month_name }}</div>
                                    <div class="badge bg-primary rounded-pill">{{ month_data.transactions|length }} transactions</div>
                                </div>
                            </button>
                        </h2>
                        <div id="monthCollapse-{{ month_key }}" class="accordion-collapse collapse {% if ui_state.get('monthCollapse-' + month_key) == 'show' %}show{% endif %}" aria-labelledby="monthHeading-{{ month_key }}" data-bs-parent="#transactionsByMonthAccordion"> 
                            <div class="accordion-body p-0">
                                <!-- Transactions Table for This Month -->
                                <div class="table-responsive">
                                    <table class="table table-striped table-hover mb-0">
                                        <thead class="table-light">
                                            <tr>
                                                <th>Date</th>
                                                <th>Description</th>
                                                <th>Code</th>
                                                <th>Classification</th>
                                                <th class="text-end">Amount</th>
                                                <th class="text-center">Actions</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {% for transaction in month_data.transactions %}
                                            <tr data-transaction-id="{{ transaction.id }}">
                                                <td>{{ transaction.date }}</td>
                                                <td>{{ transaction.description }}</td>
                                                <td>{{ transaction.code }}</td>
                                                <td>{{ transaction.classification }}</td>
                                                <td class="text-end {% if transaction.type == 'credit' %}credit{% else %}debit{% endif %}">
                                                    {% if transaction.type == 'credit' %}
                                                        {{ '{:,.2f}'.format(transaction.amount) }}
                                                    {% else %}
                                                        -{{ '{:,.2f}'.format(transaction.amount) }}
                                                    {% endif %}
                                                </td>
                                                <td class="text-center">
                                                    <div class="btn-group" role="group">
                                                        <button type="button" class="btn btn-sm btn-outline-primary edit-btn" data-bs-toggle="modal" data-bs-target="#editTransactionModal" 
                                                           data-transaction-id="{{ transaction.id }}"
                                                           data-date="{{ transaction.date }}"
                                                           data-description="{{ transaction.description }}"
                                                           data-amount="{{ transaction.amount }}"
                                                           data-type="{{ transaction.type }}"
                                                           data-classification="{{ transaction.classification }}"
                                                           data-code="{{ transaction.code }}">
                                                            <i class="bi bi-pencil"></i>
                                                        </button>
                                                        <button type="button" class="btn btn-sm btn-outline-danger delete-btn" data-bs-toggle="modal" data-bs-target="#deleteTransactionModal" 
                                                           data-transaction-id="{{ transaction.id }}"
                                                           data-description="{{ transaction.description }}">
                                                            <i class="bi bi-trash"></i>
                                                        </button>
                                                    </div>
                                                </td>
                                            </tr>
                                            {% endfor %}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            {% elif all_transactions %}
                <!-- Fallback to flat list if not grouped by month -->
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h6 class="mb-0">Showing all transactions</h6>
                    <div class="d-flex">
                        <div class="input-group me-2" style="width: 200px;">
                            <input type="number" class="form-control" id="yearFilterFlat" placeholder="Filter by Year" min="2000" max="2100" value="">
                            <button class="btn btn-outline-secondary" type="button" id="applyYearFilterFlat">Filter</button>
                            <button class="btn btn-outline-secondary" type="button" id="clearYearFilterFlat">Clear</button>
                        </div>
                        <a href="{{ url_for('print_all_transactions') }}" target="_blank" class="btn btn-sm btn-outline-secondary me-2"><i class="bi bi-printer"></i> Print All</a>
                        <button type="button" class="btn btn-sm btn-outline-secondary" data-bs-toggle="modal" data-bs-target="#printYearModal"><i class="bi bi-printer"></i> Print By Year</button>
                    </div>
                </div>
                
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>Date</th>
                                <th>Description</th>
                                <th>Code</th>
                                <th>Classification</th>
                                <th class="text-end">Amount</th>
                                <th class="text-center">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for transaction in all_transactions %}
                            <tr data-transaction-id="{{ transaction.id }}">
                                <td>{{ transaction.date }}</td>
                                <td>{{ transaction.description }}</td>
                                <td>{{ transaction.code }}</td>
                                <td>{{ transaction.classification }}</td>
                                <td class="text-end {% if transaction.type == 'credit' %}credit{% else %}debit{% endif %}">
                                    {% if transaction.type == 'credit' %}
                                        {{ '{:,.2f}'.format(transaction.amount) }}
                                    {% else %}
                                        -{{ '{:,.2f}'.format(transaction.amount) }}
                                    {% endif %}
                                </td>
                                <td class="text-center">
                                    <div class="btn-group" role="group">
                                        <button type="button" class="btn btn-sm btn-outline-primary edit-btn" data-bs-toggle="modal" data-bs-target="#editTransactionModal" 
                                           data-transaction-id="{{ transaction.id }}"
                                           data-date="{{ transaction.date }}"
                                           data-description="{{ transaction.description }}"
                                           data-amount="{{ transaction.amount }}"
                                           data-type="{{ transaction.type }}"
                                           data-classification="{{ transaction.classification }}"
                                           data-code="{{ transaction.code }}">
                                            <i class="bi bi-pencil"></i>
                                        </button>
                                        <button type="button" class="btn btn-sm btn-outline-danger delete-btn" data-bs-toggle="modal" data-bs-target="#deleteTransactionModal" 
                                           data-transaction-id="{{ transaction.id }}"
                                           data-description="{{ transaction.description }}">
                                            <i class="bi bi-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p class="text-muted">No transactions recorded yet.</p>
            {% endif %}
        </div>
    </div>
</div>

<!-- Year Filter JavaScript -->
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // For transactions organized by month
        const yearFilter = document.getElementById('yearFilter');
        const applyYearFilter = document.getElementById('applyYearFilter');
        const clearYearFilter = document.getElementById('clearYearFilter');
        const accordionItems = document.querySelectorAll('#transactionsByMonthAccordion .accordion-item');
        
        // Initial state - store original display settings
        accordionItems.forEach(item => {
            item._originalDisplay = item.style.display || '';
        });
        
        // Apply filter function for transactions by month
        function applyMonthFilter() {
            const year = yearFilter.value.trim();
            if (!year) {
                clearMonthFilter();
                return;
            }
            
            accordionItems.forEach(item => {
                const monthHeader = item.querySelector('.accordion-button .fw-bold');
                if (monthHeader) {
                    const monthText = monthHeader.textContent;
                    if (monthText.includes(year)) {
                        item.style.display = item._originalDisplay;
                    } else {
                        item.style.display = 'none';
                    }
                }
            });
        }
        
        // Clear filter function for transactions by month
        function clearMonthFilter() {
            accordionItems.forEach(item => {
                item.style.display = item._originalDisplay;
            });
            yearFilter.value = '';
        }
        
        // Attach event listeners for transactions by month
        if (applyYearFilter) {
            applyYearFilter.addEventListener('click', applyMonthFilter);
        }
        
        if (clearYearFilter) {
            clearYearFilter.addEventListener('click', clearMonthFilter);
        }
        
        if (yearFilter) {
            yearFilter.addEventListener('keyup', function(event) {
                if (event.key === 'Enter') {
                    applyMonthFilter();
                }
            });
        }
        
        // For flat list of transactions
        const yearFilterFlat = document.getElementById('yearFilterFlat');
        const applyYearFilterFlat = document.getElementById('applyYearFilterFlat');
        const clearYearFilterFlat = document.getElementById('clearYearFilterFlat');
        const flatTableRows = document.querySelectorAll('#allTransactionsTable tbody tr');
        
        // Initial state - store original display settings for flat table
        flatTableRows.forEach(row => {
            row._originalDisplay = row.style.display || '';
        });
        
        // Apply filter function for flat transactions table
        function applyFlatFilter() {
            const year = yearFilterFlat.value.trim();
            if (!year) {
                clearFlatFilter();
                return;
            }
            
            flatTableRows.forEach(row => {
                const dateCell = row.querySelector('td:first-child');
                if (dateCell) {
                    const dateText = dateCell.textContent.trim();
                    // Date format is typically YYYY-MM-DD
                    if (dateText.startsWith(year)) {
                        row.style.display = row._originalDisplay;
                    } else {
                        row.style.display = 'none';
                    }
                }
            });
        }
        
        // Clear filter function for flat transactions table
        function clearFlatFilter() {
            flatTableRows.forEach(row => {
                row.style.display = row._originalDisplay;
            });
            yearFilterFlat.value = '';
        }
        
        // Attach event listeners for flat transactions list
        if (applyYearFilterFlat) {
            applyYearFilterFlat.addEventListener('click', applyFlatFilter);
        }
        
        if (clearYearFilterFlat) {
            clearYearFilterFlat.addEventListener('click', clearFlatFilter);
        }
        
        if (yearFilterFlat) {
            yearFilterFlat.addEventListener('keyup', function(event) {
                if (event.key === 'Enter') {
                    applyFlatFilter();
                }
            });
        }
    });
</script>

{# Add this script block for saving collapse state #}
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Target the main collapse and all monthly collapses within the "All Transactions" section
    const collapseElements = document.querySelectorAll('#allTransactionsCollapse, [id^="monthCollapse-"]');

    collapseElements.forEach(element => {
        // Listen for Bootstrap collapse events
        element.addEventListener('shown.bs.collapse', handleCollapseToggle);
        element.addEventListener('hidden.bs.collapse', handleCollapseToggle);
    });

    function handleCollapseToggle(event) {
        const elementId = event.target.id;
        // Determine state based on the event type
        const state = event.type === 'shown.bs.collapse' ? 'show' : 'hide';

        // Ensure we are only saving state for the intended elements
        if (elementId === 'allTransactionsCollapse' || elementId.startsWith('monthCollapse-')) {
            saveUIState(elementId, state);
        }
    }

    // === Year Filter Persistence ===
    const yearFilterInput = document.getElementById('yearFilter');
    const applyYearFilterButton = document.getElementById('applyYearFilter');
    const clearYearFilterButton = document.getElementById('clearYearFilter');
    const yearFilterStorageKey = 'yearFilterValue';

    // 1. Restore value on page load
    const savedYear = localStorage.getItem(yearFilterStorageKey);
    if (savedYear && yearFilterInput) {
        yearFilterInput.value = savedYear;
        // Optional: Trigger the filter logic if needed after restoring
        // applyYearFilterButton.click(); // Uncomment if filter should apply automatically on load
    }

    // 2. Save value when Apply button is clicked
    if (applyYearFilterButton && yearFilterInput) {
        applyYearFilterButton.addEventListener('click', function() {
            const yearValue = yearFilterInput.value;
            if (yearValue) {
                localStorage.setItem(yearFilterStorageKey, yearValue);
            } else {
                // If the input is cleared manually and then applied, remove the stored value
                localStorage.removeItem(yearFilterStorageKey);
            }
            // Note: The actual filtering logic (page reload or AJAX) should still proceed as before.
            // This script only handles saving the value.
        });
    }

    // 3. Clear value when Clear button is clicked
    if (clearYearFilterButton && yearFilterInput) {
        clearYearFilterButton.addEventListener('click', function() {
            localStorage.removeItem(yearFilterStorageKey);
            yearFilterInput.value = ''; // Ensure the input field is cleared visually
            // Note: The actual filter clearing logic should still proceed as before.
        });
    }
    // === End Year Filter Persistence ===

    // --- Scroll Position Persistence ---
    let scrollTimeout; // Variable to hold the timeout ID

    // Function to restore scroll position
    function restoreScrollPosition() {
        const savedScrollPos = sessionStorage.getItem('scrollPos');
        if (savedScrollPos !== null) {
            // Use setTimeout to ensure scrolling happens after potential layout shifts
            setTimeout(() => {
                window.scrollTo(0, parseInt(savedScrollPos, 10));
                console.log(`Scroll position restored to: ${savedScrollPos}`); // Optional logging
            }, 100); // Increased delay slightly for potentially complex layouts
        }
    }

    // Listen for scroll events to save position
    window.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            try {
                sessionStorage.setItem('scrollPos', window.scrollY);
                console.log(`Scroll position saved: ${window.scrollY}`); // Optional logging
            } catch (e) {
                console.error('Failed to save scroll position to sessionStorage:', e);
            }
        }, 250); // Debounce saving
    });

    // Restore scroll position when the window finishes loading all content
    window.addEventListener('load', restoreScrollPosition);

    // --- End Scroll Position Persistence ---

    function saveUIState(elementId, state) {
        console.log(`Saving state: ${elementId} = ${state}`); // Debug logging
        fetch('/save_ui_state', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // IMPORTANT: Add CSRF token header if your Flask app uses CSRF protection
                // Example for Flask-WTF: 'X-CSRFToken': '{{ '{{ csrf_token() }}' }}'
            },
            body: JSON.stringify({ id: elementId, state: state })
        })
        .then(response => {
            if (!response.ok) {
                console.error('Failed to save UI state. Status:', response.statusText);
                // Optionally, inform the user
            } else {
                 console.log('UI state saved successfully.'); // Confirmation logging
            }
        })
        .catch(error => {
            console.error('Error sending UI state:', error);
            // Optionally, inform the user about the network error
        });
    }

    // Initial check - Apply state from sessionStorage for faster perceived load (optional but recommended)
    // This complements the server-side rendering based on Flask session
    collapseElements.forEach(element => {
        const savedState = sessionStorage.getItem(element.id);
        if (savedState === 'show') {
            // Use Bootstrap's JS API to show without triggering the event/AJAX call again
            const bsCollapse = bootstrap.Collapse.getInstance(element) || new bootstrap.Collapse(element, { toggle: false });
            bsCollapse.show();
        } else if (savedState === 'hide') {
             const bsCollapse = bootstrap.Collapse.getInstance(element) || new bootstrap.Collapse(element, { toggle: false });
             bsCollapse.hide();
        }
        // If no state in sessionStorage, rely on server-rendered state
    });

     // Also save to sessionStorage when toggling
     function handleCollapseToggle(event) { // Redefine to include sessionStorage
        const elementId = event.target.id;
        const state = event.type === 'shown.bs.collapse' ? 'show' : 'hide';

        if (elementId === 'allTransactionsCollapse' || elementId.startsWith('monthCollapse-')) {
            // Save to server via AJAX
            saveUIState(elementId, state);
            // Save to browser's sessionStorage
            try {
                sessionStorage.setItem(elementId, state);
                console.log(`State saved to sessionStorage: ${elementId} = ${state}`);
            } catch (e) {
                console.error('Failed to save state to sessionStorage:', e);
            }
        }
    }
});
</script>


{% if selected_month %}
<div class="monthly-transactions mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h3>Transactions for {{ monthly_totals | selectattr('month_key', 'equalto', selected_month) | map(attribute='month') | first }}</h3>
        <a href="{{ url_for('print_transactions', month=selected_month) }}" target="_blank" class="btn btn-sm btn-outline-secondary"><i class="bi bi-printer"></i> Print View</a>
    </div>
    
    <!-- Monthly Transaction Table -->
    {% if monthly_transactions %}
    <div class="table-responsive">
        <table class="table table-striped table-hover">
            <thead class="table-light">
                <tr>
                    <th>Date</th>
                    <th>Description</th>
                    <th>Code</th>
                    <th>Classification</th>
                    <th class="text-end">Amount</th>
                    <th class="text-center">Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for transaction in monthly_transactions %}
                <tr data-transaction-id="{{ transaction.id }}">
                    <td>{{ transaction.date }}</td>
                    <td>{{ transaction.description }}</td>
                    <td>{{ transaction.code }}</td>
                    <td>{{ transaction.classification }}</td>
                    <td class="text-end {% if transaction.type == 'credit' %}credit{% else %}debit{% endif %}">
                        {% if transaction.type == 'credit' %}
                            {{ '{:,.2f}'.format(transaction.amount) }}
                        {% else %}
                            -{{ '{:,.2f}'.format(transaction.amount) }}
                        {% endif %}
                    </td>
                    <td class="text-center">
                        <div class="btn-group" role="group">
                            <button type="button" class="btn btn-sm btn-outline-primary edit-btn" data-bs-toggle="modal" data-bs-target="#editTransactionModal" 
                               data-transaction-id="{{ transaction.id }}"
                               data-date="{{ transaction.date }}"
                               data-description="{{ transaction.description }}"
                               data-amount="{{ transaction.amount }}"
                               data-type="{{ transaction.type }}"
                               data-classification="{{ transaction.classification }}"
                               data-code="{{ transaction.code }}">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button type="button" class="btn btn-sm btn-outline-danger delete-btn" data-bs-toggle="modal" data-bs-target="#deleteTransactionModal" 
                               data-transaction-id="{{ transaction.id }}"
                               data-description="{{ transaction.description }}">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <div class="alert alert-info">
        No transactions recorded for this month.
    </div>
    {% endif %}
</div>
{% endif %}

{% include 'modals.html' %}
{% endblock %}

"""
