from models.serializable import Serializable


class History(Serializable):

    def __init__(self, id_product, id_order, product_name, quantity, order_date, subtotal, rating):
        self.id_product = id_product
        self.id_order = id_order
        self.product_name = product_name
        self.quantity = quantity
        self.order_date = order_date
        self.subtotal=subtotal
        self.rating=rating
    @staticmethod
    def select_user_history(connection, username):
        cursor = connection.cursor()
        #No subqueries
        sql = "select product.id_product, orders.id_order, product.product_name, order_details.quantity, orders.order_date, order_details.subtotal, user_product_rating.rating from orders, product, order_details, user_product_rating where orders.username_user='{ouser}' and orders.id_order=order_details.id_order and order_details.id_product=product.id_product and user_product_rating.username_user = '{ruser}' and user_product_rating.id_product=product.id_product group by product.id_product".format(ouser=username,ruser=username)
        try:
            cursor.execute(sql)
            products = []
            fetch = cursor.fetchall()

            for row in fetch:
                print(row['rating'])
                products.append(History(
                    row['id_product'],
                    row['id_order'],
                    row['product_name'],
                    row['quantity'],
                    row['order_date'],
                    row['subtotal'],
                    row['rating']
                ))

            return products
        except Exception as e:
            print(__name__, "select_user_history: " + str(e))
            return None