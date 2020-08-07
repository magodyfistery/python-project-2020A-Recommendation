class Product:
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
