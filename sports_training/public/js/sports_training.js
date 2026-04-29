frappe.provide("sports_training");
sports_training.utils = {
    get_athlete_summary: function(athlete) {
        return frappe.call({
            method: "sports_training.sports_training.doctype.athlete.athlete.get_athlete_dashboard_data",
            args: { athlete: athlete }
        });
    }
};
