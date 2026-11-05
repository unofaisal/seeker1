# Copyright (c) 2026, one and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class ShopContract(Document):
    def validate(self):
        if getdate(self.expiry_date) <= getdate(self.start_date):
            frappe.throw(_("Expiry Date must be after Start Date."))

    def before_submit(self):
        status = frappe.db.get_value("Shop", self.shop, "status")
        if status != "Available":
            frappe.throw(_("Shop {0} is not available for lease.").format(self.shop))

    def on_submit(self):
        frappe.db.set_value("Shop", self.shop, {"status": "Occupied", "current_tenant": self.tenant})

    def on_cancel(self):
        frappe.db.set_value("Shop", self.shop, {"status": "Available", "current_tenant": None})
