import frappe
from frappe.model.document import Document
from frappe.utils import add_days, getdate


class TrainingProgram(Document):
    def validate(self):
        if self.start_date and self.duration_weeks and not self.end_date:
            self.end_date = add_days(self.start_date, self.duration_weeks * 7)
        if self.start_date and self.end_date:
            if getdate(self.start_date) > getdate(self.end_date):
                frappe.throw("Start Date cannot be after End Date")
