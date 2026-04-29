import frappe


def update_membership_payment(doc, method):
    """Update Athlete Membership when Sales Invoice is submitted"""
    for item in doc.items:
        if item.item_code and item.item_code.startswith("MEMB-"):
            membership = frappe.db.get_value("Athlete Membership",
                                              {"sales_invoice": doc.name}, "name")
            if membership:
                m = frappe.get_doc("Athlete Membership", membership)
                m.amount_paid = doc.grand_total - doc.outstanding_amount
                m.save(ignore_permissions=True)


def get_permission_query_conditions(user):
    """Athletes only see their own record"""
    if not user:
        user = frappe.session.user
    if "Sports Manager" in frappe.get_roles(user) or "Coach" in frappe.get_roles(user):
        return ""
    return f"`tabAthlete`.email = '{user}'"
