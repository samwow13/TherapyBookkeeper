# -*- coding: utf-8 -*-
"""
Print Template Module
Contains the HTML template string for the print view of the Therapy Bookkeeping Application.
"""

PRINT_TEMPLATE = """
{% extends "base_template_string" %}

{% block title %}Print Transactions - Therapy Bookkeeper{% endblock %}

{% block styles %}
{{ super() }}
<style>
    @media print {
        .no-print {
            display: none !important;
        }
        body {
            font-size: 12pt;
        }
        .container {
            width: 100%;
            max-width: 100%;
        }
        .table th, .table td {
            padding: 0.3rem;
        }
        .page-header {
            margin-bottom: 20px;
        }
    }
    .print-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .print-title {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .print-date {
        font-style: italic;
    }
    .summary-box {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .summary-title {
        font-weight: bold;
        margin-bottom: 10px;
    }
    .summary-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
    }
    .total-row {
        font-weight: bold;
        border-top: 2px solid #dee2e6;
    }
    .pagination-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
</style>
{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="print-header">
        <div class="print-title">
            {% if period_type == 'month' %}
                Transactions for {{ month_name }} {{ year }}
            {% elif period_type == 'year' %}
                Transactions for {{ year }}
            {% else %}
                All Transactions
            {% endif %}
        </div>
        <div class="print-date">
            Printed on {{ now.strftime('%Y-%m-%d %H:%M') }}
        </div>
    </div>
    
    <div class="row">
        <div class="col-12">
            <div class="summary-box">
                <div class="summary-title">Financial Summary</div>
                <div class="summary-item">
                    <span>Total Income:</span>
                    <span>${{ "%.2f"|format(summary.total_income) }}</span>
                </div>
                <div class="summary-item">
                    <span>Total Expenses:</span>
                    <span>${{ "%.2f"|format(summary.total_expenses) }}</span>
                </div>
                <div class="summary-item">
                    <span>Net Income:</span>
                    <span>${{ "%.2f"|format(summary.net_income) }}</span>
                </div>
            </div>
        </div>
    </div>

    {% if transactions %}
    <div class="table-responsive">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Description</th>
                    <th>Classification</th>
                    <th>Code</th>
                    <th class="text-end">Amount</th>
                </tr>
            </thead>
            <tbody>
                {% for transaction in transactions %}
                <tr>
                    <td>{{ transaction.date }}</td>
                    <td>{{ transaction.description }}</td>
                    <td>{{ transaction.classification }}</td>
                    <td>{{ transaction.code }}</td>
                    <td class="text-end {% if transaction.amount < 0 %}text-danger{% endif %}">
                        ${{ "%.2f"|format(transaction.amount) }}
                    </td>
                </tr>
                {% endfor %}
                <tr class="total-row">
                    <td colspan="4" class="text-end">Total:</td>
                    <td class="text-end {% if summary.net_income < 0 %}text-danger{% endif %}">
                        ${{ "%.2f"|format(summary.net_income) }}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    {% else %}
    <div class="alert alert-info">
        No transactions found for this period.
    </div>
    {% endif %}
    
    {% if pagination and pagination.pages > 1 %}
    <div class="pagination-container no-print">
        <nav aria-label="Transaction pagination">
            <ul class="pagination">
                {% if pagination.has_prev %}
                <li class="page-item">
                    <a class="page-link" href="{{ url_for(request.endpoint, page=pagination.prev_num, **request.view_args) }}">Previous</a>
                </li>
                {% else %}
                <li class="page-item disabled">
                    <span class="page-link">Previous</span>
                </li>
                {% endif %}
                
                {% for page in pagination.iter_pages() %}
                    {% if page %}
                        {% if page != pagination.page %}
                        <li class="page-item">
                            <a class="page-link" href="{{ url_for(request.endpoint, page=page, **request.view_args) }}">{{ page }}</a>
                        </li>
                        {% else %}
                        <li class="page-item active">
                            <span class="page-link">{{ page }}</span>
                        </li>
                        {% endif %}
                    {% else %}
                        <li class="page-item disabled">
                            <span class="page-link">...</span>
                        </li>
                    {% endif %}
                {% endfor %}
                
                {% if pagination.has_next %}
                <li class="page-item">
                    <a class="page-link" href="{{ url_for(request.endpoint, page=pagination.next_num, **request.view_args) }}">Next</a>
                </li>
                {% else %}
                <li class="page-item disabled">
                    <span class="page-link">Next</span>
                </li>
                {% endif %}
            </ul>
        </nav>
    </div>
    {% endif %}
    
    <div class="mt-4 mb-5 no-print">
        <a href="{{ url_for('index') }}" class="btn btn-secondary">Back to Transactions</a>
        <button onclick="window.print()" class="btn btn-primary ms-2">Print This Page</button>
    </div>
</div>
{% endblock %}
"""
