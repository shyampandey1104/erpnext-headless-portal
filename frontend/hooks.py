# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "frontend"
app_title = "Erpnext Headless Portal"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Headless Portal for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/frontend/css/frontend.bundle.css"
app_include_js = "/assets/frontend/js/frontend.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "frontend.engine.on_document_submit",
        "on_cancel": "frontend.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "frontend.engine.daily_scheduled_sync"
    ]
}
