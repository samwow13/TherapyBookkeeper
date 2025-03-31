# -*- coding: utf-8 -*-
"""
Index Template for the Therapy Bookkeeping Application.
"""

INDEX_TEMPLATE = """
{% extends 'base_template_string' %}

{% block content %}

<!-- Year Filter -->
<div class="row mb-3">
    <div class="col-md-4">
        <label for="yearFilterInput" class="form-label">Filter Summary by Year:</label>
        <div class="input-group">
            <input type="number" class="form-control" id="yearFilterInput" value="{{ current_year }}">
            <button class="btn btn-outline-secondary" type="button" id="yearFilterButton">Go</button>
        </div>
    </div>
</div>

<!-- Overall Summary Cards -->
<div class="row text-center summary-card">
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Total Income</h5>
                <p class="card-text summary-value credit" id="totalIncomeValue">{{ '{:,.2f}'.format(overall_income) }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Total Expense</h5>
                <p class="card-text summary-value debit" id="totalExpenseValue">{{ '{:,.2f}'.format(overall_expense) }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Net Income</h5>
                <p class="card-text summary-value {% if overall_net >= 0 %}credit{% else %}debit{% endif %}" id="netIncomeValue">
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
            <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#shutdownConfirmModal">
                <i class="bi bi-power me-1"></i> Shutdown Application
            </button>
        </div>
    </div>
</div>

<!-- Code Summary Section (Dropdown) -->
<div class="card mb-4">
    <div class="card-header bg-light" id="codeSummaryHeader">
        <button id="codeSummaryButton" class="btn btn-link btn-block text-left d-flex justify-content-between align-items-center w-100 p-0 text-decoration-none {% if ui_state.get('codeSummaryCollapse') != 'show' %}collapsed{% endif %}" type="button" data-bs-toggle="collapse" data-bs-target="#codeSummaryCollapse" aria-expanded="{{ 'true' if ui_state.get('codeSummaryCollapse') == 'show' else 'false' }}" aria-controls="codeSummaryCollapse">
            <h5 class="mb-0 ms-3">Code & Classifications Summary Tool</h5>
            <i class="bi bi-chevron-down me-3"></i>
        </button>
    </div>
    <div id="codeSummaryCollapse" class="collapse {% if ui_state.get('codeSummaryCollapse') == 'show' %}show{% endif %}" aria-labelledby="codeSummaryHeader">
        <div class="card-body">
            <!-- Year Filter for Code Totals -->
            <div class="d-flex justify-content-end mb-3">
                <div class="input-group" style="width: 200px;">
                    <select id="codeSummaryYearFilter" class="form-select">
                        {% for year in available_years %}
                            <option value="{{ year }}" {% if year|int == selected_year|int %}selected{% endif %}>{{ year }}</option>
                        {% endfor %}
                    </select>
                    <button id="applyCodeSummaryYearFilter" class="btn btn-primary">
                        <i class="bi bi-filter"></i> Filter
                    </button>
                </div>
            </div>
            
            <!-- Tabs for Codes and Classifications -->
            <ul class="nav nav-tabs mb-3" id="codeSummaryTabs" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="code-totals-tab" data-bs-toggle="tab" data-bs-target="#code-totals" type="button" role="tab" aria-controls="code-totals" aria-selected="true">Code Totals</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="classification-totals-tab" data-bs-toggle="tab" data-bs-target="#classification-totals" type="button" role="tab" aria-controls="classification-totals" aria-selected="false">Classification Totals</button>
                </li>
            </ul>
            
            <div class="tab-content" id="codeSummaryTabContent">
                <!-- Code Totals Tab -->
                <div class="tab-pane fade show active" id="code-totals" role="tabpanel" aria-labelledby="code-totals-tab">
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
                                            <td class="text-success">${{ "%.2f"|format(totals.income) }}</td>
                                            <td class="text-danger">${{ "%.2f"|format(totals.expense) }}</td>
                                            <td class="{% if totals.net >= 0 %}text-success{% else %}text-danger{% endif %}">
                                                ${{ "%.2f"|format(totals.net) }}
                                            </td>
                                        </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    {% else %}
                        <p class="text-muted">No code totals available for {{ selected_year }}.</p>
                    {% endif %}
                </div>
                
                <!-- Classification Totals Tab -->
                <div class="tab-pane fade" id="classification-totals" role="tabpanel" aria-labelledby="classification-totals-tab">
                    {% if classification_totals %}
                        <div class="table-responsive">
                            <table class="table table-striped table-sm">
                                <thead class="table-light">
                                    <tr>
                                        <th>Classification</th>
                                        <th>Net Amount</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for classification, amount in classification_totals.items() | sort(reverse=True, attribute='1') %}
                                        <tr>
                                            <td><strong>{{ classification }}</strong></td>
                                            <td class="{% if amount >= 0 %}text-success{% else %}text-danger{% endif %}">
                                                ${{ "%.2f"|format(amount) }}
                                            </td>
                                        </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    {% else %}
                        <p class="text-muted">No classification totals available for {{ selected_year }}.</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Monthly Summary -->
<div class="card mb-4">
    <div class="card-header bg-light" id="monthlySummaryHeader">
         <button id="monthlySummaryButton" class="btn btn-link btn-block text-left d-flex justify-content-between align-items-center w-100 p-0 text-decoration-none {% if ui_state.get('monthlySummaryCollapse') != 'show' %}collapsed{% endif %}" type="button" data-bs-toggle="collapse" data-bs-target="#monthlySummaryCollapse" aria-expanded="{{ 'true' if ui_state.get('monthlySummaryCollapse') == 'show' else 'false' }}" aria-controls="monthlySummaryCollapse">
             <h5 class="mb-0 ms-3">Monthly Summary</h5>
             <i class="bi bi-chevron-down me-3"></i>
         </button>
    </div>
    <div id="monthlySummaryCollapse" class="collapse {% if ui_state.get('monthlySummaryCollapse') == 'show' %}show{% endif %}" aria-labelledby="monthlySummaryHeader">
        <div class="card-body">
            {% if monthly_totals %}
                <div class="accordion" id="monthlyAccordion">
                    {% for month_data in monthly_totals %}
                    <div class="accordion-item" data-month-key="{{ month_data.month_key }}">
                        <h2 class="accordion-header" id="heading{{ loop.index }}">
                            <button class="accordion-button {% if ui_state.get('selected_month') == month_data.month_key %}{% else %}collapsed{% endif %}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{{ loop.index }}" aria-expanded="{{ 'true' if ui_state.get('selected_month') == month_data.month_key else 'false' }}" aria-controls="collapse{{ loop.index }}">
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
                        <div id="collapse{{ loop.index }}" class="accordion-collapse collapse {% if ui_state.get('selected_month') == month_data.month_key %}show{% endif %}" aria-labelledby="heading{{ loop.index }}" data-bs-parent="#monthlyAccordion">
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
                                        <!-- Classifications Summary -->
                                        <div class="mt-4"> 
                                             <h5 class="fw-bold text-info mb-2"><i class="bi bi-bookmark-fill me-2"></i>Classifications Summary for {{ month_data.month }}</h5>
                                             <div class="card bg-light">
                                                 <div class="card-body py-2 px-3">
                                                     {% if month_data.classification_summary %}
                                                         {% for classification, net_total in month_data.classification_summary.items() | sort %}
                                                         <div class="row align-items-center {% if not loop.last %}mb-2{% endif %}">
                                                             <div class="col-8 text-start">{{ classification }}:</div>
                                                             <div class="col-4 text-end">
                                                                 <span class="badge {% if net_total >= 0 %}bg-success{% else %}bg-danger{% endif %} rounded-pill fs-6 w-100">
                                                                     {{ '{:,.2f}'.format(net_total) }}
                                                                 </span>
                                                             </div>
                                                         </div>
                                                         {% else %}
                                                         <p class="text-muted mb-0">No classification breakdown available.</p>
                                                         {% endfor %}
                                                     {% else %}
                                                         <p class="text-muted mb-0">No classification breakdown available.</p>
                                                     {% endif %}
                                                 </div>
                                             </div>
                                         </div>
                                     </li>
                                     {% endif %} 
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
                                                        <button type="button" class="btn btn-sm btn-outline-info copy-btn" data-bs-toggle="modal" data-bs-target="#addTransactionModal" 
                                                           data-date="{{ transaction.date }}"
                                                           data-description="{{ transaction.description }}"
                                                           data-amount="{{ transaction.amount }}"
                                                           data-type="{{ transaction.type }}"
                                                           data-classification="{{ transaction.classification }}"
                                                           data-code="{{ transaction.code }}">
                                                            <i class="bi bi-clipboard-plus"></i>
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
                                        <button type="button" class="btn btn-sm btn-outline-info copy-btn" data-bs-toggle="modal" data-bs-target="#addTransactionModal" 
                                           data-date="{{ transaction.date }}"
                                           data-description="{{ transaction.description }}"
                                           data-amount="{{ transaction.amount }}"
                                           data-type="{{ transaction.type }}"
                                           data-classification="{{ transaction.classification }}"
                                           data-code="{{ transaction.code }}">
                                            <i class="bi bi-clipboard-plus"></i>
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
        const yearInput = document.getElementById('yearFilterInput');
        const yearButton = document.getElementById('yearFilterButton'); // Get the button
        const totalIncomeEl = document.getElementById('totalIncomeValue');
        const totalExpenseEl = document.getElementById('totalExpenseValue');
        const netIncomeEl = document.getElementById('netIncomeValue');

        function formatCurrency(value) {
            return value.toLocaleString('en-US', { style: 'currency', currency: 'USD' }).replace('$', ''); // Keep consistent with Jinja filter
        }

        function updateOverallSummary(year) {
            if (!year || isNaN(year)) {
                console.error("Invalid year provided:", year);
                // Optionally reset fields or show an error message
                totalIncomeEl.textContent = 'N/A';
                totalExpenseEl.textContent = 'N/A';
                netIncomeEl.textContent = 'N/A';
                netIncomeEl.className = 'card-text summary-value'; // Reset class
                return;
            }
            console.log(`Fetching summary for year: ${year}`); // Debug log
            fetch(`/get_summary/${year}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Received summary data:", data); // Debug log
                    if (data.error) {
                         console.error("Error fetching summary:", data.error);
                         totalIncomeEl.textContent = 'Error';
                         totalExpenseEl.textContent = 'Error';
                         netIncomeEl.textContent = 'Error';
                         netIncomeEl.className = 'card-text summary-value'; // Reset class
                         return;
                    }
                    totalIncomeEl.textContent = formatCurrency(data.overall_income || 0);
                    totalExpenseEl.textContent = formatCurrency(data.overall_expense || 0);
                    netIncomeEl.textContent = formatCurrency(data.overall_net || 0);

                    // Update net income color
                    netIncomeEl.classList.remove('credit', 'debit');
                    if ((data.overall_net || 0) >= 0) {
                        netIncomeEl.classList.add('credit');
                    } else {
                        netIncomeEl.classList.add('debit');
                    }
                })
                .catch(error => {
                    console.error('Error fetching or processing overall summary:', error);
                    totalIncomeEl.textContent = 'Error';
                    totalExpenseEl.textContent = 'Error';
                    netIncomeEl.textContent = 'Error';
                    netIncomeEl.className = 'card-text summary-value'; // Reset class
                });
        }

        // Add event listener to the button
        yearButton.addEventListener('click', function() {
            const selectedYear = parseInt(yearInput.value, 10);
            updateOverallSummary(selectedYear);
        });

        // Add event listener for Enter key on the input field
        yearInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault(); // Prevent potential form submission if inside a form
                const selectedYear = parseInt(this.value, 10);
                updateOverallSummary(selectedYear);
            }
        });

        // Initial load - The initial values are now correctly rendered by Jinja
        // for the default year (2025), so no initial JS fetch is needed.
    });
</script>

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

<!-- Year Filter JavaScript for Code Summary -->
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Year filter for Code Summary section
        const codeSummaryYearFilter = document.getElementById('codeSummaryYearFilter');
        const applyCodeSummaryYearFilter = document.getElementById('applyCodeSummaryYearFilter');
        
        if (codeSummaryYearFilter && applyCodeSummaryYearFilter) {
            applyCodeSummaryYearFilter.addEventListener('click', function() {
                const selectedYear = codeSummaryYearFilter.value;
                
                // Instead of saving UI state and immediately redirecting,
                // wait for the save to complete before redirecting
                fetch('/save_ui_state', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ id: 'codeSummaryCollapse', state: 'show' })
                })
                .then(response => {
                    if (response.ok) {
                        // After the state is saved successfully, redirect to the new URL
                        const currentUrl = new URL(window.location.href);
                        // Update or add the year parameter
                        currentUrl.searchParams.set('year', selectedYear);
                        // Redirect to the updated URL
                        window.location.href = currentUrl.toString();
                    } else {
                        console.error('Failed to save UI state');
                        // Still redirect even if saving state fails
                        const currentUrl = new URL(window.location.href);
                        currentUrl.searchParams.set('year', selectedYear);
                        window.location.href = currentUrl.toString();
                    }
                })
                .catch(error => {
                    console.error('Error saving UI state:', error);
                    // Still redirect even if an error occurs
                    const currentUrl = new URL(window.location.href);
                    currentUrl.searchParams.set('year', selectedYear);
                    window.location.href = currentUrl.toString();
                });
            });
        }
        
        // Add event listener for the codeSummaryCollapse element
        const codeSummaryCollapse = document.getElementById('codeSummaryCollapse');
        if (codeSummaryCollapse) {
            codeSummaryCollapse.addEventListener('shown.bs.collapse', function() {
                saveUIState('codeSummaryCollapse', 'show');
                // Save to sessionStorage
                try {
                    sessionStorage.setItem('codeSummaryCollapse', 'show');
                } catch (e) {
                    console.error('Failed to save state to sessionStorage:', e);
                }
            });
            
            codeSummaryCollapse.addEventListener('hidden.bs.collapse', function() {
                saveUIState('codeSummaryCollapse', 'hide');
                // Save to sessionStorage
                try {
                    sessionStorage.setItem('codeSummaryCollapse', 'hide');
                } catch (e) {
                    console.error('Failed to save state to sessionStorage:', e);
                }
            });
        }
    });
</script>

<!-- Specific script for index page -->

<!-- Script for Edit Transaction Modal -->
<script>
    const addTransactionModal = document.getElementById('addTransactionModal');
    const addTransactionForm = document.getElementById('addTransactionForm');
    const modalTitle = addTransactionModal.querySelector('.modal-title');
    const submitButton = addTransactionModal.querySelector('button[type="submit"]');
    const transactionIdInput = document.getElementById('transaction_id');
    const dateInput = document.getElementById('date');
    const descriptionInput = document.getElementById('description');
    const amountInput = document.getElementById('amount');
    const typeInput = document.getElementById('type');
    const codeInput = document.getElementById('code');
    const classificationInput = document.getElementById('classification');

    addTransactionModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget; // Button that triggered the modal
        const isEdit = button && button.classList.contains('edit-transaction-btn');
        const isCopy = button && button.classList.contains('copy-transaction-btn');

        if (isEdit) {
            modalTitle.textContent = 'Edit Transaction';
            submitButton.textContent = 'Save Changes';
            const transactionId = button.getAttribute('data-id');
            // Dynamically set action URL for editing
            addTransactionForm.action = `/edit_transaction/${transactionId}`;

            transactionIdInput.value = transactionId;
            dateInput.value = button.getAttribute('data-date');
            descriptionInput.value = button.getAttribute('data-description');
            amountInput.value = button.getAttribute('data-amount');
            typeInput.value = button.getAttribute('data-type');
            codeInput.value = button.getAttribute('data-code');
            classificationInput.value = button.getAttribute('data-classification');

        } else if (isCopy) {
            modalTitle.textContent = 'Copy Transaction';
            submitButton.textContent = 'Add Transaction';
            // Set action URL for adding (since copy results in a new transaction)
            addTransactionForm.action = '/add_transaction';

            // Populate fields from data attributes
            dateInput.value = button.getAttribute('data-date');
            descriptionInput.value = button.getAttribute('data-description');
            amountInput.value = button.getAttribute('data-amount');
            typeInput.value = button.getAttribute('data-type');
            codeInput.value = button.getAttribute('data-code');
            classificationInput.value = button.getAttribute('data-classification');

            // IMPORTANT: Clear the transaction ID for a copy
            transactionIdInput.value = '';

        } else { // It's an Add operation (modal opened by Add Transaction button)
            modalTitle.textContent = 'Add New Transaction';
            submitButton.textContent = 'Add Transaction';
            // Set action URL for adding
            addTransactionForm.action = '/add_transaction';
            addTransactionForm.reset(); // Clear the form
            transactionIdInput.value = ''; // Ensure ID is clear
        }
    });

    // Optional: Reset modal title and button text when modal is hidden
    addTransactionModal.addEventListener('hidden.bs.modal', function () {
        modalTitle.textContent = 'Add New Transaction'; // Reset to default
        submitButton.textContent = 'Add Transaction';
        // Reset action to the default add action
        addTransactionForm.action = '/add_transaction';
        addTransactionForm.reset();
        transactionIdInput.value = '';
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
    
    // Monthly Summary collapse state tracking
    const monthlySummaryButton = document.getElementById('monthlySummaryButton');
    const monthlySummaryCollapse = document.getElementById('monthlySummaryCollapse');
    
    if (monthlySummaryButton && monthlySummaryCollapse) {
        monthlySummaryCollapse.addEventListener('shown.bs.collapse', function() {
            saveUIState('monthlySummaryCollapse', 'show');
            // Save to sessionStorage
            try {
                sessionStorage.setItem('monthlySummaryCollapse', 'show');
            } catch (e) {
                console.error('Failed to save state to sessionStorage:', e);
            }
        });
        
        monthlySummaryCollapse.addEventListener('hidden.bs.collapse', function() {
            saveUIState('monthlySummaryCollapse', 'hide');
            // Save to sessionStorage
            try {
                sessionStorage.setItem('monthlySummaryCollapse', 'hide');
            } catch (e) {
                console.error('Failed to save state to sessionStorage:', e);
            }
        });
    }
    
    // Month accordion state tracking
    const monthAccordionItems = document.querySelectorAll('#monthlyAccordion .accordion-item');
    
    monthAccordionItems.forEach(item => {
        const monthKey = item.getAttribute('data-month-key');
        const accordionCollapse = item.querySelector('.accordion-collapse');
        
        if (accordionCollapse && monthKey) {
            accordionCollapse.addEventListener('shown.bs.collapse', function() {
                saveUIState('selected_month', monthKey);
                // Save to sessionStorage
                try {
                    sessionStorage.setItem('selected_month', monthKey);
                } catch (e) {
                    console.error('Failed to save state to sessionStorage:', e);
                }
            });
        }
    });

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
});
</script>

<!-- Script for saving UI state -->
<script>
    function saveUIState(id, state) {
        console.log(`Saving state: ${id} = ${state}`); // Debug logging
        fetch('/save_ui_state', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // IMPORTANT: Add CSRF token header if your Flask app uses CSRF protection
                // Example for Flask-WTF: 'X-CSRFToken': '{{ '{{ csrf_token() }}' }}'
            },
            body: JSON.stringify({ id: id, state: state })
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
                            <button type="button" class="btn btn-sm btn-outline-info copy-btn" data-bs-toggle="modal" data-bs-target="#addTransactionModal" 
                               data-date="{{ transaction.date }}"
                               data-description="{{ transaction.description }}"
                               data-amount="{{ transaction.amount }}"
                               data-type="{{ transaction.type }}"
                               data-classification="{{ transaction.classification }}"
                               data-code="{{ transaction.code }}">
                                <i class="bi bi-clipboard-plus"></i>
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
