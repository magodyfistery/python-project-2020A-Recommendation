from models.serializable import Serializable


class OrderDetails(Serializable):

    def __init__(self, detail_number, id_order, id_product, quantity, subtotal):
        self.detail_number = detail_number  # int
        self.id_order = id_order  # int
        self.id_product = id_product  # int
        self.quantity = quantity  # int
        self.subtotal = subtotal  # float(10, 2)
    @staticmethod
    def insert_order_details(connection, order_details):
        cursor = connection.cursor()
        sql = "insert into order_details values (0,(SELECT max(id_order) from orders),{id_product},{quantity},{subtotal})".format(id_product=order_details.id_product,quantity=order_details.quantity,subtotal=order_details.subtotal)
        try:
            cursor.execute(sql)
            connection.commit()
            return True
        except Exception as e:
            print(__name__, "insert_order_details: " + str(e))
            return None

    @staticmethod
    def select_orders(connection, skip, step):
        cursor = connection.cursor()
        sql = "SELECT o.id_order, o.username_user, p.product_name, od.quantity, o.order_date, od.subtotal FROM order_details as od, orders as o, product as p "
        sql += "WHERE od.id_order = o.id_order AND od.id_product = p.id_product ORDER BY id_order ASC LIMIT {skip}, {step}".format(skip=skip, step=step)

        try:
            cursor.execute(sql)
            orders = []
            fetch = cursor.fetchall()
            for order in fetch:
                orders.append(
                    {
                        'id_order': order['id_order'],
                        'username_user': order['username_user'],
                        'product_name': order['product_name'],
                        'quantity': order['quantity'],
                        'order_date': str(order['order_date']),
                        'subtotal': order['subtotal']
                    }
                )
            return orders
        except Exception as e:
            print(__name__, "query: " + str(e))
            return []
