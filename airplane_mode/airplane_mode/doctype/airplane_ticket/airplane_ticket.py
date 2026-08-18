# Copyright (c) 2026, one and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import random


class AirplaneTicket(Document):
	def before_insert(self):
		self.seat = f"{random.randint(1, 99)}{random.choice('ABCDE')}"
