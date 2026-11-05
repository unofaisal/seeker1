// Copyright (c) 2026, one and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rent Payment", {
    setup(frm) {
        frm.set_query("contract", () => ({ filters: { docstatus: 1 } }));
    },
});
