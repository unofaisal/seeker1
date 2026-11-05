// Copyright (c) 2026, one and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop Contract", {
    async onload(frm) {
        if (frm.is_new() && !frm.doc.rent_amount) {
            const rent = await frappe.db.get_single_value("Shop Settings", "default_rent_amount");
            if (rent) {
                frm.set_value("rent_amount", rent);
            }
        }
    },
});