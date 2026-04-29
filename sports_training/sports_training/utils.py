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


def notify_session_scheduled(doc, method):
    """Notify primary coach and athletes when a Training Session is scheduled"""
    if doc.status == "Scheduled":
        if doc.primary_coach:
            coach_email = frappe.db.get_value("Coach", doc.primary_coach, "email")
            if coach_email:
                try:
                    frappe.sendmail(
                        recipients=[coach_email],
                        subject=f"New Training Session Scheduled: {doc.name}",
                        message=f"You have been assigned as the primary coach for session {doc.name} on {doc.session_date} at {doc.start_time}."
                    )
                except Exception:
                    frappe.log_error("Session notification email failed for Coach")
        
        for row in doc.athletes:
            athlete_email = frappe.db.get_value("Athlete", row.athlete, "email")
            if athlete_email:
                try:
                    frappe.sendmail(
                        recipients=[athlete_email],
                        subject=f"Upcoming Training Session Scheduled: {doc.name}",
                        message=f"A new training session {doc.name} has been scheduled for you on {doc.session_date} at {doc.start_time}."
                    )
                except Exception:
                    frappe.log_error("Session notification email failed for Athlete")


def notify_injury_alert(doc, method):
    """Notify primary coach when an injury is recorded for an athlete"""
    athlete_name = frappe.db.get_value("Athlete", doc.athlete, "athlete_name")
    primary_coach = frappe.db.get_value("Athlete", doc.athlete, "primary_coach")
    
    if primary_coach:
        coach_email = frappe.db.get_value("Coach", primary_coach, "email")
        if coach_email:
            try:
                frappe.sendmail(
                    recipients=[coach_email],
                    subject=f"Injury Alert: {athlete_name}",
                    message=f"An injury has been recorded for athlete {athlete_name} ({doc.athlete}) on {doc.injury_date}. Type: {doc.injury_type}. Severity: {doc.severity}."
                )
            except Exception:
                frappe.log_error("Injury alert email failed")


def notify_fitness_test_completed(doc, method):
    """Notify athlete when a fitness test is completed"""
    athlete_email = frappe.db.get_value("Athlete", doc.athlete, "email")
    athlete_name = frappe.db.get_value("Athlete", doc.athlete, "athlete_name")
    
    if athlete_email:
        try:
            frappe.sendmail(
                recipients=[athlete_email],
                subject=f"Fitness Test Results: {doc.name}",
                message=f"Dear {athlete_name},<br>Your fitness test ({doc.test_type}) results from {doc.test_date} have been recorded. Please log in to view details."
            )
        except Exception:
            frappe.log_error("Fitness test notification email failed")


