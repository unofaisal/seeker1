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

   
    let flight = await frappe.get_doc("Airplane Flight", frm.flight)
    let capacity = await frappe.get_doc("Airplane", flight.airplane).capacity
    let tickets = await frappe.db.count("Airplane Ticket", filters={"flight": flight, name: ['!=', frm.doc.name]})
    if (tickets+1 > capacity) {
        frappe.throw("The number of tickets for the flight can't exceed the number of seats in the flight's airplane")
    }

    },
    refresh: function(frm) {
        calculate_total(frm);

        if (!frm.is_new()) {
            frm.add_custom_button(__('Set Seat'), function() {
                frappe.prompt(
                    {
                        label: __('Seat Number'),
                        fieldname: 'seat_number',
                        fieldtype: 'Data',
                        reqd: 1
                    },
                    function(values) {
                        frm.set_value('seat', values.seat_number);
                    },
                    __('Set Seat'),
                    __('Set')
                );
            }, __('Actions'));
        }
    },
    flight_price: function(frm) {
        calculate_total(frm);
    },
    before_submit(frm){
    if (frm.doc.flight_status !== "Boarded"){
      frappe.throw("Only Boarded ticket status are submitable")
    }
  },
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