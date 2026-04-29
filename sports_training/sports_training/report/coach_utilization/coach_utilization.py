import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"label": _("Coach"), "fieldname": "coach", "fieldtype": "Link", "options": "Coach", "width": 140},
        {"label": _("Coach Name"), "fieldname": "coach_name", "fieldtype": "Data", "width": 180},
        {"label": _("Sessions"), "fieldname": "total_sessions", "fieldtype": "Int", "width": 100},
        {"label": _("Hours"), "fieldname": "total_hours", "fieldtype": "Float", "width": 100},
        {"label": _("Athletes Trained"), "fieldname": "unique_athletes", "fieldtype": "Int", "width": 140}
    ]

    conditions = ""
    if filters and filters.get("from_date"):
        conditions += " AND ts.session_date >= %(from_date)s"
    if filters and filters.get("to_date"):
        conditions += " AND ts.session_date <= %(to_date)s"

    data = frappe.db.sql(f"""
        SELECT ts.primary_coach as coach,
               c.coach_name,
               COUNT(DISTINCT ts.name) as total_sessions,
               SUM(ts.duration_hours) as total_hours,
               COUNT(DISTINCT sa.athlete) as unique_athletes
        FROM `tabTraining Session` ts
        LEFT JOIN `tabCoach` c ON c.name = ts.primary_coach
        LEFT JOIN `tabSession Athlete` sa ON sa.parent = ts.name
        WHERE ts.docstatus = 1 {conditions}
        GROUP BY ts.primary_coach
        ORDER BY total_sessions DESC
    """, filters, as_dict=True)

    return columns, data
