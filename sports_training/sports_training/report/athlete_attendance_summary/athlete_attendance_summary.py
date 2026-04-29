import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"label": _("Athlete"), "fieldname": "athlete", "fieldtype": "Link", "options": "Athlete", "width": 140},
        {"label": _("Name"), "fieldname": "athlete_name", "fieldtype": "Data", "width": 180},
        {"label": _("Total Sessions"), "fieldname": "total", "fieldtype": "Int", "width": 120},
        {"label": _("Present"), "fieldname": "present", "fieldtype": "Int", "width": 100},
        {"label": _("Absent"), "fieldname": "absent", "fieldtype": "Int", "width": 100},
        {"label": _("Late"), "fieldname": "late", "fieldtype": "Int", "width": 80},
        {"label": _("Attendance %"), "fieldname": "percentage", "fieldtype": "Percent", "width": 120}
    ]

    conditions = ""
    if filters and filters.get("from_date"):
        conditions += " AND session_date >= %(from_date)s"
    if filters and filters.get("to_date"):
        conditions += " AND session_date <= %(to_date)s"

    data = frappe.db.sql(f"""
        SELECT athlete, athlete_name,
               COUNT(*) as total,
               SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) as present,
               SUM(CASE WHEN status='Absent' THEN 1 ELSE 0 END) as absent,
               SUM(CASE WHEN status='Late' THEN 1 ELSE 0 END) as late,
               (SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END)/COUNT(*))*100 as percentage
        FROM `tabAttendance Log`
        WHERE 1=1 {conditions}
        GROUP BY athlete
        ORDER BY percentage DESC
    """, filters, as_dict=True)

    return columns, data
