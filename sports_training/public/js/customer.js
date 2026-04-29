frappe.ui.form.on('Customer', {
    refresh: function(frm) {
        if (frm.doc.athlete) {
            frm.add_custom_button(__('View Athlete Profile'), function() {
                frappe.set_route('Form', 'Athlete', frm.doc.athlete);
            });
        }
    }
});
