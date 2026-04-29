import frappe
from frappe.model.document import Document


class Coach(Document):
    def validate(self):
        self.coach_name = " ".join(filter(None, [self.first_name, self.last_name]))
        self.validate_schedule()

    def validate_schedule(self):
        if self.available_from and self.available_to:
            if self.available_from >= self.available_to:
                frappe.throw("Available From must be earlier than Available To")

    def get_assigned_athletes(self):
        return frappe.get_all("Athlete",
                              filters={"primary_coach": self.name, "status": "Active"},
                              fields=["name", "athlete_name", "primary_sport"])
