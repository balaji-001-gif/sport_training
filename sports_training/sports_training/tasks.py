import frappe
from frappe.utils import today, add_days


def send_membership_expiry_reminders():
    """Daily: Send reminders 7 days before expiry"""
    target = add_days(today(), 7)
    athletes = frappe.get_all("Athlete",
                              filters={"membership_end_date": target, "membership_status": "Active"},
                              fields=["name", "athlete_name", "email"])
    for a in athletes:
        if a.email:
            frappe.sendmail(
                recipients=[a.email],
                subject="Membership Expiring Soon",
                message=f"Dear {a.athlete_name},<br>Your membership will expire on {target}. Please renew."
            )


def update_athlete_attendance_stats():
    """Daily: Recalculate attendance percentages"""
    pass


def generate_performance_reports():
    """Weekly: Email performance summary to coaches"""
    coaches = frappe.get_all("Coach", filters={"status": "Active"}, fields=["name", "email"])
    for c in coaches:
        if c.email:
            athletes = frappe.get_all("Athlete",
                                      filters={"primary_coach": c.name, "status": "Active"},
                                      fields=["athlete_name"])
            if athletes:
                msg = f"Weekly summary: {len(athletes)} active athletes assigned."
                frappe.sendmail(recipients=[c.email],
                                subject="Weekly Performance Summary",
                                message=msg)
