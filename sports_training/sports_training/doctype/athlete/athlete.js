frappe.ui.form.on('Athlete', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Training Session'), function() {
                frappe.new_doc('Training Session', {athlete: frm.doc.name});
            }, __('Create'));

            frm.add_custom_button(__('Performance Assessment'), function() {
                frappe.new_doc('Performance Assessment', {athlete: frm.doc.name});
            }, __('Create'));

            frm.add_custom_button(__('Injury Record'), function() {
                frappe.new_doc('Injury Record', {athlete: frm.doc.name});
            }, __('Create'));

            frm.add_custom_button(__('View Performance'), function() {
                frappe.set_route('query-report', 'Athlete Performance Report',
                    {athlete: frm.doc.name});
            }, __('View'));
        }
    },

    date_of_birth: function(frm) {
        if (frm.doc.date_of_birth) {
            const age = moment().diff(frm.doc.date_of_birth, 'years');
            frm.set_value('age', age);
        }
    },

    height_cm: function(frm) { calculate_bmi(frm); },
    weight_kg: function(frm) { calculate_bmi(frm); }
});

function calculate_bmi(frm) {
    if (frm.doc.height_cm && frm.doc.weight_kg) {
        const h = frm.doc.height_cm / 100;
        const bmi = frm.doc.weight_kg / (h * h);
        frm.set_value('bmi', bmi.toFixed(2));
    }
}
