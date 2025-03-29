# -*- coding: utf-8 -*-
"""
Print Modals for the Therapy Bookkeeping Application.
Contains all print-related modal components.
"""

PRINT_MODALS_HTML = """
<!-- Print Year Modal -->
<div class="modal fade" id="printYearModal" tabindex="-1" aria-labelledby="printYearModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="printYearModalLabel">Print Year Report</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form action="/print/year/" method="get" id="printYearForm">
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="print_year" class="form-label">Enter Year (YYYY)</label>
                        <input type="text" class="form-control" id="print_year" name="year" 
                               pattern="\\d{4}" maxlength="4" 
                               placeholder="Enter 4-digit year (e.g., 2025)" 
                               title="Please enter a valid 4-digit year" required>
                        <div class="form-text">Enter a 4-digit year to generate a report for that year.</div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Generate Report</button>
                </div>
            </form>
        </div>
    </div>
</div>
"""

PRINT_MODALS_SCRIPT = """
// Set up print year form
document.getElementById('printYearForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const year = document.getElementById('print_year').value;
    
    // Validate that the year is a 4-digit number
    if (!/^\\d{4}$/.test(year)) {
        alert('Please enter a valid 4-digit year');
        return;
    }
    
    // Build the URL with the year parameter and navigate to it
    window.location.href = `/print/year/${year}`;
});

// Additional validation for the year input
document.getElementById('print_year').addEventListener('input', function() {
    // Only allow numbers to be typed
    this.value = this.value.replace(/[^0-9]/g, '');
    
    // Limit to 4 digits
    if (this.value.length > 4) {
        this.value = this.value.slice(0, 4);
    }
});
"""
