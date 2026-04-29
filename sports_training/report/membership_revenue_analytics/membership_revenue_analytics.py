import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"label": _("Plan"), "fieldname": "membership_plan", "fieldtype": "Link", "options": "Membership Plan", "width": 180},
        {"label": _("Active Members"), "fieldname": "active_count", "fieldtype": "Int", "width": 140},
        {"label": _("Total Revenue"), "fieldname": "total_revenue", "fieldtype": "Currency", "width": 160},
        {"label": _("Pending Amount"), "fieldname": "pending", "fieldtype": "Currency", "width": 160}
    ]

    data = frappe.db.sql("""
        SELECT membership_plan,
               COUNT(*) as active_count,
               SUM(amount_paid) as total_revenue,
               SUM(balance_due) as pending
        FROM `tabAthlete Membership`
        WHERE docstatus = 1 AND status = 'Active'
        GROUP BY membership_plan
    """, as_dict=True)

    return columns, data
