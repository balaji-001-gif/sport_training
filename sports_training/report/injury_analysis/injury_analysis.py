import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"label": _("Injury Type"), "fieldname": "injury_type", "fieldtype": "Data", "width": 140},
        {"label": _("Severity"), "fieldname": "severity", "fieldtype": "Data", "width": 100},
        {"label": _("Count"), "fieldname": "count", "fieldtype": "Int", "width": 80},
        {"label": _("Avg Recovery Days"), "fieldname": "avg_recovery", "fieldtype": "Float", "width": 160}
    ]

    data = frappe.db.sql("""
        SELECT injury_type, severity, COUNT(*) as count,
               AVG(DATEDIFF(actual_recovery_date, injury_date)) as avg_recovery
        FROM `tabInjury Record`
        WHERE injury_type IS NOT NULL
        GROUP BY injury_type, severity
        ORDER BY count DESC
    """, as_dict=True)

    return columns, data
