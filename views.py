from flask import render_template, current_app, abort, request, url_for, redirect, flash
from datetime import datetime
from product import Product
from flask_login import login_required, login_user, logout_user, current_user
from forms import LoginForm
from user import get_user
from passlib.hash import pbkdf2_sha256 as hasher


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


def product_page():
    db = current_app.config["db"]
    if request.method == "GET":
        products = db.get_products()
        return render_template("products.html", products=sorted(products))
    else:
        if not current_user.is_admin:
            abort(401)
        form_product_keys = request.form.getlist("product_keys")
        for form_product_key in form_product_keys:
            db.delete_product(int(form_product_key))
        flash("%(num)d products deleted." % {"num": len(form_product_keys)})
        return redirect(url_for("product_page"))


def customer_page():
    return render_template("customer.html")


def selected_product_page(product_key):
    db = current_app.config["db"]
    product = db.get_product(product_key)
    if product is None:
        abort(404)
    return render_template("product.html", product=product)


@login_required
def selected_product_edit_page(product_key):
    if request.method == "GET":
        db = current_app.config["db"]
        product = db.get_product(product_key)
        if product is None:
            abort(404)
        values = {"name": product.name, "price": product.price, "amount": product.amount, "type": product.type,
                  "brand": product.brand}
        return render_template("product_edit.html", values=values)
    else:
        valid = validate_product_form(request.form)
        if not valid:
            return render_template(
                "product_edit.html", values=request.form
            )
        form_name = request.form.data["name"]
        form_price = request.form.data["price"]
        form_amount = request.form.data["amount"]
        form_type = request.form.data["type"]
        form_brand = request.form.data["brand"]
        product = Product(form_name, form_price, form_amount, form_type, form_brand)
        db = current_app.config["db"]
        db.update_product(product_key, product)
        return redirect(url_for("selected_product_page", product_key=product_key))


@login_required
def product_add_page():
    if not current_user.is_admin:
        abort(401)
    if request.method == "GET":
        values = {"name": "", "price": "", "amount": "", "type": "", "brand": ""}
        return render_template(
            "product_edit.html", values=values
        )
    else:
        valid = validate_product_form(request.form)
        if not valid:
            return render_template(
                "product_edit.html", values=request.form
            )
        form_name = request.form.data["name"]
        form_price = request.form.data["price"]
        form_amount = request.form.data["amount"]
        form_type = request.form.data["type"]
        form_brand = request.form.data["brand"]
        product = Product(form_name, form_price, form_amount, form_type, form_brand)
        db = current_app.config["db"]
        product_key = db.add_product(product)
        return redirect(url_for("product_page", product_key=product_key))


def validate_product_form(form):
    form.data = {}
    form.errors = {}

    form_name = form.get("name", "").strip()
    if len(form_name) == 0:
        form.errors["name"] = "Name can not be blank."
    else:
        form.data["name"] = form_name

    form_price = form.get("price")
    if not form_price:
        form.errors["price"] = "Price can not be blank."
    elif not form_price.isdigit():
        form.errors["price"] = "Price must consist of digits only."
    else:
        price = float(form_price)
        if (price < 0):
            form.errors["price"] = "Price not in valid range."
        else:
            form.data["price"] = price

    form_amount = form.get("amount")
    if not form_amount:
        form.errors["amount"] = "Amount can not be blank."
    elif not form_amount.isdigit():
        form.errors["amount"] = "Amount must consist of digits only."
    else:
        amount = int(form_amount)
        if (amount <= 0):
            form.errors["amount"] = "You must add at least one item."
        else:
            form.data["amount"] = amount

    form_type = form.get("type")
    if not form_type:
        form.errors["type"] = "Type can not be blank."
    else:
        form.data["type"] = form_type

    form_brand = form.get("brand")
    if not form_brand:
        form.errors["brand"] = "Brand can not be blank."
    else:
        form.data["brand"] = form_brand

    return len(form.errors) == 0


def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = get_user(username)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))
