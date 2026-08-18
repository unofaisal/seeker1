import frappe

def get_context(context):
    context.color = frappe.form_dict.get("color") or "black"
    context.no_cache = 1