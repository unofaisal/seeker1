# Copyright (c) 2026, one and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {
            "label": _("Airline"),
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": 200,
        },
        {
            "label": _("Revenue"),
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 150,
        },
    ]

    data = []
    total_revenue = 0

    airlines = frappe.get_all(
        "Airline",
        fields=["name"]
    )

    for airline in airlines:
        revenue = 0

        airplanes = frappe.get_all(
            "Airplane",
            filters={"airline": airline.name},
            pluck="name"
        )

        if airplanes:
            flights = frappe.get_all(
                "Airplane Flight",
                filters={
                    "airplane": ["in", airplanes]
                },
                pluck="name"
            )

            if flights:
                tickets = frappe.get_all(
                    "Airplane Ticket",
                    filters={
                        "flight": ["in", flights],
                        "docstatus": 1
                    },
                    fields=["total_amount"]
                )

                revenue = sum(ticket.total_amount for ticket in tickets)

        data.append({
            "airline": airline.name,
            "revenue": revenue
        })

        total_revenue += revenue

    chart = {
        "data": {
            "labels": [d["airline"] for d in data],
            "datasets": [
                {
                    "values": [d["revenue"] for d in data]
                }
            ]
        },
        "type": "donut"
    }

    report_summary = [
        {
            "value": total_revenue,
            "indicator": "Green",
            "label": _("Total Revenue"),
            "datatype": "Currency",
        }
    ]

    return columns, data, None, chart, report_summary