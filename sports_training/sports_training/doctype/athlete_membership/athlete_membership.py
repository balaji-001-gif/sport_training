import frappe
from frappe.model.document import Document
from frappe.utils import add_months, flt


class AthleteMembership(Document):
    def validate(self):
        self.calculate_dates()
        self.calculate_balance()

    def calculate_dates(self):
        if self.start_date and self.membership_plan:
            duration = frappe.db.get_value("Membership Plan", self.membership_plan, "duration_months")
            if duration:
                self.end_date = add_months(self.start_date, duration)

    def calculate_balance(self):
        self.balance_due = flt(self.fee) - flt(self.amount_paid)
        if self.amount_paid == 0:
            self.payment_status = "Unpaid"
        elif self.balance_due > 0:
            self.payment_status = "Partial"
        else:
            self.payment_status = "Paid"

    def on_submit(self):
        self.update_athlete()
        self.create_sales_invoice()

    def update_athlete(self):
        athlete = frappe.get_doc("Athlete", self.athlete)
        athlete.membership_plan = self.membership_plan
        athlete.membership_start_date = self.start_date
        athlete.membership_end_date = self.end_date
        athlete.membership_status = "Active"
        athlete.save(ignore_permissions=True)

    def create_sales_invoice(self):
        if self.sales_invoice:
            return
        customer = frappe.db.get_value("Customer", {"athlete": self.athlete}, "name")
        if not customer:
            return
        si = frappe.new_doc("Sales Invoice")
        si.customer = customer
        si.due_date = self.start_date
        si.append("items", {
            "item_code": self.get_or_create_item(),
            "qty": 1,
            "rate": self.fee
        })
        si.insert(ignore_permissions=True)
        self.db_set("sales_invoice", si.name)

    def get_or_create_item(self):
        item_code = f"MEMB-{self.membership_plan}"
        if not frappe.db.exists("Item", item_code):
            item = frappe.new_doc("Item")
            item.item_code = item_code
            item.item_name = f"Membership - {self.membership_plan}"
            item.item_group = "Services"
            item.is_stock_item = 0
            item.is_service_item = 1
            item.insert(ignore_permissions=True)
        return item_code
