// Copyright (c) 2026, one and contributors
// For license information, please see license.txt

frappe.ui.form.on('Airplane Ticket', {
    validate(frm) {
    let seen_addons = new Set();

    (frm.doc.add_ons || []).forEach(row => {
        if (seen_addons.has(row.item)) {
            frappe.throw("You have duplicate addons");
            }
            seen_addons.add(row.item);
        });
    },
    refresh: function(frm) {
        calculate_total(frm);
    },
    flight_price: function(frm) {
        calculate_total(frm);
    },
    before_submit(frm){
    if (frm.doc.flight_status !== "Boarded"){
      frappe.throw("Only Boarded ticket status are submitable")
    }
  }
    'add_ons': function(frm) {
        calculate_total(frm);
    },
    'add_ons.amount': function(frm, cdt, cdn) {
        calculate_total(frm);
    }
});

function calculate_total(frm) {
    var flight_price = frm.doc.flight_price || 0;
    
    var add_ons_total = 0;
    if (frm.doc.add_ons && frm.doc.add_ons.length > 0) {
        frm.doc.add_ons.forEach(function(row) {
            add_ons_total += (row.amount || 0);
        });
    }
    
    var total = flight_price + add_ons_total;

    frm.set_value('total_amount', total);
}

frappe.ui.form.on("Airplane Ticket Add-on Item", {
  amount(frm){
    calculate_total(frm)
  }
	
})