import frappe
from frappe.utils import today, add_months


def make_demo_data():
    """Generate demo data for Sports Training app"""
    frappe.set_user("Administrator")
    
    # 1. Create Membership Plans
    plans = [
        {"doctype": "Membership Plan", "plan_name": "Standard Plan", "duration_months": 1, "fee": 5000, "max_sessions_per_month": 12},
        {"doctype": "Membership Plan", "plan_name": "Premium Plan", "duration_months": 3, "fee": 12000, "max_sessions_per_month": 24},
        {"doctype": "Membership Plan", "plan_name": "Elite Plan", "duration_months": 12, "fee": 40000, "max_sessions_per_month": 48}
    ]
    for p in plans:
        if not frappe.db.exists("Membership Plan", p["plan_name"]):
            frappe.get_doc(p).insert()
            
    # 2. Create Facilities
    facilities = [
        {"doctype": "Facility", "facility_name": "Main Gymnasium", "facility_type": "Gym", "capacity": 50},
        {"doctype": "Facility", "facility_name": "Olympic Pool", "facility_type": "Pool", "capacity": 20},
        {"doctype": "Facility", "facility_name": "Tennis Court A", "facility_type": "Court", "capacity": 4}
    ]
    for f in facilities:
        if not frappe.db.exists("Facility", f["facility_name"]):
            frappe.get_doc(f).insert()
            
    # 3. Create Coaches
    coaches = [
        {"doctype": "Coach", "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "specialization": "Fitness"},
        {"doctype": "Coach", "first_name": "Sarah", "last_name": "Smith", "email": "sarah.smith@example.com", "specialization": "Swimming"}
    ]
    created_coaches = []
    for c in coaches:
        existing = frappe.db.get_value("Coach", {"first_name": c["first_name"], "last_name": c["last_name"]}, "name")
        if not existing:
            doc = frappe.get_doc(c)
            doc.insert()
            created_coaches.append(doc.name)
        else:
            created_coaches.append(existing)
            
    # 4. Create Athletes
    athletes = [
        {"doctype": "Athlete", "first_name": "Mike", "last_name": "Tyson", "email": "mike.tyson@example.com", "primary_sport": "Boxing", "date_of_birth": "1966-06-30"},
        {"doctype": "Athlete", "first_name": "Emily", "last_name": "Blunt", "email": "emily.blunt@example.com", "primary_sport": "Tennis", "date_of_birth": "1983-02-23"}
    ]
    created_athletes = []
    for a in athletes:
        existing = frappe.db.get_value("Athlete", {"first_name": a["first_name"], "last_name": a["last_name"]}, "name")
        if not existing:
            doc = frappe.get_doc(a)
            doc.insert()
            created_athletes.append(doc.name)
        else:
            created_athletes.append(existing)
            
    # 5. Create Athlete Memberships
    for i, athlete in enumerate(created_athletes):
        plan_name = "Standard Plan" if i == 0 else "Premium Plan"
        if not frappe.db.exists("Athlete Membership", {"athlete": athlete}):
            doc = frappe.get_doc({
                "doctype": "Athlete Membership",
                "athlete": athlete,
                "membership_plan": plan_name,
                "start_date": today(),
                "end_date": add_months(today(), 1 if i == 0 else 3)
            })
            doc.insert()
            doc.submit()
            
    # 6. Create Training Sessions
    if created_coaches and created_athletes:
        if not frappe.db.exists("Training Session", {"primary_coach": created_coaches[0]}):
            session = frappe.get_doc({
                "doctype": "Training Session",
                "session_date": today(),
                "start_time": "08:00:00",
                "end_time": "09:00:00",
                "duration_hours": 1.0,
                "primary_coach": created_coaches[0],
                "facility": "Main Gymnasium",
                "athletes": [{"athlete": created_athletes[0]}],
                "status": "Scheduled"
            })
            session.insert()
            session.submit()

    frappe.db.commit()
