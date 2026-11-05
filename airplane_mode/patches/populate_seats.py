import random

import frappe


def new_seat():
    return f"{random.randint(1, 99)}{random.choice('ABCDE')}"


def execute():
    tickets = frappe.get_all("Airplane Ticket", fields=["name", "flight", "seat"])

    # Seats already taken, per flight
    taken = {}
    for t in tickets:
        if t.seat:
            taken.setdefault(t.flight, set()).add(t.seat)

    for t in tickets:
        if t.seat:
            continue  # already has a seat, leave it alone

        used = taken.setdefault(t.flight, set())
        seat = new_seat()
        attempts = 0
        while seat in used and attempts < 100:
            seat = new_seat()
            attempts += 1

        used.add(seat)
        frappe.db.set_value("Airplane Ticket", t.name, "seat", seat, update_modified=False)
