import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart


def get_columns():
    return [
        {"label": _("Assessment"), "fieldname": "name", "fieldtype": "Link", "options": "Performance Assessment", "width": 140},
        {"label": _("Athlete"), "fieldname": "athlete", "fieldtype": "Link", "options": "Athlete", "width": 140},
        {"label": _("Athlete Name"), "fieldname": "athlete_name", "fieldtype": "Data", "width": 160},
        {"label": _("Date"), "fieldname": "assessment_date", "fieldtype": "Date", "width": 100},
        {"label": _("Speed"), "fieldname": "speed_score", "fieldtype": "Float", "width": 80},
        {"label": _("Strength"), "fieldname": "strength_score", "fieldtype": "Float", "width": 90},
        {"label": _("Endurance"), "fieldname": "endurance_score", "fieldtype": "Float", "width": 100},
        {"label": _("Agility"), "fieldname": "agility_score", "fieldtype": "Float", "width": 80},
        {"label": _("Technical"), "fieldname": "technical_score", "fieldtype": "Float", "width": 90},
        {"label": _("Tactical"), "fieldname": "tactical_score", "fieldtype": "Float", "width": 90},
        {"label": _("Mental"), "fieldname": "mental_score", "fieldtype": "Float", "width": 80},
        {"label": _("Overall"), "fieldname": "overall_score", "fieldtype": "Float", "width": 90}
    ]


def get_data(filters):
    conditions = "WHERE docstatus = 1"
    if filters and filters.get("athlete"):
        conditions += " AND athlete = %(athlete)s"
    if filters and filters.get("from_date"):
        conditions += " AND assessment_date >= %(from_date)s"
    if filters and filters.get("to_date"):
        conditions += " AND assessment_date <= %(to_date)s"

    return frappe.db.sql(f"""
        SELECT name, athlete, athlete_name, assessment_date,
               speed_score, strength_score, endurance_score, agility_score,
               technical_score, tactical_score, mental_score, overall_score
        FROM `tabPerformance Assessment`
        {conditions}
        ORDER BY assessment_date DESC
    """, filters, as_dict=True)


def get_chart(data):
    if not data:
        return None
    labels = [str(d.assessment_date) for d in data[:10]][::-1]
    values = [d.overall_score or 0 for d in data[:10]][::-1]
    return {
        "data": {
            "labels": labels,
            "datasets": [{"name": "Overall Score", "values": values}]
        },
        "type": "line"
    }
