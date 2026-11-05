import frappe


def get_context(context):
    context.no_cache = 1
    name = frappe.form_dict.get("shop")

    if not name or not frappe.db.exists("Shop", name):
        frappe.throw("Shop not found", frappe.DoesNotExistError)

    # current_tenant is deliberately not fetched, so tenant details stay private
    shop = frappe.db.get_value(
        "Shop",
        name,
        ["name", "shop_name", "shop_number", "airport", "area_sq_ft", "status", "shop_type"],
        as_dict=True,
    )
    airport = frappe.db.get_value("Airport", shop.airport, ["code", "city"], as_dict=True)
    shop.airport_label = f"{airport.city} ({airport.code})" if airport else shop.airport
    context.shop = shop