from product import Product
import psycopg2 as dbapi2
import os
dsn = os.getenv('DATABASE_URL')

#dsn = """user='xpucwaxi' password='biCAXcXGlmoh5JdJBgAsrHNaF3dBeadP'
 #                        host='dumbo.db.elephantsql.com' port=5432 dbname='xpucwaxi'"""

class Database:
    def __init__(self):
        self.products = {}
        #self.product_id = 0


    def add_product(self,product):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO PRODUCTS (NAME, PRICE, AMOUNT, TYPE, BRAND) VALUES (%s, %s, %s, %s, %s) RETURNING ID"
            cursor.execute(query, (product.name, product.price, product.amount, product.type, product.brand))
            connection.commit()
            product_key = cursor.fetchone()[0]
        return product_key
        # self.products[self.product_id] = product
        # return  self.product_id
        #self.product_id += 1

    def update_product(self, product_key, product):
        #self.products[product_key] = product
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "UPDATE PRODUCTS SET NAME = %s, PRICE = %s, AMOUNT = %s, TYPE = %s, BRAND = %s WHERE (ID = %s)"
            cursor.execute(query,(product.name, product.price, product.amount, product.type, product.brand, product_key))
            connection.commit()

    def delete_product(self,product_key):
        #if product_key in self.products:
            #del self.products[product_key]
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM PRODUCTS WHERE (ID = %s)"
            cursor.execute(query, (product_key,))
            connection.commit()

    def get_product(self,product_key):
        '''product = self.products[product_key]
        if product is None:
            return None
        product_ = Product(product.name,product.price,product.amount)
        return product_'''
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT NAME, PRICE, AMOUNT, TYPE, BRAND FROM PRODUCTS WHERE (ID = %s)"
            cursor.execute(query,(product_key,))
            name, price, amount, type, brand = cursor.fetchone()
        product = Product(name, price, amount, type, brand)
        return product

    def get_products(self):
        product_arr = []
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM PRODUCTS ORDER BY ID"
            cursor.execute(query)
            for product_key, name, price, amount, type, brand  in cursor:
                product_arr.append((product_key, Product(name, price, amount, type, brand)))
        return product_arr
