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
        <div class="d-flex justify-content-center gap-3">
            <button type="button" class="btn btn-edit-codes" data-bs-toggle="modal" data-bs-target="#editCodesModal">
                <i class="bi bi-gear"></i> Edit Available Codes & Classifications
            </button>
            <button type="button" class="btn btn-add-transaction" data-bs-toggle="modal" data-bs-target="#addTransactionModal">
                <i class="bi bi-plus-circle"></i> Add New Transaction
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
                                     <li class="list-group-item text-center mt-2">
                                         <a href="{{ url_for('index', month=month_data.month_key) }}" class="btn btn-outline-primary btn-sm">
                                             View Transactions for {{ month_data.month }}
                                         </a>
                                     </li>
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

{% if selected_month %}
<!-- Monthly Transactions (Displayed Only if Month Selected) -->
<div class="monthly-transactions mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h2>Transactions for {{ selected_month_display }}</h2>
        <div>
            <a href="{{ url_for('print_transactions', month=selected_month) }}" target="_blank" class="btn btn-primary btn-sm me-2">
                <i class="bi bi-printer"></i> Print View
            </a>
            <a href="{{ url_for('index') }}" class="btn btn-outline-secondary btn-sm">
                <i class="bi bi-x-circle"></i> Clear Filter
            </a>
        </div>
    </div>

    {% if filtered_transactions %}
    <div class="table-responsive">
        <table class="table table-striped table-hover table-sm"> {# table-sm #}
            <thead class="table-light">
                <tr>
                    <th>Date</th>
                    <th>Description</th>
                    <th>Classification</th>
                    <th>Code</th>
                    <th>Amount</th>
                    <th>Type</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for transaction in filtered_transactions %}
                <tr>
                    <td>{{ transaction.date }}</td>
                    <td>{{ transaction.description }}</td>
                    <td>{{ transaction.classification }}</td>
                    <td>{{ transaction.code }}</td>
                    <td>{{ '{:,.2f}'.format(transaction.amount) }}</td>
                    <td class="{% if transaction.type == 'credit' %}credit{% else %}debit{% endif %}">
                        {{ transaction.type|capitalize }}
                    </td>
                    <td>
                        <div class="btn-group btn-group-sm" role="group">
                            <button type="button" class="btn btn-outline-primary" 
                                    data-bs-toggle="modal" 
                                    data-bs-target="#editTransactionModal"
                                    data-transaction-id="{{ transaction.id }}"
                                    data-transaction-date="{{ transaction.date }}"
                                    data-transaction-description="{{ transaction.description }}"
                                    data-transaction-amount="{{ transaction.amount }}"
                                    data-transaction-type="{{ transaction.type }}"
                                    data-transaction-code="{{ transaction.code }}"
                                    data-transaction-classification="{{ transaction.classification }}">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button type="button" class="btn btn-outline-danger" 
                                    data-bs-toggle="modal" 
                                    data-bs-target="#deleteTransactionModal"
                                    data-transaction-id="{{ transaction.id }}"
                                    data-transaction-description="{{ transaction.description }}">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="7" class="text-center text-muted">No transactions found for this month.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <div class="alert alert-info">
        <i class="bi bi-info-circle me-2"></i> No transactions found for {{ selected_month_display }}.
    </div>
    {% endif %}
</div>
{% else %}
<!-- All Transactions (Displayed if No Month Selected) -->
<div class="card mb-4">
    <div class="card-header bg-light" id="allTransactionsHeader">
        <button class="btn btn-link btn-block text-left d-flex justify-content-between align-items-center w-100 p-0 text-decoration-none collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#allTransactionsCollapse" aria-expanded="false" aria-controls="allTransactionsCollapse">
            <h5 class="mb-0 ms-3">Recent Transactions</h5>
            <i class="bi bi-chevron-down me-3"></i>
        </button>
    </div>
    <div id="allTransactionsCollapse" class="collapse" aria-labelledby="allTransactionsHeader">
        <div class="card-body">
            {% if recent_transactions %}
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="mb-0">Showing {{ recent_transactions|length }} most recent transactions</h5>
                <div>
                    <a href="{{ url_for('print_all_transactions') }}" target="_blank" class="btn btn-primary btn-sm">
                        <i class="bi bi-printer"></i> Print All Transactions
                    </a>
                </div>
            </div>
            <div class="table-responsive">
                <table class="table table-striped table-hover table-sm"> {# table-sm #}
                    <thead class="table-light">
                        <tr>
                            <th>Date</th>
                            <th>Description</th>
                            <th>Classification</th>
                            <th>Code</th>
                            <th>Amount</th>
                            <th>Type</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for transaction in recent_transactions %}
                        <tr>
                            <td>{{ transaction.date }}</td>
                            <td>{{ transaction.description }}</td>
                            <td>{{ transaction.classification }}</td>
                            <td>{{ transaction.code }}</td>
                            <td>{{ '{:,.2f}'.format(transaction.amount) }}</td>
                            <td class="{% if transaction.type == 'credit' %}credit{% else %}debit{% endif %}">
                                {{ transaction.type|capitalize }}
                            </td>
                            <td>
                                <div class="btn-group btn-group-sm" role="group">
                                    <button type="button" class="btn btn-outline-primary" 
                                            data-bs-toggle="modal" 
                                            data-bs-target="#editTransactionModal"
                                            data-transaction-id="{{ transaction.id }}"
                                            data-transaction-date="{{ transaction.date }}"
                                            data-transaction-description="{{ transaction.description }}"
                                            data-transaction-amount="{{ transaction.amount }}"
                                            data-transaction-type="{{ transaction.type }}"
                                            data-transaction-code="{{ transaction.code }}"
                                            data-transaction-classification="{{ transaction.classification }}">
                                        <i class="bi bi-pencil"></i>
                                    </button>
                                    <button type="button" class="btn btn-outline-danger" 
                                            data-bs-toggle="modal" 
                                            data-bs-target="#deleteTransactionModal"
                                            data-transaction-id="{{ transaction.id }}"
                                            data-transaction-description="{{ transaction.description }}">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="7" class="text-center text-muted">No transactions found.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="alert alert-info">
                <i class="bi bi-info-circle me-2"></i> No transactions found. Add some using the "Add New Transaction" button above.
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endif %}

{% endblock %}
"""
