// Copyright (c) 2026, one and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        if (!frm.is_new() && frm.doc.docstatus === 0) {
            frm.add_custom_button(
                __("Set Seat"),
                () => {
                    frappe.prompt(
                        {
                            label: __("Seat Number"),
                            fieldname: "seat_number",
                            fieldtype: "Data",
                            reqd: 1,
                        },
                        (values) => {
                            frm.set_value("seat", values.seat_number);
                        },
                        __("Set Seat"),
                        __("Set")
                    );
                },
                __("Actions")
            );
        }
    },

    flight_price(frm) {
        calculate_total(frm);
    },
});

// Events for rows in the add_ons child table
frappe.ui.form.on("Airplane Ticket Add-on Item", {
    amount(frm) {
        calculate_total(frm);
    },
    add_ons_remove(frm) {
        calculate_total(frm);
    },
});

// Live preview only
function calculate_total(frm) {
    const add_ons_total = (frm.doc.add_ons || []).reduce(
        (sum, row) => sum + (row.amount || 0),
        0
    );
    frm.set_value("total_amount", (frm.doc.flight_price || 0) + add_ons_total);
}