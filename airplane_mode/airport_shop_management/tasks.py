import frappe
from frappe.utils import getdate, today

from airplane_mode.airport_shop_management.doctype.rent_payment.rent_payment import MONTHS


def send_rent_reminders():
    # Global switch from Shop Settings
    if not frappe.db.get_single_value("Shop Settings", "enable_rent_reminders"):
        return

    current = getdate(today())
    month = MONTHS[current.month - 1]
    year = current.year

    contracts = frappe.get_all(
        "Shop Contract",
        filters={
            "docstatus": 1,
            "start_date": ["<=", current],
            "expiry_date": [">=", current],
        },
        fields=["name", "shop", "tenant", "rent_amount"],
    )

    for contract in contracts:
        already_paid = frappe.db.exists(
            "Rent Payment",
            {
                "contract": contract.name,
                "for_month": month,
                "for_year": year,
                "docstatus": ["<", 2],
            },
        )
        if already_paid:
            continue

        tenant = frappe.db.get_value("Tenant", contract.tenant, ["tenant_name", "email"], as_dict=True)
        if not tenant or not tenant.email:
            continue

        frappe.sendmail(
            recipients=[tenant.email],
            subject=f"Rent due for {month} {year}",
            message=(
                f"Dear {tenant.tenant_name},<br><br>"
                f"This is a reminder that the rent of {frappe.format_value(contract.rent_amount, {'fieldtype': 'Currency'})} "
                f"for shop {contract.shop} is due for {month} {year}.<br><br>"
                "Thank you."
            ),
            reference_doctype="Shop Contract",
            reference_name=contract.name,
        )