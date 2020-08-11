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
    