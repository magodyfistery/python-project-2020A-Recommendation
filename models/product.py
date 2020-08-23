 
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
    @staticmethod
    def select_category_products(connection,id):
        cursor = connection.cursor()
        sql = "select * from product where id_category={id}".format(id=id)
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
    @staticmethod
    def update_avg_rating(connection, pid):
        cursor = connection.cursor()
        sql1 = "select avg(rating) from user_product_rating where id_product={id_product} group by id_product".format(id_product=pid)
        try:
            cursor.execute(sql1)
            rating = cursor.fetchone()
            if rating['avg(rating)']:
                sql2 = "update product set avgrating={avg} where id_product={id_product}".format(avg=rating['avg(rating)'],id_product=pid)
                try:
                    cursor.execute(sql2)
                    connection.commit()
                    return True
                except Exception as e:
                    print(__name__, "update_avg_rating: " + str(e))
                    return False
        except Exception as e:
                print(__name__, "update_avg_rating: " + str(e))
                return False

    @staticmethod
    def select_products(connection, skip, step):
        cursor = connection.cursor()
        sql = "SELECT * FROM product LIMIT {skip}, {step}".format(skip=skip, step=step)
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
            return []


    def create(self, connection):
        cursor = connection.cursor()
        sql = "INSERT INTO product(id_category, product_name, price, img_path) "
        sql += "VALUES({id_category}, '{product_name}', {price}, '{img_path}')".format(id_category=self.id_category, product_name=self.name, price=self.price, img_path=self.img_path)

        try:
            cursor.execute(sql)
            connection.commit()
            return True
        except Exception as e:
            print(__name__, "get_product: " + str(e))
            return False

    def update(self, connection):
        cursor = connection.cursor()
        if self.img_path is None:
            sql = "UPDATE product set id_category={id_category}, product_name='{product_name}', price={price} WHERE id_product={id_product}".format(id_category=self.id_category, product_name=self.name, price=self.price, id_product=self.id_product)

        else:
            sql = "UPDATE product set id_category={id_category}, product_name='{product_name}', price={price}, img_path='{img_path}' WHERE id_product={id_product}".format(id_category=self.id_category, product_name=self.name, price=self.price, img_path=self.img_path, id_product=self.id_product)

        try:
            cursor.execute(sql)
            connection.commit()
            return True
        except Exception as e:
            print(__name__, "get_product: " + str(e))
            return False



