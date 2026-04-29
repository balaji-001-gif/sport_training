import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today, date_diff, flt


class Athlete(Document):
    def validate(self):
        self.set_full_name()
        self.calculate_age()
        self.calculate_bmi()
        self.validate_membership_dates()
        self.update_membership_status()

    def set_full_name(self):
        self.athlete_name = " ".join(filter(None, [self.first_name, self.last_name]))

    def calculate_age(self):
        if self.date_of_birth:
            self.age = int(date_diff(today(), self.date_of_birth) / 365.25)

    def calculate_bmi(self):
        if self.height_cm and self.weight_kg:
            height_m = flt(self.height_cm) / 100
            self.bmi = flt(self.weight_kg) / (height_m * height_m)

    def validate_membership_dates(self):
        if self.membership_start_date and self.membership_end_date:
            if getdate(self.membership_start_date) > getdate(self.membership_end_date):
                frappe.throw("Membership End Date cannot be before Start Date")

    def update_membership_status(self):
        if not self.membership_end_date:
            self.membership_status = "Pending"
            return
        if getdate(self.membership_end_date) < getdate(today()):
            self.membership_status = "Expired"
        else:
            self.membership_status = "Active"

    def on_update(self):
        self.create_or_update_customer()

    def create_or_update_customer(self):
        """Sync athlete with ERPNext Customer for billing"""
        if not frappe.db.exists("Customer", {"athlete": self.name}):
            customer = frappe.new_doc("Customer")
            customer.customer_name = self.athlete_name
            customer.customer_type = "Individual"
            customer.customer_group = frappe.db.get_single_value("Selling Settings", "customer_group") or "Individual"
            customer.territory = frappe.db.get_single_value("Selling Settings", "territory") or "All Territories"
            customer.athlete = self.name
            customer.insert(ignore_permissions=True)


@frappe.whitelist()
def get_athlete_dashboard_data(athlete):
    """Returns dashboard summary data for an athlete"""
    data = {
        "total_sessions": frappe.db.count("Training Session", {"athlete": athlete, "docstatus": 1}),
        "attended_sessions": frappe.db.count("Attendance Log", {"athlete": athlete, "status": "Present"}),
        "assessments": frappe.db.count("Performance Assessment", {"athlete": athlete}),
        "injuries": frappe.db.count("Injury Record", {"athlete": athlete, "status": "Open"}),
    }
    return data
