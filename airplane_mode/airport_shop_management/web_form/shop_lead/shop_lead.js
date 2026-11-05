   frappe.ready(function () {
       const shop = new URLSearchParams(window.location.search).get("shop");
       if (shop) {
           frappe.web_form.set_value("shop", shop);
       }
   });