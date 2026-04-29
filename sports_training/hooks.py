from . import __version__ as app_version

app_name = "sports_training"
app_title = "Sports Training"
app_publisher = "Your Company"
app_description = "Sports & Performance Training Institute Management"
app_email = "info@yourcompany.com"
app_license = "MIT"
required_apps = ["frappe", "erpnext"]

app_include_css = "/assets/sports_training/css/sports_training.css"
app_include_js = "/assets/sports_training/js/sports_training.js"

doctype_js = {
    "Customer": "public/js/customer.js"
}

fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "Sports Training"]]},
    {"dt": "Role", "filters": [["role_name", "in", ["Coach", "Athlete", "Sports Manager", "Physio"]]]}
]

doc_events = {
    "Sales Invoice": {
        "on_submit": "sports_training.sports_training.utils.update_membership_payment"
    }
}

scheduler_events = {
    "daily": [
        "sports_training.sports_training.tasks.send_membership_expiry_reminders",
        "sports_training.sports_training.tasks.update_athlete_attendance_stats"
    ],
    "weekly": [
        "sports_training.sports_training.tasks.generate_performance_reports"
    ]
}

permission_query_conditions = {
    "Athlete": "sports_training.sports_training.utils.get_permission_query_conditions"
}

website_route_rules = [
    {"from_route": "/athletes/<path:name>", "to_route": "athletes"},
]

after_install = "sports_training.setup.install.after_install"
