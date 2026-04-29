import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours


class TrainingSession(Document):
    def validate(self):
        self.calculate_duration()
        self.update_attendance_count()
        self.validate_coach_availability()

    def calculate_duration(self):
        if self.start_time and self.end_time:
            self.duration_hours = time_diff_in_hours(str(self.end_time), str(self.start_time))

    def update_attendance_count(self):
        present = sum(1 for a in self.athletes if a.attendance_status == "Present")
        absent = sum(1 for a in self.athletes if a.attendance_status == "Absent")
        self.athletes_present = present
        self.athletes_absent = absent

    def validate_coach_availability(self):
        if self.primary_coach and self.session_date and self.start_time and self.end_time:
            overlapping = frappe.db.sql("""
                SELECT name FROM `tabTraining Session`
                WHERE primary_coach = %s
                AND session_date = %s
                AND name != %s
                AND docstatus < 2
                AND ((start_time <= %s AND end_time > %s)
                  OR (start_time < %s AND end_time >= %s)
                  OR (start_time >= %s AND end_time <= %s))
            """, (self.primary_coach, self.session_date, self.name or "",
                  self.start_time, self.start_time,
                  self.end_time, self.end_time,
                  self.start_time, self.end_time))
            if overlapping:
                frappe.msgprint(f"Coach has overlapping session: {overlapping[0][0]}", alert=True)

    def on_submit(self):
        self.create_attendance_logs()

    def create_attendance_logs(self):
        for athlete in self.athletes:
            log = frappe.new_doc("Attendance Log")
            log.athlete = athlete.athlete
            log.training_session = self.name
            log.session_date = self.session_date
            log.status = athlete.attendance_status or "Present"
            log.coach = self.primary_coach
            log.insert(ignore_permissions=True)


@frappe.whitelist()
def get_program_athletes(training_program):
    return frappe.get_all("Athlete",
                          filters={"training_program": training_program, "status": "Active"},
                          fields=["name as athlete", "athlete_name"])
