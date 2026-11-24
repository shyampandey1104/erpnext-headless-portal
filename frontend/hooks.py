# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "frontend"
app_title = "Erpnext Headless Portal"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Headless Portal - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/frontend/css/frontend.bundle.css"
app_include_js = "/assets/frontend/js/frontend.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Erpnext Headless Portal Entry": {
        "validate": "frontend.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "frontend.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "frontend.tasks.hourly_sync"
    ],
    "daily": [
        "frontend.tasks.daily_reconciliation"
    ],
    "weekly": [
        "frontend.tasks.weekly_digest"
    ]
}
