# Copyright (c) 2026, one and contributors
# For license information, please see license.txt

import random

import frappe
from frappe import _
from frappe.model.document import Document


class AirplaneTicket(Document):
    def before_insert(self):
        self.check_capacity()
        booked = set(
            frappe.get_all(
                "Airplane Ticket",
                filters={"flight": self.flight, "seat": ["is", "set"]},
                pluck="seat",
            )
        )
        seat = f"{random.randint(1, 99)}{random.choice('ABCDE')}"
        attempts = 0
        while seat in booked and attempts < 100:
            seat = f"{random.randint(1, 99)}{random.choice('ABCDE')}"
            attempts += 1
        self.seat = seat


    def validate(self):
        # Runs every time the ticket is saved
        self.remove_duplicate_addons()
        self.calculate_total_amount()

    def before_submit(self):
        # Only allow submission once the passenger has boarded
        if self.status != "Boarded":
            frappe.throw(_("A ticket can only be submitted when its status is Boarded."))

    def remove_duplicate_addons(self):
        seen = set()
        unique_rows = []
        for row in self.add_ons:
            if row.item in seen:
                continue  # skip repeated add-on types
            seen.add(row.item)
            unique_rows.append(row)
        self.set("add_ons", unique_rows)

    def calculate_total_amount(self):
        add_ons_total = sum((row.amount or 0) for row in self.add_ons)
        self.total_amount = (self.flight_price or 0) + add_ons_total

    def check_capacity(self):
        airplane = frappe.db.get_value("Airplane Flight", self.flight, "airplane")
        capacity = frappe.db.get_value("Airplane", airplane, "capacity")
        tickets = frappe.db.count("Airplane Ticket", {"flight": self.flight})
        if tickets >= capacity:
            frappe.throw(_("This flight is full. The airplane has only {0} seats.").format(capacity))
