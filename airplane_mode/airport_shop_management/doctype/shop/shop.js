// Copyright (c) 2026, one and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop", {
    setup(frm) {
        frm.set_query("shop_type", () => ({
            filters: { enabled: 1 },
        }));
    },
});