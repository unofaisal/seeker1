import frappe


def get_context(context):
    context.no_cache = 1

    airports = {a.name: a for a in frappe.get_all("Airport", fields=["name", "code", "city"])}
    shops = frappe.get_all(
        "Shop",
        fields=["name", "shop_name", "shop_number", "airport", "area_sq_ft", "status", "shop_type"],
        order_by="airport asc, shop_number asc",
    )
    for shop in shops:
        airport = airports.get(shop.airport)
        shop.airport_label = f"{airport.city} ({airport.code})" if airport else shop.airport
    context.shops = shops