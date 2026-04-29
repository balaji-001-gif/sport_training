import frappe
from frappe.model.document import Document


class PerformanceAssessment(Document):
    def validate(self):
        self.calculate_overall_score()

    def calculate_overall_score(self):
        scores = [
            self.speed_score, self.strength_score, self.endurance_score,
            self.agility_score, self.flexibility_score, self.technical_score,
            self.tactical_score, self.mental_score
        ]
        valid_scores = [s for s in scores if s]
        if valid_scores:
            self.overall_score = sum(valid_scores) / len(valid_scores)
