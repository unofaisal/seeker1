# Copyright (c) 2026, one and contributors
# For license information, please see license.txt

from datetime import date

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_last_day, getdate

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


class RentPayment(Document):
    def validate(self):
        self.validate_contract_period()
        self.validate_one_payment_per_month()

    def validate_contract_period(self):
        contract = frappe.db.get_value(
            "Shop Contract",
            self.contract,
            ["docstatus", "start_date", "expiry_date"],
            as_dict=True,
        )
        if contract.docstatus != 1:
            frappe.throw(_("The contract must be submitted before rent can be recorded."))

        period_start = date(int(self.for_year), MONTHS.index(self.for_month) + 1, 1)
        period_end = get_last_day(period_start)
        if period_end < getdate(contract.start_date) or period_start > getdate(contract.expiry_date):
            frappe.throw(_("{0} {1} is outside the contract period.").format(self.for_month, self.for_year))

    def validate_one_payment_per_month(self):
        duplicate = frappe.db.exists(
            "Rent Payment",
            {
                "contract": self.contract,
                "for_month": self.for_month,
                "for_year": self.for_year,
                "docstatus": ["<", 2],
                "name": ["!=", self.name],
            },
        )
        if duplicate:
            frappe.throw(_("Rent for {0} {1} is already recorded in {2}.").format(self.for_month, self.for_year, duplicate))
