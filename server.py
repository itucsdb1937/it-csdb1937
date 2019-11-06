from flask import Flask
from flask_login import LoginManager
import views
from database import Database
from product import Product
from user import get_user

lm = LoginManager()
@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    app.add_url_rule("/", view_func=views.home_page)

    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)

    app.add_url_rule("/products", view_func=views.product_page, methods=["GET", "POST"])
    app.add_url_rule("/customers", view_func=views.customer_page)
    app.add_url_rule("/products/<int:product_key>", view_func=views.selected_product_page)
    app.add_url_rule("/products/<int:product_key>/edit", view_func=views.selected_product_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/newProduct",view_func=views.product_add_page, methods=["GET","POST"])

    lm.init_app(app)
    lm.login_view = "login_page"

    db = Database()
    #db.add_product(Product("Mouse", 20, 2))
    #db.add_product(Product("Laptop",150,5))
    #db.add_product(Product("Desk", 100, 10))
    #db.add_product(Product("Chair", 70, 3))
    app.config["db"] = db

    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
