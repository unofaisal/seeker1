# Copyright (c) 2026, one and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe import _
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
    def before_submit(self):
        self.status = "Completed"

    def on_change(self):
        # Runs after every save, including edits made after submit
        if self.has_value_changed("gate_number"):
            frappe.enqueue(
                "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_ticket_gates",
                queue="short",
                flight=self.name,
                gate_number=self.gate_number,
                enqueue_after_commit=True,
            )
            frappe.msgprint(
                _("Gate number changed. Tickets are being updated in the background."),
                alert=True,
            )

    def get_context(self, context):
        return context


def update_ticket_gates(flight, gate_number):
    """Background job: copy the flight's gate number onto its tickets."""
    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"flight": flight, "docstatus": ["<", 2]},
        pluck="name",
    )
    for name in tickets:
        frappe.db.set_value("Airplane Ticket", name, "gate_number", gate_number, update_modified=False)
