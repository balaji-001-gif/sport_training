import frappe
from frappe.model.document import Document


class InjuryRecord(Document):
    def validate(self):
        if self.actual_recovery_date and self.status not in ["Recovered", "Closed"]:
            self.status = "Recovered"
