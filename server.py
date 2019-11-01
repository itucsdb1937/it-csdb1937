from flask import Flask
import views
from database import Database
from product import Product

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/products", view_func=views.product_page, methods=["GET", "POST"])
    app.add_url_rule("/customers", view_func=views.customer_page)
    app.add_url_rule("/products/<int:product_key>", view_func=views.selected_product_page)
    app.add_url_rule("/newProduct",view_func=views.product_add_page, methods=["GET","POST"])
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
