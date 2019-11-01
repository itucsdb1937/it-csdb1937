from flask import render_template, current_app, abort, request, url_for, redirect
from datetime import datetime
from product import Product

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

def product_page():
    db = current_app.config["db"]
    if request.method == "GET":
        products = db.get_products()
        return render_template("products.html",products = sorted(products))
    else:
        form_product_keys = request.form.getlist("product_keys")
        for form_product_key in form_product_keys:
            db.delete_product(int(form_product_key))
        return redirect(url_for("product_page"))
def customer_page():
    return render_template("customer.html")

def selected_product_page(product_key):
    db = current_app.config["db"]
    product = db.get_product(product_key)
    if product is None:
        abort(404)
    return render_template("product.html",product = product)

def product_add_page():
    if request.method == "GET":
        return render_template(
            "product_edit.html"
        )
    else:
        form_name = request.form["name"]
        form_price = request.form["price"]
        form_amount = request.form["amount"]
        product = Product(form_name, form_price,form_amount)
        db = current_app.config["db"]
        product_key = db.add_product(product)
        return redirect(url_for("product_page", product_key=product_key))