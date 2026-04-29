import frappe


def after_install():
    create_roles()
    create_default_sports()
    create_custom_fields()
    frappe.db.commit()


def create_roles():
    roles = ["Sports Manager", "Coach", "Athlete", "Physio"]
    for r in roles:
        if not frappe.db.exists("Role", r):
            frappe.get_doc({"doctype": "Role", "role_name": r, "desk_access": 1}).insert(ignore_permissions=True)


def create_default_sports():
    sports = [
        {"sport_name": "Football", "category": "Team Sport"},
        {"sport_name": "Basketball", "category": "Team Sport"},
        {"sport_name": "Cricket", "category": "Team Sport"},
        {"sport_name": "Tennis", "category": "Racquet Sport"},
        {"sport_name": "Badminton", "category": "Racquet Sport"},
        {"sport_name": "Swimming", "category": "Water Sport"},
        {"sport_name": "Athletics", "category": "Individual Sport"},
        {"sport_name": "Boxing", "category": "Combat Sport"},
        {"sport_name": "Wrestling", "category": "Combat Sport"},
        {"sport_name": "Yoga", "category": "Individual Sport"}
    ]
    for s in sports:
        if not frappe.db.exists("Sport", s["sport_name"]):
            frappe.get_doc({"doctype": "Sport", **s, "is_active": 1}).insert(ignore_permissions=True)


def create_custom_fields():
    from frappe.custom.doctype.custom_field.custom_field import create_custom_field
    create_custom_field("Customer", {
        "fieldname": "athlete",
        "label": "Athlete",
        "fieldtype": "Link",
        "options": "Athlete",
        "insert_after": "customer_name",
        "module": "Sports Training"
    })
