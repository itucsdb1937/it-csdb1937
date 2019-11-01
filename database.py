from product import Product

class Database:
    def __init__(self):
        self.products = {}
        self.product_id = 0

    def add_product(self,product):
        self.product_id += 1
        self.products[self.product_id] = product
        return  self.product_id

    def delete_product(self,product_key):
        if product_key in self.products:
            del self.products[product_key]

    def get_product(self,product_key):
        product = self.products[product_key]
        if product is None:
            return None
        product_ = Product(product.name,product.price,product.amount)
        return product_

    def get_products(self):
        product_arr = []
        for product_key,product in self.products.items():
            product_ = Product(product.name, product.price, product.amount)
            product_arr.append((product_key,product_))
        return product_arr
