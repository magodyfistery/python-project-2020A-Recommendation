 
from models.serializable import Serializable

class Product(Serializable):
    def __init__(self, id_product, id_category, name, price, img_path, avgrating):
        self.id_product = id_product  # int
        self.id_category = id_category  # int
        self.name = name  # varchar(255)
        self.price = price  # float(10,2)
        self.img_path = img_path  # varchar(255)
        self.avgrating = avgrating  # float(2, 1)

    @staticmethod
    def select_best_sellers(connection, n):
        """
        Obtiene el top n de productos más vendidos
        :arg connection
        :arg n -> cantidad de best seller
        :returns lista de Product() o None
        """

        cursor = connection.cursor()
        sql = "select product.* from order_details, product order by order_details.quantity desc limit {n}".format(n=n)

        try:
            cursor.execute(sql)
            products = []
            fetch = cursor.fetchall()

            for product in fetch:
                products.append(Product(
                    product['id_product'],
                    product['id_category'],
                    product['product_name'],
                    product['price'],
                    product['img_path'],
                    product['avgrating'],
                ))
                print(product['product_name'])

            return products
        except Exception as e:
            print(__name__, "select_best_sellers: " + str(e))
            return None

    @staticmethod
    def select_top_rated(connection, n):
        cursor = connection.cursor()
        sql = "select * from product order by avgrating desc limit {n}".format(n=n)

        try:
            cursor.execute(sql)
            products = []
            fetch = cursor.fetchall()

            for product in fetch:
                products.append(Product(
                    product['id_product'],
                    product['id_category'],
                    product['product_name'],
                    product['price'],
                    product['img_path'],
                    product['avgrating'],
                ))

            return products
        except Exception as e:
            print(__name__, "select_top_rated: " + str(e))
            return None

    @staticmethod        
    def get_product(connection,id_product):
        cursor = connection.cursor()
        sql = "select * from product where id_product={id}".format(id=id_product)
        try:
            cursor.execute(sql)
            product = cursor.fetchone()
            return Product(
                    product['id_product'],
                    product['id_category'],
                    product['product_name'],
                    product['price'],
                    product['img_path'],
                    product['avgrating']
                )
        except Exception as e:
            print(__name__, "get_product: " + str(e))
            return None
    @staticmethod
    def select_similar_products(connection, prod, cat, n):
        cursor = connection.cursor()
        sql = "select product.* from product, category where category.id_category={cat} and product.id_category=category.id_category and product.id_product!={prod} limit {n}".format(cat=cat,prod=prod,n=n)
        #Alternativa
        #select * from product where product_name LIKE '%computer%' limit 1;
        try:
            cursor.execute(sql)
            products = []
            fetch = cursor.fetchall()
            for product in fetch:
                products.append(Product(
                    product['id_product'],
                    product['id_category'],
                    product['product_name'],
                    product['price'],
                    product['img_path'],
                    product['avgrating'],
                ))
            return products
        except Exception as e:
            print(__name__, "select_similar_products: " + str(e))
            return None
    @staticmethod
    def query(connection, string, n):
        cursor = connection.cursor()
        sql = "select * from product where product_name like '%{string}%' limit {n}".format(string=string, n=n)
        try:
            cursor.execute(sql)
            products = []
            fetch = cursor.fetchall()
            for product in fetch:
                products.append(Product(
                    product['id_product'],
                    product['id_category'],
                    product['product_name'],
                    product['price'],
                    product['img_path'],
                    product['avgrating'],
                ))
            return products
        except Exception as e:
            print(__name__, "query: " + str(e))
            return None